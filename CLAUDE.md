# emotions-club — карта

Страница кейса переехала в портфолио: `project.html?id=emotions-club`, блоки — в `projects.json` репо
EyeAnton.github.io (правятся в админке). Тексты и раскладку менять там, не здесь.

| Что | Где |
|---|---|
| Переадресация со старого адреса /emotions-club/ | `index.html` |
| Картинки и видео кейса (страница грузит их по `/emotions-club/assets/…`) | `assets/` — файлы не переименовывать |
| Сборка ассетов из сырой папки | `tools/build_assets.py` |
| Новелла для плеера в портфолио (блок `novel`): JSON сценария + картинки → `assets/novels/<id>/` (novel.json + webp как есть). Эмоции подхватит сама, когда рядом появятся `character_NN_<эмоция>` | `python3 tools/build_novel.py "<сырьё>/room_313.json"` |

Сырьё: `C:\Users\lerit\Yandex.Disk\Портфолио_SDG\2026\Portfolio\Emotions Club` (`.sources.json` — исходные пути в SDG).
Ждём от пользователя: JSON с маркерами из файла генерации ComfyUI (найдёт сам), спрайты эмоций (в сырье только `_base`),
видео пайплайна — добавлять новыми блоками в админке.
