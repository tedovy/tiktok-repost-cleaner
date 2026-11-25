<p align="center"><img src="icons/icon128.png" width="96" alt=""></p>

# TikTok Repost Cleaner

[English](README.md) · [Русский](README.ru.md) · **简体中文** · [العربية](README.ar.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Português (BR)](README.pt-BR.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Türkçe](README.tr.md)

一个浏览器扩展，一键删除你在 TikTok 上的转发——全部删除，或只删除最近几条。

- **速度快。** 一次并行读取多页转发列表，并用数十个并行请求删除转发。列表还在读取时就已开始删除。
- **全部或最近 N 条。** 可以全部清空，也可以输入要删除的最近转发数量。
- **三种速度：** 谨慎、正常、快速。
- **在 TikTok 页面上实时显示进度：** 计数、每秒速度和“停止”按钮。
- **11 种语言。** 扩展会跟随你的浏览器语言。
- 支持 **Chrome、Edge、Brave、Opera、Arc、Yandex 浏览器** 以及其他基于 Chromium 的浏览器。

## 安装

1. 从[最新发布](https://github.com/tedovy/tiktok-repost-cleaner/releases/latest)下载 `tiktok-repost-cleaner-*.zip`。
2. 解压。
3. 打开 `chrome://extensions`（Edge：`edge://extensions`，Yandex：`browser://extensions`）。
4. 开启 **开发者模式**。
5. 点击 **加载已解压的扩展程序**，选择解压后的文件夹。
6. 把扩展固定到工具栏（拼图图标 → 图钉）。

## 使用方法

1. 在此浏览器中登录 TikTok。
2. 点击扩展图标。
3. 选择 **全部** 或 **最近…** 并输入数量。
4. 点击 **删除**。会打开你的主页并立即开始删除，角落里的面板显示进度。在显示 **完成** 之前不要关闭标签页。
5. 点击 **刷新页面** 查看更新后的转发列表。

## 速度与 TikTok 的限制

| 模式 | 同时读取的列表页数 | 同时删除的数量 |
|---|---|---|
| 谨慎 | 1 | 3 |
| 正常 | 4 | 16 |
| 快速 | 8 | 48 |

删除操作对 TikTok 来说很轻松，但转发列表很大。请求过于频繁时，TikTok 会对整个账号暂时限制该列表（一段时间内网站上的“转发”标签页也会是空的）。遇到这种情况，扩展会暂停并重试；如果限制一直不解除，它会停止并告诉你已删除多少条。等几分钟再点一次按钮即可，它会继续处理剩下的转发。

## 工作原理

扩展不会在网页上模拟点击。它在你打开的 TikTok 标签页中发送与 TikTok 网站相同的请求：

- `GET /api/repost/item_list/` —— 你的转发列表，每页 30 条；
- `POST /tiktok/v1/upvote/delete?item_id=…` —— 与 **删除转发** 按钮相同的请求。

除了 TikTok 本身，不会向任何地方发送数据。扩展不收集任何数据，也不读取你的密码或 Cookie。

## 权限

- `tiktok.com` —— 在 TikTok 标签页中运行；
- `scripting` —— 在该标签页中启动清理；
- `tabs` —— 打开你的主页；
- `storage` —— 记住你的设置。

## 免责声明

本项目与 TikTok 或字节跳动无关。扩展使用 TikTok 非官方的网页接口，这些接口随时可能变化。删除的转发无法自动恢复。使用风险自负。

## 许可证

MIT —— 见 [LICENSE](LICENSE)。
