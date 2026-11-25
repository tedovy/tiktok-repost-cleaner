<p align="center"><img src="icons/icon128.png" width="96" alt=""></p>

# TikTok Repost Cleaner

[English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md) · [العربية](README.ar.md) · **Deutsch** · [Français](README.fr.md) · [Español](README.es.md) · [Português (BR)](README.pt-BR.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Türkçe](README.tr.md)

Eine Browser-Erweiterung, die deine TikTok-Reposts mit einem Klick entfernt – alle oder nur die neuesten.

- **Schnell.** Die Repost-Liste wird seitenweise parallel gelesen, und Reposts werden mit Dutzenden parallelen Anfragen entfernt. Das Entfernen beginnt schon, während die Liste noch gelesen wird.
- **Alle oder die neuesten N.** Alles löschen oder eingeben, wie viele der neuesten Reposts entfernt werden sollen.
- **Drei Tempi:** Vorsichtig, Normal und Schnell.
- **Live-Fortschritt** auf der TikTok-Seite: Zähler, Tempo pro Sekunde und ein Stopp-Button.
- **11 Sprachen.** Die Erweiterung folgt der Sprache deines Browsers.
- Funktioniert in **Chrome, Edge, Brave, Opera, Arc, Yandex Browser** und anderen Chromium-Browsern.

## Installation

1. Lade `tiktok-repost-cleaner-*.zip` aus dem [neuesten Release](https://github.com/tedovy/tiktok-repost-cleaner/releases/latest) herunter.
2. Entpacke die Datei.
3. Öffne `chrome://extensions` (Edge: `edge://extensions`, Yandex: `browser://extensions`).
4. Aktiviere den **Entwicklermodus**.
5. Klicke auf **Entpackte Erweiterung laden** und wähle den entpackten Ordner.
6. Hefte die Erweiterung an die Symbolleiste an (Puzzle-Symbol → Pin).

## Benutzung

1. Melde dich in diesem Browser bei TikTok an.
2. Klicke auf das Symbol der Erweiterung.
3. Wähle **Alle** oder **Neueste…** und gib die Anzahl ein.
4. Klicke auf **Entfernen**. Dein Profil öffnet sich und das Entfernen startet sofort; ein Panel in der Ecke zeigt den Fortschritt. Lass den Tab offen, bis **Fertig** erscheint.
5. Klicke auf **Seite neu laden**, um deine aktualisierten Reposts zu sehen.

## Tempo und TikTok-Limits

| Modus | Listenseiten gleichzeitig | Entfernungen gleichzeitig |
|---|---|---|
| Vorsichtig | 1 | 3 |
| Normal | 4 | 16 |
| Schnell | 8 | 48 |

Das Entfernen ist für TikTok leicht, die Repost-Liste dagegen ist schwer, und TikTok begrenzt sie vorübergehend für das ganze Konto, wenn sie zu oft abgefragt wird (eine Weile bleibt dann sogar der Reposts-Tab auf der Website leer). Passiert das, pausiert die Erweiterung und versucht es erneut; hebt sich das Limit nicht, hält sie an und zeigt, wie viele Reposts entfernt wurden. Warte ein paar Minuten und klicke erneut – sie macht einfach mit dem Rest weiter.

## So funktioniert es

Die Erweiterung klickt sich nicht durch die Website. Aus deinem geöffneten TikTok-Tab sendet sie dieselben Anfragen wie die TikTok-Website:

- `GET /api/repost/item_list/` – deine Repost-Liste, 30 pro Seite;
- `POST /tiktok/v1/upvote/delete?item_id=…` – dieselbe Anfrage wie der Button **Repost entfernen**.

Es wird nichts an andere Stellen als TikTok gesendet. Die Erweiterung sammelt keine Daten und liest weder Passwörter noch Cookies.

## Berechtigungen

- `tiktok.com` – um im TikTok-Tab zu laufen;
- `scripting` – um das Entfernen in diesem Tab zu starten;
- `tabs` – um dein Profil zu öffnen;
- `storage` – um deine Einstellungen zu speichern.

## Haftungsausschluss

Kein Bezug zu TikTok oder ByteDance. Die Erweiterung nutzt inoffizielle Web-Schnittstellen von TikTok, die sich jederzeit ändern können. Entfernte Reposts lassen sich nicht automatisch wiederherstellen. Nutzung auf eigenes Risiko.

## Lizenz

MIT – siehe [LICENSE](LICENSE).
