<p align="center"><img src="icons/icon128.png" width="96" alt=""></p>

# TikTok Repost Cleaner

[English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md) · [العربية](README.ar.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Português (BR)](README.pt-BR.md) · [日本語](README.ja.md) · **한국어** · [Türkçe](README.tr.md)

TikTok 리포스트를 클릭 한 번으로 삭제하는 브라우저 확장 프로그램입니다. 전부 또는 최근 것만 삭제할 수 있어요.

- **빠름.** 리포스트 목록을 여러 페이지씩 동시에 읽고, 수십 개의 병렬 요청으로 삭제합니다. 목록을 읽는 동안 이미 삭제가 시작됩니다.
- **전체 또는 최근 N개.** 전부 지우거나, 삭제할 최근 리포스트 개수를 입력하세요.
- **세 가지 속도:** 신중하게, 보통, 빠르게.
- **TikTok 페이지에서 실시간 진행 상황:** 카운터, 초당 속도, 중지 버튼.
- **11개 언어.** 브라우저 언어에 맞춰 표시됩니다.
- **Chrome, Edge, Brave, Opera, Arc, Yandex Browser** 등 Chromium 기반 브라우저에서 작동합니다.

## 설치

1. [최신 릴리스](https://github.com/tedovy/tiktok-repost-cleaner/releases/latest)에서 `tiktok-repost-cleaner-*.zip`을 내려받으세요.
2. 압축을 푸세요.
3. `chrome://extensions`를 여세요 (Edge: `edge://extensions`, Yandex: `browser://extensions`).
4. **개발자 모드**를 켜세요.
5. **압축해제된 확장 프로그램을 로드합니다**를 누르고 압축을 푼 폴더를 선택하세요.
6. 확장 프로그램을 툴바에 고정하세요 (퍼즐 아이콘 → 핀).

## 사용 방법

1. 이 브라우저에서 TikTok에 로그인하세요.
2. 확장 프로그램 아이콘을 누르세요.
3. **전체** 또는 **최근…**을 고르고 개수를 입력하세요.
4. **삭제**를 누르세요. 프로필이 열리고 바로 삭제가 시작되며, 구석의 패널에 진행 상황이 표시됩니다. **완료**가 나올 때까지 탭을 닫지 마세요.
5. **페이지 새로고침**을 누르면 업데이트된 리포스트 목록을 볼 수 있어요.

## 속도와 TikTok 제한

| 모드 | 동시에 읽는 목록 페이지 | 동시에 삭제하는 개수 |
|---|---|---|
| 신중하게 | 1 | 3 |
| 보통 | 4 | 16 |
| 빠르게 | 8 | 48 |

삭제는 TikTok에 부담이 적지만 리포스트 목록은 무거워서, 너무 자주 요청하면 TikTok이 계정 전체에 대해 일시적으로 제한합니다 (한동안 사이트의 리포스트 탭도 비어 보여요). 이럴 때 확장 프로그램은 잠시 멈췄다가 다시 시도하고, 제한이 풀리지 않으면 멈추고 삭제한 개수를 알려줍니다. 몇 분 기다린 뒤 버튼을 다시 누르면 남은 것부터 이어서 진행합니다.

## 작동 방식

확장 프로그램은 사이트를 클릭하지 않습니다. 열려 있는 TikTok 탭에서 TikTok 웹사이트와 같은 요청을 보냅니다:

- `GET /api/repost/item_list/` — 리포스트 목록, 페이지당 30개;
- `POST /tiktok/v1/upvote/delete?item_id=…` — **리포스트 삭제** 버튼과 같은 요청.

TikTok 외에는 어디에도 데이터를 보내지 않습니다. 확장 프로그램은 데이터를 수집하지 않으며 비밀번호나 쿠키를 읽지 않습니다.

## 권한

- `tiktok.com` — TikTok 탭 안에서 실행하기 위해;
- `scripting` — 그 탭에서 삭제를 시작하기 위해;
- `tabs` — 프로필을 열기 위해;
- `storage` — 설정을 기억하기 위해.

## 면책 조항

TikTok 또는 ByteDance와 관련이 없습니다. 이 확장 프로그램은 언제든 바뀔 수 있는 TikTok의 비공식 웹 API를 사용합니다. 삭제한 리포스트는 자동으로 복구할 수 없습니다. 사용에 따른 책임은 본인에게 있습니다.

## 라이선스

MIT — [LICENSE](LICENSE)를 참고하세요.
