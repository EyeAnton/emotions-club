# Visual Novels — ассеты кейса для портфолио

Кейс про генерацию интерактивных визуальных новелл (SDG, 2025): один JSON от агента → один ComfyUI-флоу →
фоны, персонажи с эмоциями, обложки, видеообложки.

Сама страница — в портфолио: https://eyeanton.github.io/project.html?id=emotions-club
(блоки в `projects.json` репо EyeAnton.github.io, правятся в админке). Старый адрес
https://eyeanton.github.io/emotions-club/ переадресует туда (`index.html`).

Этот репо хранит только картинки, видео и данные новелл, которые страница берёт по ссылкам
`/emotions-club/assets/…` (GitHub Pages с `main`). **Не переименовывайте файлы в `assets/`** — на них ссылаются
блоки в админке и плеер новелл.

## Запуск (сборка ассетов)
Нужен Python 3.9+ (только стандартная библиотека). Сырьё (папка «Emotions Club» на Яндекс.Диске) в репо не входит;
путь — аргументом или переменной `EMC_RAW`.

| Команда | Что делает | Внешние программы |
|---|---|---|
| `python3 tools/build_assets.py [SRC]` | картинки кейса → webp, видео → mp4 (`assets/story`, `covers`, `casts`, `videocovers`, `promo`) | ffmpeg (`FFMPEG` или PATH) |
| `python3 tools/build_assets.py [SRC] --full-covers` | только `assets/covers/full/` — обложки 1024px для увеличения | — |
| `python3 -I tools/build_library.py [SRC]` | все 28 новелл → `assets/novels/<id>/` + `assets/novels/library.json` | sips (macOS) |
| `python3 tools/build_novel.py story.json [--title …] [--genre …] [--id …]` | одна новелла | sips — по желанию |

`SRC` по умолчанию: `build_assets.py` — `~/Yandex.Disk/Портфолио_SDG/2026/Portfolio/Emotions Club`,
`build_library.py` — `~/Downloads/Portfolio/Emotions Club`. Уже готовые файлы `build_assets.py` не пересобирает.

Новые файлы добавляются в кейс через админку портфолио: путь `/emotions-club/assets/…` в поле картинки или видео.

## Тесты
```
python3 -m unittest discover -s tests
```
Без сырья, ffmpeg, sips и сети: синтетическая мини-новелла во временной папке.

## Структура
- `index.html` — переадресация на страницу кейса в портфолио
- `assets/` — то, что раздаёт GitHub Pages (≈70 МБ, из них новеллы ≈54 МБ)
- `tools/` — сборщики ассетов (см. таблицу выше)
- `tests/` — тесты сборщиков
- `CODEMAP.md` — карта модулей и потоков данных

## Статус
Готово и работает в портфолио. Ждут сырья от владельца: спрайты эмоций (`character_NN_<эмоция>`, сейчас только
`_base`), JSON с маркерами из файла генерации ComfyUI, видео пайплайна.
