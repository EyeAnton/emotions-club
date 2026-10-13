# emotions-club — карта

| Что | Где |
|---|---|
| Разметка и русские тексты | `index.html` (`data-i18n`) |
| Английские тексты, списки картинок (сцены, каст, обложки, видео) | `app.js` (EN, SCENES, CAST, CASTS, COVERS, VCOVERS, PROMOS) |
| Стили страницы (`ec-*`) | `style.css`; общее — `/design-system.css`, `/style.css` портфолио |
| Сборка ассетов из сырой папки | `tools/build_assets.py` |

Сырьё: `C:\Users\lerit\Yandex.Disk\Портфолио_SDG\2026\Portfolio\Emotions Club` (`.sources.json` — исходные пути в SDG).
Ждём от пользователя (в index.html — TODO-комментарии): JSON с маркерами из файла генерации ComfyUI (найдёт сам),
спрайты эмоций (в сырье только `_base`), видео пайплайна.
