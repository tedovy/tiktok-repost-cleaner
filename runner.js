// Runs inside the TikTok tab (MAIN world). Scans the repost list through the site's own API
// (many pages in parallel) and removes reposts with a pool of parallel requests.
// Requests go through the page's window.fetch, so TikTok's own code signs them.
(() => {
  if (window.__repostCleaner) return;

  const LIST_URL = "/api/repost/item_list/";
  const DELETE_URL = "/tiktok/v1/upvote/delete";
  const PAGE_SIZE = 30; // TikTok rejects larger pages (status 10201)
  const MAX_PAGES = 2000; // safety cap: 60k reposts
  const MAX_PASSES = 3; // extra passes only if a scan was cut short
  const BACKOFF_MS = [2000, 5000, 15000, 30000, 60000];

  // pages: list pages fetched in parallel; workers: parallel delete requests.
  // Removing is cheap for TikTok, but list pages are heavy (~600 KB each) and the list API
  // gets rate-limited for the whole account if hammered — so the list side stays modest.
  const SPEEDS = {
    careful: { pages: 1, workers: 3, gap: 250 },
    normal: { pages: 4, workers: 16, gap: 0 },
    fast: { pages: 8, workers: 48, gap: 0 },
  };

  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const state = { running: false, stop: false, pauseUntil: 0 };

  // Localized strings come from the extension (chrome.i18n is not available in MAIN world).
  let strings = {
    panelTitle: "Removing reposts",
    hide: "Hide",
    stop: "Stop",
    reload: "Refresh page",
    starting: "Starting…",
    collecting: "Scanning reposts…",
    found: "Scanning… found {n}",
    deleting: "Removing reposts…",
    throttled: "TikTok is slowing down, waiting {n} s…",
    of: "of {n}",
    rate: "{n}/s",
    stopping: "Stopping…",
    stopped: "Stopped. Removed: {n}.",
    none: "No reposts — nothing to remove.",
    done: "Done! Reposts removed: {n}.",
    failedTail: " Failed: {n}.",
    notLoggedIn: "You don't seem to be logged in to TikTok. Log in and press the button again.",
    limited: "TikTok is limiting requests right now. Removed: {n}. Try again in a few minutes.",
  };
  let dir = "ltr";

  const t = (key, n) => String(strings[key] ?? key).replace(/\{n\}/g, String(n ?? ""));

  function configure(opts) {
    if (opts?.strings) strings = { ...strings, ...opts.strings };
    if (opts?.dir) dir = opts.dir;
  }

  // ---------- Page readiness ----------

  function readSecUid() {
    const el = document.getElementById("__UNIVERSAL_DATA_FOR_REHYDRATION__");
    if (!el) return null;
    try {
      const scope = JSON.parse(el.textContent).__DEFAULT_SCOPE__ || {};
      return scope["webapp.app-context"]?.user?.secUid || null;
    } catch {
      return null;
    }
  }

  // The secUid is in the initial HTML, so we can start long before the page finishes loading.
  async function waitForPage(timeoutMs = 20000) {
    const until = Date.now() + timeoutMs;
    let secUid = null;
    while (Date.now() < until && !(secUid = readSecUid())) await sleep(100);
    if (!secUid) throw new Error(t("notLoggedIn"));
    return secUid;
  }

  // ---------- Requests with a shared back-off ----------

  async function respectPause() {
    while (Date.now() < state.pauseUntil) await sleep(Math.min(500, state.pauseUntil - Date.now()));
  }

  async function withRetry(fn) {
    for (let attempt = 0; ; attempt++) {
      await respectPause();
      try {
        return await fn();
      } catch (e) {
        if (attempt >= BACKOFF_MS.length || state.stop) throw e;
        const wait = BACKOFF_MS[attempt];
        // One slow-down pauses every worker, so we don't hammer TikTok while it's limiting us.
        if (Date.now() + wait > state.pauseUntil) {
          state.pauseUntil = Date.now() + wait;
          ui.status(t("throttled", Math.round(wait / 1000)));
        }
      }
    }
  }

  async function fetchJson(url, init) {
    const res = await fetch(url, { credentials: "include", ...init });
    const text = await res.text();
    let json = null;
    try { json = JSON.parse(text); } catch { /* empty or not JSON */ }
    if (!res.ok || !json) throw new Error(`HTTP ${res.status}`);
    return json;
  }

  async function fetchPage(secUid, cursor) {
    return withRetry(async () => {
      const j = await fetchJson(
        `${LIST_URL}?aid=1988&count=${PAGE_SIZE}&cursor=${cursor}&secUid=${encodeURIComponent(secUid)}`
      );
      if (j.statusCode !== 0 && j.status_code !== 0) throw new Error(j.statusMsg || "list error");
      return { ids: (j.itemList || []).map((i) => i?.id).filter(Boolean), hasMore: !!j.hasMore };
    });
  }

  async function deleteRepost(id) {
    return withRetry(async () => {
      const j = await fetchJson(`${DELETE_URL}?aid=1988&item_id=${id}`, { method: "POST" });
      if (j.status_code !== 0) throw new Error(j.status_msg || `code ${j.status_code}`);
      return true;
    });
  }

  // ---------- Scan + remove, at the same time ----------
  // The list cursor is an offset, so pages 0, 30, 60… can be fetched in parallel.
  // Removed reposts keep their slot in the list for a while (pages come back with holes),
  // so offsets don't shift while we delete — scanning and removing can overlap.
  // Pages are handed to the removers strictly in order, so "latest N" really means the newest N.
  async function run(secUid, limit, skip, speed, done, failed) {
    const seen = new Set(skip);
    const before = done.size + failed.size;
    const queue = [];
    const pages = new Map(); // page index -> ids, waiting to be handed over in order
    const waiting = [];      // removers waiting for work
    let nextPage = 0;        // next page to request
    let flushed = 0;         // pages already handed to the removers
    let endPage = Infinity;  // first page index past the end of the list
    let queued = 0;
    let scanning = true;
    let cut = false;         // the scan stopped early because TikTok refused a page
    const startedAt = performance.now();

    const wakeAll = () => { while (waiting.length) waiting.pop()(); };

    const flush = () => {
      while (pages.has(flushed) && queued < limit) {
        for (const id of pages.get(flushed)) {
          if (queued >= limit) break;
          if (seen.has(id)) continue;
          seen.add(id);
          queue.push(id);
          queued++;
        }
        pages.delete(flushed);
        flushed++;
      }
      if (queued >= limit) endPage = Math.min(endPage, flushed);
      if (queued) ui.setTotal(before + queued, scanning && flushed < endPage);
      if (!done.size) ui.status(t("found", queued));
      wakeAll();
    };

    const scanner = async () => {
      while (!state.stop && nextPage < endPage && nextPage < MAX_PAGES) {
        const page = nextPage++;
        let r;
        try {
          r = await fetchPage(secUid, page * PAGE_SIZE);
        } catch {
          // TikTok kept refusing this page: stop here; the next pass will try again.
          endPage = Math.min(endPage, page);
          cut = true;
          break;
        }
        if (!r.hasMore) endPage = Math.min(endPage, page + 1);
        pages.set(page, r.ids);
        flush();
        if (speed.gap) await sleep(speed.gap);
      }
    };

    const remover = async () => {
      while (!state.stop) {
        const id = queue.shift();
        if (id === undefined) {
          if (!scanning) return;
          await new Promise((resolve) => waiting.push(resolve));
          continue;
        }
        try {
          await deleteRepost(id);
          done.add(id);
          if (Date.now() >= state.pauseUntil) ui.status(t("deleting"));
        } catch {
          failed.add(id);
        }
        const secs = (performance.now() - startedAt) / 1000;
        ui.progress(done.size, failed.size, secs > 1 ? Math.round((done.size + failed.size - before) / secs) : 0);
        if (speed.gap) await sleep(speed.gap);
      }
    };

    const removers = Array.from({ length: speed.workers }, remover);
    await Promise.all(Array.from({ length: speed.pages }, scanner));
    scanning = false;
    flush();
    await Promise.all(removers);
    return { queued, complete: !cut };
  }

  // ---------- Main ----------

  async function start(opts = {}) {
    configure(opts);
    if (state.running) { ui.show(); return; }
    state.running = true;
    state.stop = false;
    state.pauseUntil = 0;

    const limit = opts.mode === "count" && opts.count > 0 ? Math.floor(opts.count) : Infinity;
    const speed = SPEEDS[opts.speed] || SPEEDS.fast;
    const done = new Set();
    const failed = new Set();

    ui.show();
    ui.reset(limit);
    ui.status(t("collecting"));

    try {
      const secUid = await waitForPage();
      document.querySelector('[data-e2e="repost-tab"]')?.click();

      // Removed reposts keep their slot in the list, so one pass covers everything.
      // Another pass is only needed if TikTok refused part of the list.
      let complete = false;
      for (let pass = 0; pass < MAX_PASSES && !state.stop; pass++) {
        const left = limit - done.size;
        if (left <= 0) { complete = true; break; }
        ui.status(t("collecting"));
        ui.scanning();
        const r = await run(secUid, left, new Set([...done, ...failed]), speed, done, failed);
        complete = r.complete;
        if (complete || !r.queued) break;
      }

      if (state.stop) {
        ui.finish(t("stopped", done.size));
      } else if (!complete) {
        ui.finish(t("limited", done.size), true);
      } else if (!done.size && !failed.size) {
        ui.finish(t("none"));
      } else {
        ui.finish(t("done", done.size) + (failed.size ? t("failedTail", failed.size) : ""));
      }
    } catch (e) {
      ui.finish(String(e?.message || e), true);
    } finally {
      state.running = false;
    }
  }

  function stop() {
    state.stop = true;
    ui.status(t("stopping"));
  }

  function error(opts) {
    configure(opts);
    ui.show();
    ui.reset(Infinity);
    ui.finish(opts?.message || "Error", true);
  }

  // ---------- Panel on top of the page ----------

  const ui = (() => {
    let root, els, total = Infinity;

    function build() {
      const host = document.createElement("div");
      host.id = "repost-cleaner-host";
      host.style.cssText = "position:fixed;bottom:20px;z-index:2147483647;";
      root = host.attachShadow({ mode: "open" });
      root.innerHTML = `
        <style>
          :host { all: initial; }
          .card { width: 300px; box-sizing: border-box; padding: 16px; border-radius: 16px;
            background: #121212; color: #f1f1f2; border: 1px solid rgba(255,255,255,.08);
            box-shadow: 0 12px 40px rgba(0,0,0,.5);
            font: 14px/1.4 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans", sans-serif; }
          .head { display:flex; align-items:center; justify-content:space-between; margin-bottom: 12px; }
          .title { font-weight: 700; font-size: 15px; }
          .x { all: unset; cursor: pointer; color: rgba(255,255,255,.5); font-size: 18px; padding: 0 4px; }
          .x:hover { color: #fff; }
          .row { display:flex; align-items: baseline; justify-content: space-between; gap: 8px; }
          .count { font-size: 28px; font-weight: 800; letter-spacing: -.5px; font-variant-numeric: tabular-nums; }
          .count small { font-size: 15px; font-weight: 600; color: rgba(255,255,255,.5); letter-spacing: 0; }
          .rate { font-size: 13px; font-weight: 600; color: rgba(255,255,255,.5); font-variant-numeric: tabular-nums; }
          .bar { height: 6px; border-radius: 3px; background: rgba(255,255,255,.1); margin: 10px 0; overflow: hidden; }
          .fill { height: 100%; width: 0; background: #fe2c55; border-radius: 3px; transition: width .2s ease; }
          .bar.indet .fill { width: 30%; animation: slide 1.1s ease-in-out infinite; }
          @keyframes slide { from { transform: translateX(-100%); } to { transform: translateX(340%); } }
          [dir="rtl"] .bar.indet .fill { animation-name: slide-rtl; }
          @keyframes slide-rtl { from { transform: translateX(100%); } to { transform: translateX(-340%); } }
          .status { color: rgba(255,255,255,.65); font-size: 13px; min-height: 18px; }
          .status.err { color: #ff6b81; }
          .btns { display:flex; gap: 8px; margin-top: 14px; }
          button.b { all: unset; flex: 1; text-align: center; cursor: pointer; padding: 9px 0; border-radius: 10px;
            font-weight: 600; font-size: 14px; background: rgba(255,255,255,.1); color: #fff; }
          button.b:hover { background: rgba(255,255,255,.16); }
          button.b.primary { background: #fe2c55; }
          button.b.primary:hover { background: #ff4468; }
          [hidden] { display: none !important; }
        </style>
        <div class="card">
          <div class="head"><span class="title"></span><button class="x">×</button></div>
          <div class="row">
            <div class="count"><span class="n">0</span> <small class="of"></small></div>
            <div class="rate"></div>
          </div>
          <div class="bar indet"><div class="fill"></div></div>
          <div class="status"></div>
          <div class="btns">
            <button class="b stop"></button>
            <button class="b primary reload" hidden></button>
          </div>
        </div>`;
      els = {
        card: root.querySelector(".card"),
        title: root.querySelector(".title"),
        n: root.querySelector(".n"),
        of: root.querySelector(".of"),
        rate: root.querySelector(".rate"),
        bar: root.querySelector(".bar"),
        fill: root.querySelector(".fill"),
        status: root.querySelector(".status"),
        stop: root.querySelector(".stop"),
        reload: root.querySelector(".reload"),
        close: root.querySelector(".x"),
      };
      els.stop.onclick = stop;
      els.reload.onclick = () => location.reload();
      els.close.onclick = () => { host.style.display = "none"; };
      document.documentElement.appendChild(host);
    }

    function applyText() {
      els.card.dir = dir;
      root.host.style.right = dir === "rtl" ? "" : "20px";
      root.host.style.left = dir === "rtl" ? "20px" : "";
      els.title.textContent = t("panelTitle");
      els.close.title = t("hide");
      els.stop.textContent = t("stop");
      els.reload.textContent = t("reload");
    }

    return {
      show() {
        if (!root) build();
        applyText();
        root.host.style.display = "";
      },
      reset(limit) {
        total = limit;
        els.n.textContent = "0";
        els.of.textContent = limit === Infinity ? "" : t("of", limit);
        els.rate.textContent = "";
        els.bar.classList.add("indet");
        els.fill.style.width = "";
        els.status.classList.remove("err");
        els.status.textContent = t("starting");
        els.stop.hidden = false;
        els.reload.hidden = true;
      },
      scanning() {
        els.bar.classList.add("indet");
        els.fill.style.width = "";
      },
      setTotal(n, growing = false) {
        total = n;
        els.of.textContent = t("of", n) + (growing ? "+" : "");
        els.bar.classList.remove("indet");
      },
      progress(ok, bad, perSec) {
        els.n.textContent = String(ok);
        if (perSec) els.rate.textContent = t("rate", perSec);
        const pct = total === Infinity ? 0 : Math.min(100, ((ok + bad) / total) * 100);
        els.fill.style.width = `${pct}%`;
      },
      status(text) {
        if (els) els.status.textContent = text;
      },
      finish(text, isError = false) {
        els.bar.classList.remove("indet");
        if (!isError) els.fill.style.width = "100%";
        els.status.textContent = text;
        els.status.classList.toggle("err", isError);
        els.stop.hidden = true;
        els.reload.hidden = false;
      },
    };
  })();

  window.__repostCleaner = { start, stop, error };
})();
