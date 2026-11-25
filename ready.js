// Tiny content script: tells the extension a TikTok page has started, so a pending
// cleanup can begin right away instead of waiting for every image and video to load.
chrome.runtime.sendMessage({ cmd: "tiktokReady" }).catch(() => {});
