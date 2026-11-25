<p align="center"><img src="icons/icon128.png" width="96" alt=""></p>

# TikTok Repost Cleaner

[English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md) · [العربية](README.ar.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Português (BR)](README.pt-BR.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · **Türkçe**

TikTok repostlarını tek tıkla silen bir tarayıcı eklentisi — hepsini ya da yalnızca en yenilerini.

- **Hızlı.** Repost listesi aynı anda birçok sayfa halinde okunur ve repostlar onlarca paralel istekle silinir. Liste okunurken silme işlemi zaten başlar.
- **Tümü ya da en yeni N tane.** Hepsini temizle ya da en yeni kaç repostun silineceğini yaz.
- **Üç hız:** Dikkatli, Normal ve Hızlı.
- **TikTok sayfasında canlı ilerleme:** sayaç, saniye başına hız ve Durdur düğmesi.
- **11 dil.** Eklenti tarayıcının dilini kullanır.
- **Chrome, Edge, Brave, Opera, Arc, Yandex Browser** ve diğer Chromium tarayıcılarda çalışır.

## Kurulum

1. [Son sürümden](https://github.com/tedovy/tiktok-repost-cleaner/releases/latest) `tiktok-repost-cleaner-*.zip` dosyasını indir.
2. Arşivi aç.
3. `chrome://extensions` adresini aç (Edge: `edge://extensions`, Yandex: `browser://extensions`).
4. **Geliştirici modunu** aç.
5. **Paketlenmemiş öğe yükle**'ye tıkla ve açtığın klasörü seç.
6. Eklentiyi araç çubuğuna sabitle (yapboz simgesi → raptiye).

## Kullanım

1. Bu tarayıcıda TikTok'a giriş yap.
2. Eklenti simgesine tıkla.
3. **Tümü** ya da **En yeni…** seç ve kaç tane olduğunu yaz.
4. **Sil**'e bas. Profilin açılır ve silme hemen başlar; köşedeki panel ilerlemeyi gösterir. **Tamam** yazana kadar sekmeyi kapatma.
5. Güncel repostlarını görmek için **Sayfayı yenile**'ye bas.

## Hız ve TikTok sınırları

| Mod | Aynı anda liste sayfası | Aynı anda silme |
|---|---|---|
| Dikkatli | 1 | 3 |
| Normal | 4 | 16 |
| Hızlı | 8 | 48 |

Silme TikTok için hafiftir, ama repost listesi ağırdır ve çok sık istenirse TikTok onu tüm hesap için geçici olarak sınırlar (bir süre sitedeki Repostlar sekmesi bile boş görünür). Böyle olursa eklenti durup yeniden dener; sınır kalkmazsa durur ve kaç repost silindiğini söyler. Birkaç dakika bekleyip düğmeye tekrar bas — kalanlarla devam eder.

## Nasıl çalışır

Eklenti sitede tıklama yapmaz. Açık TikTok sekmenden, TikTok sitesinin gönderdiği isteklerin aynısını gönderir:

- `GET /api/repost/item_list/` — repost listen, sayfa başına 30;
- `POST /tiktok/v1/upvote/delete?item_id=…` — **Repostu kaldır** düğmesiyle aynı istek.

TikTok dışında hiçbir yere bir şey gönderilmez. Eklenti veri toplamaz, şifrelerini ya da çerezlerini okumaz.

## İzinler

- `tiktok.com` — TikTok sekmesinde çalışmak için;
- `scripting` — o sekmede silmeyi başlatmak için;
- `tabs` — profilini açmak için;
- `storage` — ayarlarını hatırlamak için.

## Sorumluluk reddi

TikTok veya ByteDance ile bağlantılı değildir. Eklenti, TikTok'un her an değişebilecek resmi olmayan web uç noktalarını kullanır. Silinen repostlar otomatik olarak geri getirilemez. Kullanım riski sana aittir.

## Lisans

MIT — [LICENSE](LICENSE) dosyasına bak.
