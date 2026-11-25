<p align="center"><img src="icons/icon128.png" width="96" alt=""></p>

# TikTok Repost Cleaner

**English** · [Русский](README.ru.md) · [简体中文](README.zh-CN.md) · [العربية](README.ar.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Português (BR)](README.pt-BR.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Türkçe](README.tr.md)

A browser extension that removes your TikTok reposts in one click — all of them, or only the latest few.

- **Fast.** The repost list is read many pages at a time, and reposts are removed by dozens of parallel requests. Removing starts while the list is still being read.
- **All or latest N.** Clear everything, or type how many of the newest reposts to remove.
- **Three speeds:** Careful, Normal and Fast.
- **Live progress** on the TikTok page: counter, speed per second and a Stop button.
- **11 languages.** The extension follows your browser language.
- Works in **Chrome, Edge, Brave, Opera, Arc, Yandex Browser** and other Chromium browsers.

## Install

1. Download `tiktok-repost-cleaner-*.zip` from the [latest release](https://github.com/tedovy/tiktok-repost-cleaner/releases/latest).
2. Unzip it.
3. Open `chrome://extensions` (Edge: `edge://extensions`, Yandex: `browser://extensions`).
4. Turn on **Developer mode**.
5. Click **Load unpacked** and choose the unzipped folder.
6. Pin the extension to the toolbar (puzzle icon → pin).

## How to use

1. Log in to TikTok in this browser.
2. Click the extension icon.
3. Choose **All** or **Latest…** and type how many.
4. Press **Remove**. Your profile opens and removal starts right away; a panel in the corner shows progress. Keep the tab open until it says **Done**.
5. Press **Refresh page** to see your updated reposts.

## Speed and TikTok limits

| Mode | List pages at once | Removals at once |
|---|---|---|
| Careful | 1 | 3 |
| Normal | 4 | 16 |
| Fast | 8 | 48 |

Removing is quick for TikTok, but the repost list is heavy, and TikTok temporarily limits it for the whole account when it's requested too often (for a while even the Reposts tab on the site stays empty). If that happens, the extension pauses and retries; if the limit doesn't lift, it stops and tells you how many reposts were removed. Wait a few minutes and press the button again — it simply continues with what's left.

## How it works

The extension doesn't click through the site. From your open TikTok tab it sends the same requests the TikTok website sends:

- `GET /api/repost/item_list/` — your repost list, 30 per page;
- `POST /tiktok/v1/upvote/delete?item_id=…` — the same request as the **Remove repost** button.

Nothing is sent anywhere except TikTok. The extension collects no data and doesn't read your passwords or cookies.

## Permissions

- `tiktok.com` — to run inside the TikTok tab;
- `scripting` — to start the cleaner in that tab;
- `tabs` — to open your profile;
- `storage` — to remember your settings.

## Disclaimer

Not affiliated with TikTok or ByteDance. The extension uses TikTok's unofficial web endpoints, which can change at any time. Removed reposts can't be restored automatically. Use at your own risk.

## License

MIT — see [LICENSE](LICENSE).
