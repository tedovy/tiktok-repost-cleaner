// Runs runner.js against a fake TikTok (no network): node tools/mock-test.mjs
// The fake server mimics what we saw on the real site: 30 items per page, offset cursors,
// removed reposts leave holes instead of shifting the list, random latency, and
// occasional empty 200 responses when "rate-limited".
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import assert from "node:assert/strict";

const src = fs.readFileSync(path.join(path.dirname(new URL(import.meta.url).pathname), "..", "runner.js"), "utf8");

function fakeElement() {
  const el = {
    style: {}, classList: { add() {}, remove() {}, toggle() {} }, dataset: {},
    textContent: "", hidden: false, dir: "", title: "",
    attachShadow: () => el, appendChild() {}, click() {},
    querySelector: () => fakeElement(),
    set innerHTML(_) {},
  };
  el.host = el;
  return el;
}

function makeWorld({ total, limitedEvery = 0, latency = [5, 40] }) {
  const ids = Array.from({ length: total }, (_, i) => `75${String(total - i).padStart(17, "0")}`); // newest first, unique
  const deleted = new Set();
  let calls = 0;
  const stats = { list: 0, del: 0, limited: 0, maxConcurrent: 0, concurrent: 0 };
  const respond = (body) => ({ ok: true, status: 200, text: async () => body });

  async function fetch(url, init = {}) {
    stats.concurrent++;
    stats.maxConcurrent = Math.max(stats.maxConcurrent, stats.concurrent);
    await new Promise((r) => setTimeout(r, latency[0] + Math.random() * (latency[1] - latency[0])));
    stats.concurrent--;
    calls++;
    if (limitedEvery && calls % limitedEvery === 0) { stats.limited++; return respond(""); }
    const u = new URL(url, "https://www.tiktok.com");
    if (u.pathname === "/api/repost/item_list/") {
      stats.list++;
      const cursor = Number(u.searchParams.get("cursor"));
      const count = Number(u.searchParams.get("count"));
      if (count > 30) return respond(JSON.stringify({ statusCode: 10201 }));
      const slice = ids.slice(cursor, cursor + count).filter((id) => !deleted.has(id));
      return respond(JSON.stringify({
        statusCode: 0, status_code: 0, cursor: String(cursor + count),
        hasMore: cursor + count < ids.length, itemList: slice.map((id) => ({ id })),
      }));
    }
    if (u.pathname === "/tiktok/v1/upvote/delete" && init.method === "POST") {
      stats.del++;
      deleted.add(u.searchParams.get("item_id"));
      return respond(JSON.stringify({ status_code: 0, status_msg: "" }));
    }
    return { ok: false, status: 404, text: async () => "" };
  }

  const rehydration = { textContent: JSON.stringify({ __DEFAULT_SCOPE__: { "webapp.app-context": { user: { secUid: "SEC" } } } }) };
  const document = {
    readyState: "complete",
    documentElement: fakeElement(),
    getElementById: (id) => (id === "__UNIVERSAL_DATA_FOR_REHYDRATION__" ? rehydration : null),
    createElement: () => fakeElement(),
    querySelector: () => null,
  };
  const window = {};
  const ctx = vm.createContext({ window, document, fetch, setTimeout, performance, location: { reload() {} }, console });
  vm.runInContext(src, ctx);
  return { cleaner: window.__repostCleaner, ids, deleted, stats };
}

async function test(name, fn) {
  const t0 = Date.now();
  await fn();
  console.log(`ok  ${name} (${Date.now() - t0} ms)`);
}

await test("all: removes every repost in one pass", async () => {
  const w = makeWorld({ total: 2495 });
  await w.cleaner.start({ mode: "all", speed: "fast" });
  assert.equal(w.deleted.size, 2495);
  assert.equal(w.stats.del, 2495, "no repost removed twice");
  assert.ok(w.stats.list <= Math.ceil(2495 / 30) + 8, `list calls ${w.stats.list}`);
});

await test("latest N: removes exactly the newest N", async () => {
  const w = makeWorld({ total: 500 });
  await w.cleaner.start({ mode: "count", count: 77, speed: "fast" });
  assert.equal(w.deleted.size, 77);
  for (const id of w.ids.slice(0, 77)) assert.ok(w.deleted.has(id), "newest removed");
  assert.ok(w.stats.list <= 6, `list calls ${w.stats.list}`); console.log(`    list calls: ${w.stats.list}`);
});

await test("latest N larger than list: removes everything", async () => {
  const w = makeWorld({ total: 40 });
  await w.cleaner.start({ mode: "count", count: 1000, speed: "normal" });
  assert.equal(w.deleted.size, 40);
});

await test("empty list: nothing to do", async () => {
  const w = makeWorld({ total: 0 });
  await w.cleaner.start({ mode: "all", speed: "fast" });
  assert.equal(w.stats.del, 0);
});

await test("rate limiting: retries and still finishes", async () => {
  const w = makeWorld({ total: 300, limitedEvery: 25 });
  await w.cleaner.start({ mode: "all", speed: "fast" });
  assert.equal(w.deleted.size, 300);
  assert.ok(w.stats.limited > 0);
});

await test("stop: halts quickly", async () => {
  const w = makeWorld({ total: 3000, latency: [20, 60] });
  const run = w.cleaner.start({ mode: "all", speed: "normal" });
  await new Promise((r) => setTimeout(r, 400));
  w.cleaner.stop();
  await run;
  const after = w.deleted.size;
  await new Promise((r) => setTimeout(r, 300));
  assert.ok(after > 0 && after < 3000, `removed ${after}`);
  assert.equal(w.deleted.size, after, "nothing removed after stop finished");
});

await test("parallelism stays within the fast preset", async () => {
  const w = makeWorld({ total: 1500 });
  await w.cleaner.start({ mode: "all", speed: "fast" });
  assert.ok(w.stats.maxConcurrent <= 8 + 48, `max concurrent ${w.stats.maxConcurrent}`);
  console.log(`    max concurrent requests: ${w.stats.maxConcurrent}`);
});

await test("latest N with holes at the top: reads further and removes the next N", async () => {
  const w = makeWorld({ total: 400 });
  for (const id of w.ids.slice(0, 40)) w.deleted.add(id); // removed earlier, still occupying slots
  await w.cleaner.start({ mode: "count", count: 50, speed: "fast" });
  assert.equal(w.stats.del, 50);
  for (const id of w.ids.slice(40, 90)) assert.ok(w.deleted.has(id), "next newest removed");
  assert.ok(!w.deleted.has(w.ids[90]), "nothing beyond N");
});

await test("latest N when TikTok keeps refusing the list: finishes instead of hanging", async () => {
  const w = makeWorld({ total: 400, limitedEvery: 1 });
  const t0 = Date.now();
  await w.cleaner.start({ mode: "count", count: 50, speed: "fast" });
  assert.equal(w.stats.del, 0);
  console.log(`    gave up after ${Math.round((Date.now() - t0) / 1000)} s of back-off`);
});
