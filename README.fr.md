<p align="center"><img src="icons/icon128.png" width="96" alt=""></p>

# TikTok Repost Cleaner

[English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md) · [العربية](README.ar.md) · [Deutsch](README.de.md) · **Français** · [Español](README.es.md) · [Português (BR)](README.pt-BR.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Türkçe](README.tr.md)

Une extension de navigateur qui supprime tes republications TikTok en un clic — toutes, ou seulement les plus récentes.

- **Rapide.** La liste des republications est lue plusieurs pages à la fois, et les republications sont supprimées par des dizaines de requêtes en parallèle. La suppression commence pendant que la liste est encore en cours de lecture.
- **Toutes ou les N plus récentes.** Tout effacer, ou indiquer combien de republications récentes supprimer.
- **Trois vitesses :** Prudent, Normal et Rapide.
- **Progression en direct** sur la page TikTok : compteur, vitesse par seconde et bouton Arrêter.
- **11 langues.** L'extension suit la langue de ton navigateur.
- Fonctionne dans **Chrome, Edge, Brave, Opera, Arc, Yandex Browser** et les autres navigateurs Chromium.

## Installation

1. Télécharge `tiktok-repost-cleaner-*.zip` depuis la [dernière version](https://github.com/tedovy/tiktok-repost-cleaner/releases/latest).
2. Décompresse-le.
3. Ouvre `chrome://extensions` (Edge : `edge://extensions`, Yandex : `browser://extensions`).
4. Active le **Mode développeur**.
5. Clique sur **Charger l'extension non empaquetée** et choisis le dossier décompressé.
6. Épingle l'extension à la barre d'outils (icône puzzle → épingle).

## Utilisation

1. Connecte-toi à TikTok dans ce navigateur.
2. Clique sur l'icône de l'extension.
3. Choisis **Toutes** ou **Récentes…** et indique combien.
4. Clique sur **Supprimer**. Ton profil s'ouvre et la suppression démarre aussitôt ; un panneau dans le coin affiche la progression. Garde l'onglet ouvert jusqu'à **Terminé**.
5. Clique sur **Actualiser la page** pour voir tes republications à jour.

## Vitesse et limites de TikTok

| Mode | Pages de liste à la fois | Suppressions à la fois |
|---|---|---|
| Prudent | 1 | 3 |
| Normal | 4 | 16 |
| Rapide | 8 | 48 |

Supprimer est léger pour TikTok, mais la liste des republications est lourde, et TikTok la limite temporairement pour tout le compte quand elle est demandée trop souvent (pendant un moment, même l'onglet Republications du site reste vide). Dans ce cas, l'extension fait une pause et réessaie ; si la limite ne se lève pas, elle s'arrête et indique combien de republications ont été supprimées. Attends quelques minutes et appuie de nouveau sur le bouton — elle reprend simplement avec ce qui reste.

## Comment ça marche

L'extension ne clique pas sur le site. Depuis ton onglet TikTok ouvert, elle envoie les mêmes requêtes que le site TikTok :

- `GET /api/repost/item_list/` — ta liste de republications, 30 par page ;
- `POST /tiktok/v1/upvote/delete?item_id=…` — la même requête que le bouton **Supprimer la republication**.

Rien n'est envoyé ailleurs qu'à TikTok. L'extension ne collecte aucune donnée et ne lit ni tes mots de passe ni tes cookies.

## Autorisations

- `tiktok.com` — pour fonctionner dans l'onglet TikTok ;
- `scripting` — pour lancer la suppression dans cet onglet ;
- `tabs` — pour ouvrir ton profil ;
- `storage` — pour mémoriser tes réglages.

## Avertissement

Sans lien avec TikTok ni ByteDance. L'extension utilise des points d'accès web non officiels de TikTok, qui peuvent changer à tout moment. Les republications supprimées ne peuvent pas être restaurées automatiquement. À utiliser à tes risques.

## Licence

MIT — voir [LICENSE](LICENSE).
