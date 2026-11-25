#!/usr/bin/env python3
"""Generates README.md (English) and README.<lang>.md from one table. Run: python3 tools/readmes.py"""
import os

REPO = "tedovy/tiktok-repost-cleaner"
RELEASES = f"https://github.com/{REPO}/releases/latest"

LANGS = [
    ("en", "README.md", "English"),
    ("ru", "README.ru.md", "Русский"),
    ("zh-CN", "README.zh-CN.md", "简体中文"),
    ("ar", "README.ar.md", "العربية"),
    ("de", "README.de.md", "Deutsch"),
    ("fr", "README.fr.md", "Français"),
    ("es", "README.es.md", "Español"),
    ("pt-BR", "README.pt-BR.md", "Português (BR)"),
    ("ja", "README.ja.md", "日本語"),
    ("ko", "README.ko.md", "한국어"),
    ("tr", "README.tr.md", "Türkçe"),
]

T = {
    "en": dict(
        tagline="A browser extension that removes your TikTok reposts in one click — all of them, or only the latest few.",
        features=[
            "**Fast.** The repost list is read many pages at a time, and reposts are removed by dozens of parallel requests. Removing starts while the list is still being read.",
            "**All or latest N.** Clear everything, or type how many of the newest reposts to remove.",
            "**Three speeds:** Careful, Normal and Fast.",
            "**Live progress** on the TikTok page: counter, speed per second and a Stop button.",
            "**11 languages.** The extension follows your browser language.",
            "Works in **Chrome, Edge, Brave, Opera, Arc, Yandex Browser** and other Chromium browsers.",
        ],
        h_install="Install",
        install=[
            "Download `tiktok-repost-cleaner-*.zip` from the [latest release]({releases}).",
            "Unzip it.",
            "Open `chrome://extensions` (Edge: `edge://extensions`, Yandex: `browser://extensions`).",
            "Turn on **Developer mode**.",
            "Click **Load unpacked** and choose the unzipped folder.",
            "Pin the extension to the toolbar (puzzle icon → pin).",
        ],
        h_use="How to use",
        use=[
            "Log in to TikTok in this browser.",
            "Click the extension icon.",
            "Choose **All** or **Latest…** and type how many.",
            "Press **Remove**. Your profile opens and removal starts right away; a panel in the corner shows progress. Keep the tab open until it says **Done**.",
            "Press **Refresh page** to see your updated reposts.",
        ],
        h_speed="Speed and TikTok limits",
        speed_cols=("Mode", "List pages at once", "Removals at once"),
        speed_note="Removing is quick for TikTok, but the repost list is heavy, and TikTok temporarily limits it for the whole account when it's requested too often (for a while even the Reposts tab on the site stays empty). If that happens, the extension pauses and retries; if the limit doesn't lift, it stops and tells you how many reposts were removed. Wait a few minutes and press the button again — it simply continues with what's left.",
        h_how="How it works",
        how="The extension doesn't click through the site. From your open TikTok tab it sends the same requests the TikTok website sends:",
        how_list=[
            "`GET /api/repost/item_list/` — your repost list, 30 per page;",
            "`POST /tiktok/v1/upvote/delete?item_id=…` — the same request as the **Remove repost** button.",
        ],
        privacy="Nothing is sent anywhere except TikTok. The extension collects no data and doesn't read your passwords or cookies.",
        h_perms="Permissions",
        perms=[
            "`tiktok.com` — to run inside the TikTok tab;",
            "`scripting` — to start the cleaner in that tab;",
            "`tabs` — to open your profile;",
            "`storage` — to remember your settings.",
        ],
        h_disclaimer="Disclaimer",
        disclaimer="Not affiliated with TikTok or ByteDance. The extension uses TikTok's unofficial web endpoints, which can change at any time. Removed reposts can't be restored automatically. Use at your own risk.",
        h_license="License",
        license="MIT — see [LICENSE](LICENSE).",
    ),
    "ru": dict(
        tagline="Расширение для браузера, которое в один клик удаляет твои репосты в TikTok — все или только последние.",
        features=[
            "**Быстро.** Список репостов читается сразу по многу страниц, а удаление идёт десятками параллельных запросов. Удалять начинает, пока список ещё читается.",
            "**Все или последние N.** Можно очистить всё или вписать, сколько последних репостов удалить.",
            "**Три скорости:** Осторожно, Обычно и Быстро.",
            "**Прогресс прямо на странице TikTok:** счётчик, скорость в секунду и кнопка «Остановить».",
            "**11 языков.** Расширение говорит на языке твоего браузера.",
            "Работает в **Chrome, Edge, Brave, Opera, Arc, Яндекс Браузере** и других браузерах на Chromium.",
        ],
        h_install="Установка",
        install=[
            "Скачай `tiktok-repost-cleaner-*.zip` из [последнего релиза]({releases}).",
            "Распакуй архив.",
            "Открой `chrome://extensions` (Edge: `edge://extensions`, Яндекс: `browser://extensions`).",
            "Включи **Режим разработчика**.",
            "Нажми **Загрузить распакованное расширение** и выбери распакованную папку.",
            "Закрепи иконку на панели (значок пазла → булавка).",
        ],
        h_use="Как пользоваться",
        use=[
            "Войди в TikTok в этом браузере.",
            "Нажми на иконку расширения.",
            "Выбери **Все** или **Последние…** и впиши, сколько.",
            "Нажми **Удалить**. Откроется твой профиль, и удаление сразу начнётся; в углу появится панель с прогрессом. Не закрывай вкладку, пока не появится **Готово**.",
            "Нажми **Обновить страницу**, чтобы увидеть актуальный список репостов.",
        ],
        h_speed="Скорость и ограничения TikTok",
        speed_cols=("Режим", "Страниц списка сразу", "Удалений сразу"),
        speed_note="Удаление TikTok выдерживает легко, а вот список репостов тяжёлый, и при слишком частых запросах TikTok временно ограничивает его для всего аккаунта (какое-то время даже вкладка «Репосты» на сайте будет пустой). Если так случится, расширение подождёт и повторит; если ограничение не снимется, оно остановится и напишет, сколько успело удалить. Подожди несколько минут и нажми кнопку ещё раз — оно просто продолжит с оставшимися.",
        h_how="Как это работает",
        how="Расширение не кликает по сайту. Из твоей открытой вкладки TikTok оно отправляет те же запросы, что и сам сайт:",
        how_list=[
            "`GET /api/repost/item_list/` — список репостов, по 30 на страницу;",
            "`POST /tiktok/v1/upvote/delete?item_id=…` — тот же запрос, что и кнопка **Удалить репост**.",
        ],
        privacy="Ничего никуда не отправляется, кроме самого TikTok. Расширение не собирает данные и не читает пароли и куки.",
        h_perms="Разрешения",
        perms=[
            "`tiktok.com` — чтобы работать во вкладке TikTok;",
            "`scripting` — чтобы запустить удаление в этой вкладке;",
            "`tabs` — чтобы открыть твой профиль;",
            "`storage` — чтобы запомнить настройки.",
        ],
        h_disclaimer="Отказ от ответственности",
        disclaimer="Проект не связан с TikTok и ByteDance. Расширение использует неофициальные веб-запросы TikTok, которые могут измениться в любой момент. Удалённые репосты нельзя вернуть автоматически. Используй на свой риск.",
        h_license="Лицензия",
        license="MIT — см. [LICENSE](LICENSE).",
    ),
    "zh-CN": dict(
        tagline="一个浏览器扩展，一键删除你在 TikTok 上的转发——全部删除，或只删除最近几条。",
        features=[
            "**速度快。** 一次并行读取多页转发列表，并用数十个并行请求删除转发。列表还在读取时就已开始删除。",
            "**全部或最近 N 条。** 可以全部清空，也可以输入要删除的最近转发数量。",
            "**三种速度：** 谨慎、正常、快速。",
            "**在 TikTok 页面上实时显示进度：** 计数、每秒速度和“停止”按钮。",
            "**11 种语言。** 扩展会跟随你的浏览器语言。",
            "支持 **Chrome、Edge、Brave、Opera、Arc、Yandex 浏览器** 以及其他基于 Chromium 的浏览器。",
        ],
        h_install="安装",
        install=[
            "从[最新发布]({releases})下载 `tiktok-repost-cleaner-*.zip`。",
            "解压。",
            "打开 `chrome://extensions`（Edge：`edge://extensions`，Yandex：`browser://extensions`）。",
            "开启 **开发者模式**。",
            "点击 **加载已解压的扩展程序**，选择解压后的文件夹。",
            "把扩展固定到工具栏（拼图图标 → 图钉）。",
        ],
        h_use="使用方法",
        use=[
            "在此浏览器中登录 TikTok。",
            "点击扩展图标。",
            "选择 **全部** 或 **最近…** 并输入数量。",
            "点击 **删除**。会打开你的主页并立即开始删除，角落里的面板显示进度。在显示 **完成** 之前不要关闭标签页。",
            "点击 **刷新页面** 查看更新后的转发列表。",
        ],
        h_speed="速度与 TikTok 的限制",
        speed_cols=("模式", "同时读取的列表页数", "同时删除的数量"),
        speed_note="删除操作对 TikTok 来说很轻松，但转发列表很大。请求过于频繁时，TikTok 会对整个账号暂时限制该列表（一段时间内网站上的“转发”标签页也会是空的）。遇到这种情况，扩展会暂停并重试；如果限制一直不解除，它会停止并告诉你已删除多少条。等几分钟再点一次按钮即可，它会继续处理剩下的转发。",
        h_how="工作原理",
        how="扩展不会在网页上模拟点击。它在你打开的 TikTok 标签页中发送与 TikTok 网站相同的请求：",
        how_list=[
            "`GET /api/repost/item_list/` —— 你的转发列表，每页 30 条；",
            "`POST /tiktok/v1/upvote/delete?item_id=…` —— 与 **删除转发** 按钮相同的请求。",
        ],
        privacy="除了 TikTok 本身，不会向任何地方发送数据。扩展不收集任何数据，也不读取你的密码或 Cookie。",
        h_perms="权限",
        perms=[
            "`tiktok.com` —— 在 TikTok 标签页中运行；",
            "`scripting` —— 在该标签页中启动清理；",
            "`tabs` —— 打开你的主页；",
            "`storage` —— 记住你的设置。",
        ],
        h_disclaimer="免责声明",
        disclaimer="本项目与 TikTok 或字节跳动无关。扩展使用 TikTok 非官方的网页接口，这些接口随时可能变化。删除的转发无法自动恢复。使用风险自负。",
        h_license="许可证",
        license="MIT —— 见 [LICENSE](LICENSE)。",
    ),
    "ar": dict(
        tagline="إضافة للمتصفح تحذف إعادات النشر في TikTok بنقرة واحدة — كلها، أو الأحدث منها فقط.",
        features=[
            "**سريعة.** تُقرأ قائمة إعادات النشر عدة صفحات في وقت واحد، وتُحذف إعادات النشر بعشرات الطلبات المتوازية. يبدأ الحذف بينما لا تزال القائمة تُقرأ.",
            "**الكل أو أحدث N.** احذف كل شيء، أو اكتب عدد أحدث إعادات النشر التي تريد حذفها.",
            "**ثلاث سرعات:** بحذر، عادي، سريع.",
            "**تقدّم مباشر** على صفحة TikTok: عدّاد، وسرعة في الثانية، وزر إيقاف.",
            "**11 لغة.** تتبع الإضافة لغة متصفحك.",
            "تعمل في **Chrome وEdge وBrave وOpera وArc ومتصفح Yandex** وغيرها من متصفحات Chromium.",
        ],
        h_install="التثبيت",
        install=[
            "نزّل `tiktok-repost-cleaner-*.zip` من [أحدث إصدار]({releases}).",
            "فك ضغط الملف.",
            "افتح `chrome://extensions` (في Edge: `edge://extensions`، وفي Yandex: `browser://extensions`).",
            "فعّل **وضع المطوّر**.",
            "اضغط **تحميل إضافة غير مضغوطة** واختر المجلد الذي فككت ضغطه.",
            "ثبّت الإضافة في شريط الأدوات (أيقونة قطعة الأحجية ← الدبوس).",
        ],
        h_use="طريقة الاستخدام",
        use=[
            "سجّل الدخول إلى TikTok في هذا المتصفح.",
            "اضغط على أيقونة الإضافة.",
            "اختر **الكل** أو **الأحدث…** واكتب العدد.",
            "اضغط **حذف**. سيُفتح ملفك الشخصي ويبدأ الحذف فورًا، وتعرض لوحة في الزاوية التقدّم. لا تغلق التبويب حتى تظهر عبارة **تم**.",
            "اضغط **تحديث الصفحة** لترى قائمة إعادات النشر المحدّثة.",
        ],
        h_speed="السرعة وقيود TikTok",
        speed_cols=("الوضع", "صفحات القائمة في وقت واحد", "عمليات الحذف في وقت واحد"),
        speed_note="الحذف سهل على TikTok، لكن قائمة إعادات النشر ثقيلة، ويقيّدها TikTok مؤقتًا للحساب كله عند طلبها كثيرًا (ولفترة تبقى حتى علامة تبويب إعادات النشر على الموقع فارغة). إذا حدث ذلك، تتوقف الإضافة قليلًا ثم تعيد المحاولة؛ وإذا لم يُرفع القيد، تتوقف وتخبرك بعدد ما حُذف. انتظر بضع دقائق واضغط الزر مرة أخرى — وستكمل ببساطة ما تبقى.",
        h_how="كيف تعمل",
        how="لا تنقر الإضافة على عناصر الموقع. بل ترسل من تبويب TikTok المفتوح لديك الطلبات نفسها التي يرسلها موقع TikTok:",
        how_list=[
            "`GET /api/repost/item_list/` — قائمة إعادات النشر، 30 في كل صفحة؛",
            "`POST /tiktok/v1/upvote/delete?item_id=…` — الطلب نفسه الذي يرسله زر **حذف إعادة النشر**.",
        ],
        privacy="لا يُرسل أي شيء إلى أي مكان سوى TikTok. لا تجمع الإضافة أي بيانات ولا تقرأ كلمات مرورك أو ملفات تعريف الارتباط.",
        h_perms="الأذونات",
        perms=[
            "`tiktok.com` — للعمل داخل تبويب TikTok؛",
            "`scripting` — لتشغيل الحذف في ذلك التبويب؛",
            "`tabs` — لفتح ملفك الشخصي؛",
            "`storage` — لتذكّر إعداداتك.",
        ],
        h_disclaimer="إخلاء المسؤولية",
        disclaimer="هذا المشروع غير تابع لـ TikTok أو ByteDance. تستخدم الإضافة واجهات ويب غير رسمية من TikTok قد تتغير في أي وقت. لا يمكن استعادة إعادات النشر المحذوفة تلقائيًا. الاستخدام على مسؤوليتك.",
        h_license="الترخيص",
        license="MIT — راجع [LICENSE](LICENSE).",
    ),
    "de": dict(
        tagline="Eine Browser-Erweiterung, die deine TikTok-Reposts mit einem Klick entfernt – alle oder nur die neuesten.",
        features=[
            "**Schnell.** Die Repost-Liste wird seitenweise parallel gelesen, und Reposts werden mit Dutzenden parallelen Anfragen entfernt. Das Entfernen beginnt schon, während die Liste noch gelesen wird.",
            "**Alle oder die neuesten N.** Alles löschen oder eingeben, wie viele der neuesten Reposts entfernt werden sollen.",
            "**Drei Tempi:** Vorsichtig, Normal und Schnell.",
            "**Live-Fortschritt** auf der TikTok-Seite: Zähler, Tempo pro Sekunde und ein Stopp-Button.",
            "**11 Sprachen.** Die Erweiterung folgt der Sprache deines Browsers.",
            "Funktioniert in **Chrome, Edge, Brave, Opera, Arc, Yandex Browser** und anderen Chromium-Browsern.",
        ],
        h_install="Installation",
        install=[
            "Lade `tiktok-repost-cleaner-*.zip` aus dem [neuesten Release]({releases}) herunter.",
            "Entpacke die Datei.",
            "Öffne `chrome://extensions` (Edge: `edge://extensions`, Yandex: `browser://extensions`).",
            "Aktiviere den **Entwicklermodus**.",
            "Klicke auf **Entpackte Erweiterung laden** und wähle den entpackten Ordner.",
            "Hefte die Erweiterung an die Symbolleiste an (Puzzle-Symbol → Pin).",
        ],
        h_use="Benutzung",
        use=[
            "Melde dich in diesem Browser bei TikTok an.",
            "Klicke auf das Symbol der Erweiterung.",
            "Wähle **Alle** oder **Neueste…** und gib die Anzahl ein.",
            "Klicke auf **Entfernen**. Dein Profil öffnet sich und das Entfernen startet sofort; ein Panel in der Ecke zeigt den Fortschritt. Lass den Tab offen, bis **Fertig** erscheint.",
            "Klicke auf **Seite neu laden**, um deine aktualisierten Reposts zu sehen.",
        ],
        h_speed="Tempo und TikTok-Limits",
        speed_cols=("Modus", "Listenseiten gleichzeitig", "Entfernungen gleichzeitig"),
        speed_note="Das Entfernen ist für TikTok leicht, die Repost-Liste dagegen ist schwer, und TikTok begrenzt sie vorübergehend für das ganze Konto, wenn sie zu oft abgefragt wird (eine Weile bleibt dann sogar der Reposts-Tab auf der Website leer). Passiert das, pausiert die Erweiterung und versucht es erneut; hebt sich das Limit nicht, hält sie an und zeigt, wie viele Reposts entfernt wurden. Warte ein paar Minuten und klicke erneut – sie macht einfach mit dem Rest weiter.",
        h_how="So funktioniert es",
        how="Die Erweiterung klickt sich nicht durch die Website. Aus deinem geöffneten TikTok-Tab sendet sie dieselben Anfragen wie die TikTok-Website:",
        how_list=[
            "`GET /api/repost/item_list/` – deine Repost-Liste, 30 pro Seite;",
            "`POST /tiktok/v1/upvote/delete?item_id=…` – dieselbe Anfrage wie der Button **Repost entfernen**.",
        ],
        privacy="Es wird nichts an andere Stellen als TikTok gesendet. Die Erweiterung sammelt keine Daten und liest weder Passwörter noch Cookies.",
        h_perms="Berechtigungen",
        perms=[
            "`tiktok.com` – um im TikTok-Tab zu laufen;",
            "`scripting` – um das Entfernen in diesem Tab zu starten;",
            "`tabs` – um dein Profil zu öffnen;",
            "`storage` – um deine Einstellungen zu speichern.",
        ],
        h_disclaimer="Haftungsausschluss",
        disclaimer="Kein Bezug zu TikTok oder ByteDance. Die Erweiterung nutzt inoffizielle Web-Schnittstellen von TikTok, die sich jederzeit ändern können. Entfernte Reposts lassen sich nicht automatisch wiederherstellen. Nutzung auf eigenes Risiko.",
        h_license="Lizenz",
        license="MIT – siehe [LICENSE](LICENSE).",
    ),
    "fr": dict(
        tagline="Une extension de navigateur qui supprime tes republications TikTok en un clic — toutes, ou seulement les plus récentes.",
        features=[
            "**Rapide.** La liste des republications est lue plusieurs pages à la fois, et les republications sont supprimées par des dizaines de requêtes en parallèle. La suppression commence pendant que la liste est encore en cours de lecture.",
            "**Toutes ou les N plus récentes.** Tout effacer, ou indiquer combien de republications récentes supprimer.",
            "**Trois vitesses :** Prudent, Normal et Rapide.",
            "**Progression en direct** sur la page TikTok : compteur, vitesse par seconde et bouton Arrêter.",
            "**11 langues.** L'extension suit la langue de ton navigateur.",
            "Fonctionne dans **Chrome, Edge, Brave, Opera, Arc, Yandex Browser** et les autres navigateurs Chromium.",
        ],
        h_install="Installation",
        install=[
            "Télécharge `tiktok-repost-cleaner-*.zip` depuis la [dernière version]({releases}).",
            "Décompresse-le.",
            "Ouvre `chrome://extensions` (Edge : `edge://extensions`, Yandex : `browser://extensions`).",
            "Active le **Mode développeur**.",
            "Clique sur **Charger l'extension non empaquetée** et choisis le dossier décompressé.",
            "Épingle l'extension à la barre d'outils (icône puzzle → épingle).",
        ],
        h_use="Utilisation",
        use=[
            "Connecte-toi à TikTok dans ce navigateur.",
            "Clique sur l'icône de l'extension.",
            "Choisis **Toutes** ou **Récentes…** et indique combien.",
            "Clique sur **Supprimer**. Ton profil s'ouvre et la suppression démarre aussitôt ; un panneau dans le coin affiche la progression. Garde l'onglet ouvert jusqu'à **Terminé**.",
            "Clique sur **Actualiser la page** pour voir tes republications à jour.",
        ],
        h_speed="Vitesse et limites de TikTok",
        speed_cols=("Mode", "Pages de liste à la fois", "Suppressions à la fois"),
        speed_note="Supprimer est léger pour TikTok, mais la liste des republications est lourde, et TikTok la limite temporairement pour tout le compte quand elle est demandée trop souvent (pendant un moment, même l'onglet Republications du site reste vide). Dans ce cas, l'extension fait une pause et réessaie ; si la limite ne se lève pas, elle s'arrête et indique combien de republications ont été supprimées. Attends quelques minutes et appuie de nouveau sur le bouton — elle reprend simplement avec ce qui reste.",
        h_how="Comment ça marche",
        how="L'extension ne clique pas sur le site. Depuis ton onglet TikTok ouvert, elle envoie les mêmes requêtes que le site TikTok :",
        how_list=[
            "`GET /api/repost/item_list/` — ta liste de republications, 30 par page ;",
            "`POST /tiktok/v1/upvote/delete?item_id=…` — la même requête que le bouton **Supprimer la republication**.",
        ],
        privacy="Rien n'est envoyé ailleurs qu'à TikTok. L'extension ne collecte aucune donnée et ne lit ni tes mots de passe ni tes cookies.",
        h_perms="Autorisations",
        perms=[
            "`tiktok.com` — pour fonctionner dans l'onglet TikTok ;",
            "`scripting` — pour lancer la suppression dans cet onglet ;",
            "`tabs` — pour ouvrir ton profil ;",
            "`storage` — pour mémoriser tes réglages.",
        ],
        h_disclaimer="Avertissement",
        disclaimer="Sans lien avec TikTok ni ByteDance. L'extension utilise des points d'accès web non officiels de TikTok, qui peuvent changer à tout moment. Les republications supprimées ne peuvent pas être restaurées automatiquement. À utiliser à tes risques.",
        h_license="Licence",
        license="MIT — voir [LICENSE](LICENSE).",
    ),
    "es": dict(
        tagline="Una extensión de navegador que elimina tus reposts de TikTok con un clic: todos o solo los más recientes.",
        features=[
            "**Rápida.** La lista de reposts se lee varias páginas a la vez y los reposts se eliminan con decenas de solicitudes en paralelo. La eliminación empieza mientras la lista aún se está leyendo.",
            "**Todos o los N más recientes.** Borra todo o escribe cuántos de los reposts más recientes quieres eliminar.",
            "**Tres velocidades:** Con cuidado, Normal y Rápido.",
            "**Progreso en directo** en la página de TikTok: contador, velocidad por segundo y botón Detener.",
            "**11 idiomas.** La extensión usa el idioma de tu navegador.",
            "Funciona en **Chrome, Edge, Brave, Opera, Arc, Yandex Browser** y otros navegadores Chromium.",
        ],
        h_install="Instalación",
        install=[
            "Descarga `tiktok-repost-cleaner-*.zip` desde la [última versión]({releases}).",
            "Descomprímelo.",
            "Abre `chrome://extensions` (Edge: `edge://extensions`, Yandex: `browser://extensions`).",
            "Activa el **Modo de desarrollador**.",
            "Pulsa **Cargar descomprimida** y elige la carpeta descomprimida.",
            "Fija la extensión en la barra de herramientas (icono de pieza de puzle → chincheta).",
        ],
        h_use="Cómo se usa",
        use=[
            "Inicia sesión en TikTok en este navegador.",
            "Pulsa el icono de la extensión.",
            "Elige **Todos** o **Recientes…** y escribe cuántos.",
            "Pulsa **Eliminar**. Se abre tu perfil y la eliminación empieza al instante; un panel en la esquina muestra el progreso. Deja la pestaña abierta hasta que aparezca **¡Listo!**.",
            "Pulsa **Actualizar página** para ver tus reposts actualizados.",
        ],
        h_speed="Velocidad y límites de TikTok",
        speed_cols=("Modo", "Páginas de lista a la vez", "Eliminaciones a la vez"),
        speed_note="Eliminar es ligero para TikTok, pero la lista de reposts es pesada, y TikTok la limita temporalmente para toda la cuenta si se pide con demasiada frecuencia (durante un rato, incluso la pestaña de reposts del sitio aparece vacía). Si pasa, la extensión hace una pausa y lo vuelve a intentar; si el límite no se levanta, se detiene y te dice cuántos reposts eliminó. Espera unos minutos y vuelve a pulsar el botón: simplemente continuará con los que quedan.",
        h_how="Cómo funciona",
        how="La extensión no hace clic por el sitio. Desde tu pestaña de TikTok abierta envía las mismas solicitudes que envía la web de TikTok:",
        how_list=[
            "`GET /api/repost/item_list/` — tu lista de reposts, 30 por página;",
            "`POST /tiktok/v1/upvote/delete?item_id=…` — la misma solicitud que el botón **Eliminar repost**.",
        ],
        privacy="No se envía nada a ningún sitio salvo a TikTok. La extensión no recopila datos ni lee tus contraseñas o cookies.",
        h_perms="Permisos",
        perms=[
            "`tiktok.com` — para funcionar dentro de la pestaña de TikTok;",
            "`scripting` — para iniciar la limpieza en esa pestaña;",
            "`tabs` — para abrir tu perfil;",
            "`storage` — para recordar tus ajustes.",
        ],
        h_disclaimer="Aviso",
        disclaimer="Sin relación con TikTok ni ByteDance. La extensión usa puntos de acceso web no oficiales de TikTok, que pueden cambiar en cualquier momento. Los reposts eliminados no se pueden restaurar automáticamente. Úsala bajo tu propia responsabilidad.",
        h_license="Licencia",
        license="MIT — consulta [LICENSE](LICENSE).",
    ),
    "pt-BR": dict(
        tagline="Uma extensão de navegador que remove seus reposts do TikTok com um clique — todos ou só os mais recentes.",
        features=[
            "**Rápida.** A lista de reposts é lida várias páginas de uma vez, e os reposts são removidos por dezenas de solicitações em paralelo. A remoção começa enquanto a lista ainda está sendo lida.",
            "**Todos ou os N mais recentes.** Apague tudo ou digite quantos dos reposts mais recentes remover.",
            "**Três velocidades:** Cuidadoso, Normal e Rápido.",
            "**Progresso ao vivo** na página do TikTok: contador, velocidade por segundo e botão Parar.",
            "**11 idiomas.** A extensão segue o idioma do seu navegador.",
            "Funciona no **Chrome, Edge, Brave, Opera, Arc, Yandex Browser** e outros navegadores Chromium.",
        ],
        h_install="Instalação",
        install=[
            "Baixe `tiktok-repost-cleaner-*.zip` na [versão mais recente]({releases}).",
            "Descompacte o arquivo.",
            "Abra `chrome://extensions` (Edge: `edge://extensions`, Yandex: `browser://extensions`).",
            "Ative o **Modo do desenvolvedor**.",
            "Clique em **Carregar sem compactação** e escolha a pasta descompactada.",
            "Fixe a extensão na barra de ferramentas (ícone de quebra-cabeça → alfinete).",
        ],
        h_use="Como usar",
        use=[
            "Entre no TikTok neste navegador.",
            "Clique no ícone da extensão.",
            "Escolha **Todos** ou **Recentes…** e digite quantos.",
            "Clique em **Remover**. Seu perfil abre e a remoção começa na hora; um painel no canto mostra o progresso. Mantenha a aba aberta até aparecer **Pronto**.",
            "Clique em **Atualizar página** para ver seus reposts atualizados.",
        ],
        h_speed="Velocidade e limites do TikTok",
        speed_cols=("Modo", "Páginas da lista ao mesmo tempo", "Remoções ao mesmo tempo"),
        speed_note="Remover é leve para o TikTok, mas a lista de reposts é pesada, e o TikTok a limita temporariamente para a conta inteira quando é pedida com muita frequência (por um tempo, até a aba Reposts do site fica vazia). Se isso acontecer, a extensão pausa e tenta de novo; se o limite não sair, ela para e mostra quantos reposts foram removidos. Espere alguns minutos e clique no botão de novo — ela simplesmente continua com o que falta.",
        h_how="Como funciona",
        how="A extensão não fica clicando pelo site. A partir da sua aba aberta do TikTok, ela envia as mesmas solicitações que o site do TikTok envia:",
        how_list=[
            "`GET /api/repost/item_list/` — sua lista de reposts, 30 por página;",
            "`POST /tiktok/v1/upvote/delete?item_id=…` — a mesma solicitação do botão **Remover repost**.",
        ],
        privacy="Nada é enviado para lugar nenhum além do próprio TikTok. A extensão não coleta dados e não lê suas senhas nem cookies.",
        h_perms="Permissões",
        perms=[
            "`tiktok.com` — para rodar dentro da aba do TikTok;",
            "`scripting` — para iniciar a limpeza nessa aba;",
            "`tabs` — para abrir seu perfil;",
            "`storage` — para lembrar suas configurações.",
        ],
        h_disclaimer="Aviso",
        disclaimer="Sem vínculo com o TikTok ou a ByteDance. A extensão usa endpoints web não oficiais do TikTok, que podem mudar a qualquer momento. Reposts removidos não podem ser restaurados automaticamente. Use por sua conta e risco.",
        h_license="Licença",
        license="MIT — veja [LICENSE](LICENSE).",
    ),
    "ja": dict(
        tagline="TikTok のリポストをワンクリックで削除するブラウザ拡張機能です。すべて、または最新のものだけを削除できます。",
        features=[
            "**高速。** リポスト一覧を複数ページ同時に読み込み、数十件の並列リクエストで削除します。一覧の読み込み中から削除が始まります。",
            "**すべて、または最新 N 件。** 全部消すことも、削除する最新リポストの数を指定することもできます。",
            "**3 段階の速度：** 慎重・標準・高速。",
            "**TikTok のページ上でリアルタイムに進捗を表示：** カウンター、1 秒あたりの件数、停止ボタン。",
            "**11 言語対応。** ブラウザの言語に合わせて表示されます。",
            "**Chrome、Edge、Brave、Opera、Arc、Yandex Browser** など Chromium 系ブラウザで動作します。",
        ],
        h_install="インストール",
        install=[
            "[最新リリース]({releases})から `tiktok-repost-cleaner-*.zip` をダウンロードします。",
            "解凍します。",
            "`chrome://extensions` を開きます（Edge：`edge://extensions`、Yandex：`browser://extensions`）。",
            "**デベロッパー モード** をオンにします。",
            "**パッケージ化されていない拡張機能を読み込む** をクリックし、解凍したフォルダを選びます。",
            "拡張機能をツールバーに固定します（パズルアイコン → ピン）。",
        ],
        h_use="使い方",
        use=[
            "このブラウザで TikTok にログインします。",
            "拡張機能のアイコンをクリックします。",
            "**すべて** または **最新…** を選び、件数を入力します。",
            "**削除** を押します。プロフィールが開き、すぐに削除が始まります。隅のパネルに進捗が表示されます。**完了** と表示されるまでタブを閉じないでください。",
            "**ページを再読み込み** を押すと、更新されたリポスト一覧が表示されます。",
        ],
        h_speed="速度と TikTok の制限",
        speed_cols=("モード", "同時に読む一覧ページ数", "同時に削除する件数"),
        speed_note="削除は TikTok にとって軽い処理ですが、リポスト一覧は重く、頻繁にリクエストするとアカウント全体で一時的に制限されます（しばらくはサイトのリポストタブも空になります）。その場合、拡張機能は一時停止して再試行します。制限が解除されなければ停止し、削除できた件数を表示します。数分待ってからもう一度ボタンを押せば、残りの削除を続けます。",
        h_how="仕組み",
        how="拡張機能はサイト上でクリック操作をしません。開いている TikTok のタブから、TikTok のサイトと同じリクエストを送ります：",
        how_list=[
            "`GET /api/repost/item_list/` — リポスト一覧（1 ページ 30 件）；",
            "`POST /tiktok/v1/upvote/delete?item_id=…` — **リポストを削除** ボタンと同じリクエスト。",
        ],
        privacy="TikTok 以外にはどこにも送信しません。拡張機能はデータを収集せず、パスワードや Cookie も読みません。",
        h_perms="権限",
        perms=[
            "`tiktok.com` — TikTok のタブ内で動作するため；",
            "`scripting` — そのタブで削除を開始するため；",
            "`tabs` — プロフィールを開くため；",
            "`storage` — 設定を保存するため。",
        ],
        h_disclaimer="免責事項",
        disclaimer="TikTok および ByteDance とは無関係です。この拡張機能は TikTok の非公式なウェブ API を使用しており、仕様はいつでも変わる可能性があります。削除したリポストは自動では元に戻せません。自己責任でご利用ください。",
        h_license="ライセンス",
        license="MIT — [LICENSE](LICENSE) を参照してください。",
    ),
    "ko": dict(
        tagline="TikTok 리포스트를 클릭 한 번으로 삭제하는 브라우저 확장 프로그램입니다. 전부 또는 최근 것만 삭제할 수 있어요.",
        features=[
            "**빠름.** 리포스트 목록을 여러 페이지씩 동시에 읽고, 수십 개의 병렬 요청으로 삭제합니다. 목록을 읽는 동안 이미 삭제가 시작됩니다.",
            "**전체 또는 최근 N개.** 전부 지우거나, 삭제할 최근 리포스트 개수를 입력하세요.",
            "**세 가지 속도:** 신중하게, 보통, 빠르게.",
            "**TikTok 페이지에서 실시간 진행 상황:** 카운터, 초당 속도, 중지 버튼.",
            "**11개 언어.** 브라우저 언어에 맞춰 표시됩니다.",
            "**Chrome, Edge, Brave, Opera, Arc, Yandex Browser** 등 Chromium 기반 브라우저에서 작동합니다.",
        ],
        h_install="설치",
        install=[
            "[최신 릴리스]({releases})에서 `tiktok-repost-cleaner-*.zip`을 내려받으세요.",
            "압축을 푸세요.",
            "`chrome://extensions`를 여세요 (Edge: `edge://extensions`, Yandex: `browser://extensions`).",
            "**개발자 모드**를 켜세요.",
            "**압축해제된 확장 프로그램을 로드합니다**를 누르고 압축을 푼 폴더를 선택하세요.",
            "확장 프로그램을 툴바에 고정하세요 (퍼즐 아이콘 → 핀).",
        ],
        h_use="사용 방법",
        use=[
            "이 브라우저에서 TikTok에 로그인하세요.",
            "확장 프로그램 아이콘을 누르세요.",
            "**전체** 또는 **최근…**을 고르고 개수를 입력하세요.",
            "**삭제**를 누르세요. 프로필이 열리고 바로 삭제가 시작되며, 구석의 패널에 진행 상황이 표시됩니다. **완료**가 나올 때까지 탭을 닫지 마세요.",
            "**페이지 새로고침**을 누르면 업데이트된 리포스트 목록을 볼 수 있어요.",
        ],
        h_speed="속도와 TikTok 제한",
        speed_cols=("모드", "동시에 읽는 목록 페이지", "동시에 삭제하는 개수"),
        speed_note="삭제는 TikTok에 부담이 적지만 리포스트 목록은 무거워서, 너무 자주 요청하면 TikTok이 계정 전체에 대해 일시적으로 제한합니다 (한동안 사이트의 리포스트 탭도 비어 보여요). 이럴 때 확장 프로그램은 잠시 멈췄다가 다시 시도하고, 제한이 풀리지 않으면 멈추고 삭제한 개수를 알려줍니다. 몇 분 기다린 뒤 버튼을 다시 누르면 남은 것부터 이어서 진행합니다.",
        h_how="작동 방식",
        how="확장 프로그램은 사이트를 클릭하지 않습니다. 열려 있는 TikTok 탭에서 TikTok 웹사이트와 같은 요청을 보냅니다:",
        how_list=[
            "`GET /api/repost/item_list/` — 리포스트 목록, 페이지당 30개;",
            "`POST /tiktok/v1/upvote/delete?item_id=…` — **리포스트 삭제** 버튼과 같은 요청.",
        ],
        privacy="TikTok 외에는 어디에도 데이터를 보내지 않습니다. 확장 프로그램은 데이터를 수집하지 않으며 비밀번호나 쿠키를 읽지 않습니다.",
        h_perms="권한",
        perms=[
            "`tiktok.com` — TikTok 탭 안에서 실행하기 위해;",
            "`scripting` — 그 탭에서 삭제를 시작하기 위해;",
            "`tabs` — 프로필을 열기 위해;",
            "`storage` — 설정을 기억하기 위해.",
        ],
        h_disclaimer="면책 조항",
        disclaimer="TikTok 또는 ByteDance와 관련이 없습니다. 이 확장 프로그램은 언제든 바뀔 수 있는 TikTok의 비공식 웹 API를 사용합니다. 삭제한 리포스트는 자동으로 복구할 수 없습니다. 사용에 따른 책임은 본인에게 있습니다.",
        h_license="라이선스",
        license="MIT — [LICENSE](LICENSE)를 참고하세요.",
    ),
    "tr": dict(
        tagline="TikTok repostlarını tek tıkla silen bir tarayıcı eklentisi — hepsini ya da yalnızca en yenilerini.",
        features=[
            "**Hızlı.** Repost listesi aynı anda birçok sayfa halinde okunur ve repostlar onlarca paralel istekle silinir. Liste okunurken silme işlemi zaten başlar.",
            "**Tümü ya da en yeni N tane.** Hepsini temizle ya da en yeni kaç repostun silineceğini yaz.",
            "**Üç hız:** Dikkatli, Normal ve Hızlı.",
            "**TikTok sayfasında canlı ilerleme:** sayaç, saniye başına hız ve Durdur düğmesi.",
            "**11 dil.** Eklenti tarayıcının dilini kullanır.",
            "**Chrome, Edge, Brave, Opera, Arc, Yandex Browser** ve diğer Chromium tarayıcılarda çalışır.",
        ],
        h_install="Kurulum",
        install=[
            "[Son sürümden]({releases}) `tiktok-repost-cleaner-*.zip` dosyasını indir.",
            "Arşivi aç.",
            "`chrome://extensions` adresini aç (Edge: `edge://extensions`, Yandex: `browser://extensions`).",
            "**Geliştirici modunu** aç.",
            "**Paketlenmemiş öğe yükle**'ye tıkla ve açtığın klasörü seç.",
            "Eklentiyi araç çubuğuna sabitle (yapboz simgesi → raptiye).",
        ],
        h_use="Kullanım",
        use=[
            "Bu tarayıcıda TikTok'a giriş yap.",
            "Eklenti simgesine tıkla.",
            "**Tümü** ya da **En yeni…** seç ve kaç tane olduğunu yaz.",
            "**Sil**'e bas. Profilin açılır ve silme hemen başlar; köşedeki panel ilerlemeyi gösterir. **Tamam** yazana kadar sekmeyi kapatma.",
            "Güncel repostlarını görmek için **Sayfayı yenile**'ye bas.",
        ],
        h_speed="Hız ve TikTok sınırları",
        speed_cols=("Mod", "Aynı anda liste sayfası", "Aynı anda silme"),
        speed_note="Silme TikTok için hafiftir, ama repost listesi ağırdır ve çok sık istenirse TikTok onu tüm hesap için geçici olarak sınırlar (bir süre sitedeki Repostlar sekmesi bile boş görünür). Böyle olursa eklenti durup yeniden dener; sınır kalkmazsa durur ve kaç repost silindiğini söyler. Birkaç dakika bekleyip düğmeye tekrar bas — kalanlarla devam eder.",
        h_how="Nasıl çalışır",
        how="Eklenti sitede tıklama yapmaz. Açık TikTok sekmenden, TikTok sitesinin gönderdiği isteklerin aynısını gönderir:",
        how_list=[
            "`GET /api/repost/item_list/` — repost listen, sayfa başına 30;",
            "`POST /tiktok/v1/upvote/delete?item_id=…` — **Repostu kaldır** düğmesiyle aynı istek.",
        ],
        privacy="TikTok dışında hiçbir yere bir şey gönderilmez. Eklenti veri toplamaz, şifrelerini ya da çerezlerini okumaz.",
        h_perms="İzinler",
        perms=[
            "`tiktok.com` — TikTok sekmesinde çalışmak için;",
            "`scripting` — o sekmede silmeyi başlatmak için;",
            "`tabs` — profilini açmak için;",
            "`storage` — ayarlarını hatırlamak için.",
        ],
        h_disclaimer="Sorumluluk reddi",
        disclaimer="TikTok veya ByteDance ile bağlantılı değildir. Eklenti, TikTok'un her an değişebilecek resmi olmayan web uç noktalarını kullanır. Silinen repostlar otomatik olarak geri getirilemez. Kullanım riski sana aittir.",
        h_license="Lisans",
        license="MIT — [LICENSE](LICENSE) dosyasına bak.",
    ),
}

# Speed mode names come from the extension's own translations.
SPEED_NAMES = {
    "en": ("Careful", "Normal", "Fast"), "ru": ("Осторожно", "Обычно", "Быстро"),
    "zh-CN": ("谨慎", "正常", "快速"), "ar": ("بحذر", "عادي", "سريع"),
    "de": ("Vorsichtig", "Normal", "Schnell"), "fr": ("Prudent", "Normal", "Rapide"),
    "es": ("Con cuidado", "Normal", "Rápido"), "pt-BR": ("Cuidadoso", "Normal", "Rápido"),
    "ja": ("慎重", "標準", "高速"), "ko": ("신중하게", "보통", "빠르게"), "tr": ("Dikkatli", "Normal", "Hızlı"),
}
SPEED_VALUES = (("1", "3"), ("4", "16"), ("8", "48"))  # keep in sync with SPEEDS in runner.js


def render(code):
    s = T[code]
    langbar = " · ".join(
        f"**{name}**" if c == code else f"[{name}]({fname})" for c, fname, name in LANGS
    )
    out = []
    if code == "ar":
        out.append('<div dir="rtl">\n')
    out.append('<p align="center"><img src="icons/icon128.png" width="96" alt=""></p>\n')
    out.append("# TikTok Repost Cleaner\n")
    out.append(langbar + "\n")
    out.append(s["tagline"] + "\n")
    out += [f"- {f}" for f in s["features"]]
    out.append("")
    out.append(f"## {s['h_install']}\n")
    out += [f"{i}. {step.format(releases=RELEASES)}" for i, step in enumerate(s["install"], 1)]
    out.append("")
    out.append(f"## {s['h_use']}\n")
    out += [f"{i}. {step}" for i, step in enumerate(s["use"], 1)]
    out.append("")
    out.append(f"## {s['h_speed']}\n")
    a, b, c = s["speed_cols"]
    out.append(f"| {a} | {b} | {c} |")
    out.append("|---|---|---|")
    for name, (pages, workers) in zip(SPEED_NAMES[code], SPEED_VALUES):
        out.append(f"| {name} | {pages} | {workers} |")
    out.append("")
    out.append(s["speed_note"] + "\n")
    out.append(f"## {s['h_how']}\n")
    out.append(s["how"] + "\n")
    out += [f"- {x}" for x in s["how_list"]]
    out.append("")
    out.append(s["privacy"] + "\n")
    out.append(f"## {s['h_perms']}\n")
    out += [f"- {x}" for x in s["perms"]]
    out.append("")
    out.append(f"## {s['h_disclaimer']}\n")
    out.append(s["disclaimer"] + "\n")
    out.append(f"## {s['h_license']}\n")
    out.append(s["license"])
    if code == "ar":
        out.append("\n</div>")
    return "\n".join(out) + "\n"


root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
for code, fname, _ in LANGS:
    with open(os.path.join(root, fname), "w", encoding="utf-8") as f:
        f.write(render(code))
print("readmes:", ", ".join(f for _, f, _ in LANGS))
