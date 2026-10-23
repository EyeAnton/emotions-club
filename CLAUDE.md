# emotions-club — карта

Страница кейса переехала в портфолио: `project.html?id=emotions-club`, блоки — в `projects.json` репо
EyeAnton.github.io (правятся в админке). Тексты и раскладку менять там, не здесь.

| Что | Где |
|---|---|
| Переадресация со старого адреса /emotions-club/ | `index.html` |
| Картинки и видео кейса (страница грузит их по `/emotions-club/assets/…`) | `assets/` — файлы не переименовывать |
| Сборка ассетов из сырой папки | `tools/build_assets.py` |
| Новеллы для плеера в портфолио (блок `novel`): все 28 → `assets/novels/<id>/` (novel.json + картинки; пропуски закрываются соседними фонами, тяжёлые фоны → JPEG через sips) и `assets/novels/library.json` (бесплатные — FREE в скрипте, порядок, жанр, minutes/choices/endings, thumb.jpg 360px). Одна новелла — `tools/build_novel.py`. Эмоции подхватятся сами, когда появятся `character_NN_<эмоция>` | `python3 -I tools/build_library.py [сырьё]` |

Сырьё: `C:\Users\lerit\Yandex.Disk\Портфолио_SDG\2026\Portfolio\Emotions Club` (`.sources.json` — исходные пути в SDG).
Ждём от пользователя: JSON с маркерами из файла генерации ComfyUI (найдёт сам), спрайты эмоций (в сырье только `_base`),
видео пайплайна — добавлять новыми блоками в админке.
