# Emotions Club — ассеты кейса для портфолио

Кейс про генерацию интерактивных визуальных новелл (SDG, 2025): один JSON от агента → один ComfyUI-флоу →
фоны, персонажи с эмоциями, обложки, видеообложки.

Сама страница теперь в портфолио: https://eyeanton.github.io/project.html?id=emotions-club
(блоки в `projects.json` репо EyeAnton.github.io, правятся в админке). Старый адрес
https://eyeanton.github.io/emotions-club/ переадресует туда (`index.html`).

Этот репо хранит только картинки и видео, которые страница берёт по ссылкам `/emotions-club/assets/…`
(GitHub Pages с `main`). Не переименовывайте файлы в `assets/` — на них ссылаются блоки в админке.

## Ассеты
`python tools/build_assets.py [SRC]` — собирает `assets/` из сырой папки
(`Yandex.Disk\Портфолио_SDG\2026\Portfolio\Emotions Club`): webp для картинок, mp4 для видео. Нужен ffmpeg.
Новые файлы добавляются в кейс через админку: путь `/emotions-club/assets/…` в поле картинки или видео.
