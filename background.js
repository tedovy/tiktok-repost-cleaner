// Opens the TikTok profile and starts the repost cleaner inside that tab.

const PROFILE_URL = "https://www.tiktok.com/profile";
const PROFILE_RE = /^https:\/\/www\.tiktok\.com\/@[^/?#]+\/?(?:[?#].*)?$/;
const LOGIN_RE = /^https:\/\/www\.tiktok\.com\/login/;
const START_TIMEOUT_MS = 30000;

// Message keys passed to runner.js (chrome.i18n is not available in the page's MAIN world).
const RUNNER_KEYS = [
  "panelTitle", "hide", "stop", "reload", "starting", "collecting", "found", "deleting",
  "throttled", "of", "rate", "stopping", "stopped", "none", "done", "failedTail", "notLoggedIn", "limited",
];

const msg = (key) => chrome.i18n.getMessage(key);

function runnerLocale() {
  const strings = {};
  for (const key of RUNNER_KEYS) {
    const text = msg(key);
    if (text) strings[key] = text;
  }
  return { strings, dir: msg("@@bidi_dir") || "ltr" };
}

// Pending jobs live in session storage: the service worker may restart while the tab loads.
const pendingKey = (tabId) => `pending:${tabId}`;

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message?.cmd === "start") {
    start(message.options || {})
      .then(() => sendResponse({ ok: true }))
      .catch((e) => sendResponse({ ok: false, error: String(e?.message || e) }));
    return true; // async response
  }
  if (message?.cmd === "tiktokReady" && sender.tab?.id != null) {
    onTikTokReady(sender.tab.id, sender.url || sender.tab.url || "");
  }
});

async function start(options) {
  const [active] = await chrome.tabs.query({ active: true, currentWindow: true });

  // Already on a profile page: start right here, no reload.
  if (active && PROFILE_RE.test(active.url || "")) {
    await callRunner(active.id, "start", { ...options, ...runnerLocale() });
    return;
  }

  const onTikTok = active?.url?.startsWith("https://www.tiktok.com/");
  const tab = onTikTok
    ? await chrome.tabs.update(active.id, { url: PROFILE_URL, active: true })
    : await chrome.tabs.create({ url: PROFILE_URL, active: true });

  await chrome.storage.session.set({ [pendingKey(tab.id)]: { options, at: Date.now() } });
}

// Called by ready.js as soon as a TikTok page starts (document_start).
async function onTikTokReady(tabId, url) {
  const key = pendingKey(tabId);
  const { [key]: job } = await chrome.storage.session.get(key);
  if (!job) return;

  if (Date.now() - job.at > START_TIMEOUT_MS) {
    await chrome.storage.session.remove(key);
    return;
  }
  if (LOGIN_RE.test(url)) {
    await chrome.storage.session.remove(key);
    await callRunner(tabId, "error", { ...runnerLocale(), message: msg("errLogin") }).catch(() => {});
    return;
  }
  if (!PROFILE_RE.test(url)) return; // e.g. /profile before it redirects to /@username

  await chrome.storage.session.remove(key);
  await callRunner(tabId, "start", { ...job.options, ...runnerLocale() }).catch(() => {});
}

async function callRunner(tabId, method, arg) {
  await chrome.scripting.executeScript({
    target: { tabId },
    world: "MAIN",
    injectImmediately: true,
    files: ["runner.js"],
  });
  await chrome.scripting.executeScript({
    target: { tabId },
    world: "MAIN",
    injectImmediately: true,
    func: (m, a) => { window.__repostCleaner[m](a); },
    args: [method, arg],
  });
}
