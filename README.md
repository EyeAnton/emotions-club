# Emotions Club — кейс для портфолио

Страница-кейс https://eyeanton.github.io/emotions-club/ — генерация интерактивных визуальных новелл (SDG, 2025):
один JSON от агента → один ComfyUI-флоу → фоны, персонажи с эмоциями, обложки, видеообложки.

Статика без сборки, GitHub Pages с `main`. Шапка, подвал и токены — из портфолио (`/design-system.css`, `/style.css`),
поэтому локально страница смотрится только рядом с репо портфолио.

## Ассеты
`python tools/build_assets.py [SRC]` — собирает `assets/` из сырой папки
(`Yandex.Disk\Портфолио_SDG\2026\Portfolio\Emotions Club`): webp для картинок, mp4 для видео. Нужен ffmpeg.
