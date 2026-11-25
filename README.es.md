<p align="center"><img src="icons/icon128.png" width="96" alt=""></p>

# TikTok Repost Cleaner

[English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md) · [العربية](README.ar.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · **Español** · [Português (BR)](README.pt-BR.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Türkçe](README.tr.md)

Una extensión de navegador que elimina tus reposts de TikTok con un clic: todos o solo los más recientes.

- **Rápida.** La lista de reposts se lee varias páginas a la vez y los reposts se eliminan con decenas de solicitudes en paralelo. La eliminación empieza mientras la lista aún se está leyendo.
- **Todos o los N más recientes.** Borra todo o escribe cuántos de los reposts más recientes quieres eliminar.
- **Tres velocidades:** Con cuidado, Normal y Rápido.
- **Progreso en directo** en la página de TikTok: contador, velocidad por segundo y botón Detener.
- **11 idiomas.** La extensión usa el idioma de tu navegador.
- Funciona en **Chrome, Edge, Brave, Opera, Arc, Yandex Browser** y otros navegadores Chromium.

## Instalación

1. Descarga `tiktok-repost-cleaner-*.zip` desde la [última versión](https://github.com/tedovy/tiktok-repost-cleaner/releases/latest).
2. Descomprímelo.
3. Abre `chrome://extensions` (Edge: `edge://extensions`, Yandex: `browser://extensions`).
4. Activa el **Modo de desarrollador**.
5. Pulsa **Cargar descomprimida** y elige la carpeta descomprimida.
6. Fija la extensión en la barra de herramientas (icono de pieza de puzle → chincheta).

## Cómo se usa

1. Inicia sesión en TikTok en este navegador.
2. Pulsa el icono de la extensión.
3. Elige **Todos** o **Recientes…** y escribe cuántos.
4. Pulsa **Eliminar**. Se abre tu perfil y la eliminación empieza al instante; un panel en la esquina muestra el progreso. Deja la pestaña abierta hasta que aparezca **¡Listo!**.
5. Pulsa **Actualizar página** para ver tus reposts actualizados.

## Velocidad y límites de TikTok

| Modo | Páginas de lista a la vez | Eliminaciones a la vez |
|---|---|---|
| Con cuidado | 1 | 3 |
| Normal | 4 | 16 |
| Rápido | 8 | 48 |

Eliminar es ligero para TikTok, pero la lista de reposts es pesada, y TikTok la limita temporalmente para toda la cuenta si se pide con demasiada frecuencia (durante un rato, incluso la pestaña de reposts del sitio aparece vacía). Si pasa, la extensión hace una pausa y lo vuelve a intentar; si el límite no se levanta, se detiene y te dice cuántos reposts eliminó. Espera unos minutos y vuelve a pulsar el botón: simplemente continuará con los que quedan.

## Cómo funciona

La extensión no hace clic por el sitio. Desde tu pestaña de TikTok abierta envía las mismas solicitudes que envía la web de TikTok:

- `GET /api/repost/item_list/` — tu lista de reposts, 30 por página;
- `POST /tiktok/v1/upvote/delete?item_id=…` — la misma solicitud que el botón **Eliminar repost**.

No se envía nada a ningún sitio salvo a TikTok. La extensión no recopila datos ni lee tus contraseñas o cookies.

## Permisos

- `tiktok.com` — para funcionar dentro de la pestaña de TikTok;
- `scripting` — para iniciar la limpieza en esa pestaña;
- `tabs` — para abrir tu perfil;
- `storage` — para recordar tus ajustes.

## Aviso

Sin relación con TikTok ni ByteDance. La extensión usa puntos de acceso web no oficiales de TikTok, que pueden cambiar en cualquier momento. Los reposts eliminados no se pueden restaurar automáticamente. Úsala bajo tu propia responsabilidad.

## Licencia

MIT — consulta [LICENSE](LICENSE).
