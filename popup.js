const $ = (id) => document.getElementById(id);
const msg = (key, ...subs) => chrome.i18n.getMessage(key, subs.map(String));
const SPEEDS = ["careful", "normal", "fast"];
const opts = { mode: "all", count: 10, speed: "fast" };

document.documentElement.lang = chrome.i18n.getUILanguage();
document.documentElement.dir = msg("@@bidi_dir") || "ltr";
for (const el of document.querySelectorAll("[data-i18n]")) {
  el.textContent = msg(el.dataset.i18n);
}

function pick(groupId, value) {
  for (const b of $(groupId).querySelectorAll("button")) {
    b.classList.toggle("on", b.dataset.value === value);
  }
}

function goLabel() {
  return opts.mode === "all" ? msg("btnAll") : msg("btnLast", opts.count || "…");
}

function render() {
  pick("mode", opts.mode);
  pick("speed", opts.speed);
  $("countRow").hidden = opts.mode !== "count";
  $("count").value = opts.count;
  $("go").textContent = goLabel();
}

function save() {
  chrome.storage.local.set({ opts }).catch(() => {});
}

$("mode").addEventListener("click", (e) => {
  const v = e.target.closest("button")?.dataset.value;
  if (!v) return;
  opts.mode = v;
  render(); save();
  if (v === "count") $("count").focus();
});

$("speed").addEventListener("click", (e) => {
  const v = e.target.closest("button")?.dataset.value;
  if (!v) return;
  opts.speed = v;
  render(); save();
});

$("count").addEventListener("input", () => {
  const n = parseInt($("count").value, 10);
  opts.count = n > 0 ? n : "";
  $("go").textContent = goLabel();
  save();
});

$("count").addEventListener("keydown", (e) => { if (e.key === "Enter") $("go").click(); });

$("go").addEventListener("click", async () => {
  $("msg").textContent = "";
  if (opts.mode === "count" && !(opts.count > 0)) {
    $("msg").textContent = msg("needCount");
    $("count").focus();
    return;
  }
  $("go").disabled = true;
  const res = await chrome.runtime.sendMessage({
    cmd: "start",
    options: { mode: opts.mode, count: Number(opts.count), speed: opts.speed },
  }).catch((e) => ({ ok: false, error: e.message }));
  // If the popup is still open (e.g. the TikTok tab was already active), show the error here.
  $("go").disabled = false;
  if (res && !res.ok) $("msg").textContent = res.error;
  else window.close();
});

chrome.storage.local.get("opts").then(({ opts: saved }) => {
  if (saved) {
    if (saved.mode === "all" || saved.mode === "count") opts.mode = saved.mode;
    if (saved.count > 0) opts.count = saved.count;
    if (SPEEDS.includes(saved.speed)) opts.speed = saved.speed;
  }
  render();
}).catch(render);
render();
