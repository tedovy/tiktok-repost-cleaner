<p align="center"><img src="icons/icon128.png" width="96" alt=""></p>

# TikTok Repost Cleaner

[English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md) · [العربية](README.ar.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · **Português (BR)** · [日本語](README.ja.md) · [한국어](README.ko.md) · [Türkçe](README.tr.md)

Uma extensão de navegador que remove seus reposts do TikTok com um clique — todos ou só os mais recentes.

- **Rápida.** A lista de reposts é lida várias páginas de uma vez, e os reposts são removidos por dezenas de solicitações em paralelo. A remoção começa enquanto a lista ainda está sendo lida.
- **Todos ou os N mais recentes.** Apague tudo ou digite quantos dos reposts mais recentes remover.
- **Três velocidades:** Cuidadoso, Normal e Rápido.
- **Progresso ao vivo** na página do TikTok: contador, velocidade por segundo e botão Parar.
- **11 idiomas.** A extensão segue o idioma do seu navegador.
- Funciona no **Chrome, Edge, Brave, Opera, Arc, Yandex Browser** e outros navegadores Chromium.

## Instalação

1. Baixe `tiktok-repost-cleaner-*.zip` na [versão mais recente](https://github.com/tedovy/tiktok-repost-cleaner/releases/latest).
2. Descompacte o arquivo.
3. Abra `chrome://extensions` (Edge: `edge://extensions`, Yandex: `browser://extensions`).
4. Ative o **Modo do desenvolvedor**.
5. Clique em **Carregar sem compactação** e escolha a pasta descompactada.
6. Fixe a extensão na barra de ferramentas (ícone de quebra-cabeça → alfinete).

## Como usar

1. Entre no TikTok neste navegador.
2. Clique no ícone da extensão.
3. Escolha **Todos** ou **Recentes…** e digite quantos.
4. Clique em **Remover**. Seu perfil abre e a remoção começa na hora; um painel no canto mostra o progresso. Mantenha a aba aberta até aparecer **Pronto**.
5. Clique em **Atualizar página** para ver seus reposts atualizados.

## Velocidade e limites do TikTok

| Modo | Páginas da lista ao mesmo tempo | Remoções ao mesmo tempo |
|---|---|---|
| Cuidadoso | 1 | 3 |
| Normal | 4 | 16 |
| Rápido | 8 | 48 |

Remover é leve para o TikTok, mas a lista de reposts é pesada, e o TikTok a limita temporariamente para a conta inteira quando é pedida com muita frequência (por um tempo, até a aba Reposts do site fica vazia). Se isso acontecer, a extensão pausa e tenta de novo; se o limite não sair, ela para e mostra quantos reposts foram removidos. Espere alguns minutos e clique no botão de novo — ela simplesmente continua com o que falta.

## Como funciona

A extensão não fica clicando pelo site. A partir da sua aba aberta do TikTok, ela envia as mesmas solicitações que o site do TikTok envia:

- `GET /api/repost/item_list/` — sua lista de reposts, 30 por página;
- `POST /tiktok/v1/upvote/delete?item_id=…` — a mesma solicitação do botão **Remover repost**.

Nada é enviado para lugar nenhum além do próprio TikTok. A extensão não coleta dados e não lê suas senhas nem cookies.

## Permissões

- `tiktok.com` — para rodar dentro da aba do TikTok;
- `scripting` — para iniciar a limpeza nessa aba;
- `tabs` — para abrir seu perfil;
- `storage` — para lembrar suas configurações.

## Aviso

Sem vínculo com o TikTok ou a ByteDance. A extensão usa endpoints web não oficiais do TikTok, que podem mudar a qualquer momento. Reposts removidos não podem ser restaurados automaticamente. Use por sua conta e risco.

## Licença

MIT — veja [LICENSE](LICENSE).
