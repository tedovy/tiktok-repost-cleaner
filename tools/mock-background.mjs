// Runs background.js against a fake chrome.* API: node tools/mock-background.mjs
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import assert from "node:assert/strict";

const root = path.join(path.dirname(new URL(import.meta.url).pathname), "..");
const src = fs.readFileSync(path.join(root, "background.js"), "utf8");
const en = JSON.parse(fs.readFileSync(path.join(root, "_locales/en/messages.json"), "utf8"));

function makeChrome({ activeUrl }) {
  const listeners = { message: [], updated: [], removed: [] };
  const session = new Map();
  const injected = [];
  let nextId = 100;
  const tabs = new Map([[1, { id: 1, url: activeUrl, active: true }]]);
  const chrome = {
    i18n: { getMessage: (k) => (k === "@@bidi_dir" ? "ltr" : en[k]?.message ?? "") },
    runtime: { onMessage: { addListener: (f) => listeners.message.push(f) } },
    storage: {
      session: {
        set: async (o) => { for (const [k, v] of Object.entries(o)) session.set(k, v); },
        get: async (k) => (session.has(k) ? { [k]: session.get(k) } : {}),
        remove: async (k) => { session.delete(k); },
      },
    },
    tabs: {
      query: async () => [...tabs.values()].filter((t) => t.active),
      create: async ({ url }) => { const t = { id: nextId++, url, active: true }; tabs.set(t.id, t); return t; },
      update: async (id, { url }) => { const t = tabs.get(id); t.url = url; return t; },
      onUpdated: { addListener: (f) => listeners.updated.push(f) },
      onRemoved: { addListener: (f) => listeners.removed.push(f) },
    },
    scripting: {
      executeScript: async (o) => {
        injected.push({ tabId: o.target.tabId, world: o.world, now: o.injectImmediately, files: o.files, args: o.args });
      },
    },
  };
  vm.runInContext(src, vm.createContext({ chrome, console }));
  const send = (message, sender = {}) =>
    new Promise((resolve) => {
      let async = false;
      for (const f of listeners.message) if (f(message, sender, resolve) === true) async = true;
      if (!async) resolve(undefined);
    });
  const tick = () => new Promise((r) => setTimeout(r, 10));
  return { chrome, send, listeners, session, injected, tabs, tick };
}

const starts = (w) => w.injected.filter((i) => i.args?.[0] === "start");

async function test(name, fn) { await fn(); console.log(`ok  ${name}`); }

await test("not on TikTok: opens profile, starts when /@user page begins loading", async () => {
  const w = makeChrome({ activeUrl: "https://example.com/" });
  const res = await w.send({ cmd: "start", options: { mode: "all", speed: "fast" } });
  assert.equal(res?.ok, true);
  const tab = [...w.tabs.values()].find((t) => t.id >= 100);
  assert.equal(tab.url, "https://www.tiktok.com/profile");
  assert.ok(w.session.has(`pending:${tab.id}`), "job remembered");

  await w.send({ cmd: "tiktokReady" }, { tab: { id: tab.id }, url: "https://www.tiktok.com/profile" });
  await w.tick();
  assert.equal(starts(w).length, 0, "ignores /profile before redirect");

  await w.send({ cmd: "tiktokReady" }, { tab: { id: tab.id }, url: "https://www.tiktok.com/@someone?lang=en" });
  await w.tick();
  const s = starts(w);
  assert.equal(s.length, 1);
  assert.equal(s[0].world, "MAIN");
  assert.equal(s[0].now, true);
  assert.equal(s[0].args[1].mode, "all");
  assert.equal(s[0].args[1].speed, "fast");
  assert.equal(s[0].args[1].strings.done, en.done.message);
  assert.ok(!w.session.has(`pending:${tab.id}`), "job cleared");
});

await test("already on a profile page: starts right away without reloading", async () => {
  const w = makeChrome({ activeUrl: "https://www.tiktok.com/@me" });
  await w.send({ cmd: "start", options: { mode: "count", count: 5, speed: "normal" } });
  assert.equal(starts(w).length, 1);
  assert.equal(w.tabs.get(1).url, "https://www.tiktok.com/@me");
});

await test("on TikTok feed: reuses the tab and navigates to the profile", async () => {
  const w = makeChrome({ activeUrl: "https://www.tiktok.com/foryou" });
  await w.send({ cmd: "start", options: { mode: "all" } });
  assert.equal(w.tabs.get(1).url, "https://www.tiktok.com/profile");
  assert.ok(w.session.has("pending:1"));
});

await test("logged out: shows the login error on the page", async () => {
  const w = makeChrome({ activeUrl: "https://example.com/" });
  await w.send({ cmd: "start", options: {} });
  const tab = [...w.tabs.values()].find((t) => t.id >= 100);
  await w.send({ cmd: "tiktokReady" }, { tab: { id: tab.id }, url: "https://www.tiktok.com/login?redirect_url=x" });
  await w.tick();
  const err = w.injected.find((i) => i.args?.[0] === "error");
  assert.ok(err);
  assert.equal(err.args[1].message, en.errLogin.message);
  assert.equal(starts(w).length, 0);
});

await test("backup trigger: tab update to /@user starts the job", async () => {
  const w = makeChrome({ activeUrl: "https://example.com/" });
  await w.send({ cmd: "start", options: { mode: "all" } });
  const tab = [...w.tabs.values()].find((t) => t.id >= 100);
  tab.url = "https://www.tiktok.com/@me";
  for (const f of w.listeners.updated) f(tab.id, { url: tab.url }, tab);
  await w.tick();
  assert.equal(starts(w).length, 1);
});

await test("other tabs and pages are left alone", async () => {
  const w = makeChrome({ activeUrl: "https://example.com/" });
  await w.send({ cmd: "tiktokReady" }, { tab: { id: 1 }, url: "https://www.tiktok.com/@me" });
  for (const f of w.listeners.updated) f(1, { status: "complete" }, { id: 1, url: "https://www.tiktok.com/@me" });
  await w.tick();
  assert.equal(w.injected.length, 0);
});
