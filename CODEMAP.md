# CODEMAP — emotions-club

Репо — статический склад ассетов для страницы кейса в портфолио (`EyeAnton.github.io`, `project.html?id=emotions-club`).
Кода, который работает в браузере, здесь нет (кроме переадресации); плеер новелл живёт в портфолио (блок `novel`).

## Модули

| Файл | Роль |
|---|---|
| `index.html` | meta refresh + `location.replace` на `/project.html?id=emotions-club`, OG-теги для превью ссылки |
| `tools/build_assets.py` | сырьё → `assets/story`, `covers` (+`covers/full`), `casts`, `videocovers`, `promo`. Списки новелл в константах `COVERS`, `CASTS`, `VIDEOCOVERS`, `PROMOS`; имя файла = `slug(title)` |
| `tools/build_novel.py` | `build()`: JSON истории SDG (`tales.<id>`) → `assets/novels/<id>/novel.json` + картинки. Заполняет пропуски фонов, подбирает спрайт эмоции по ремарке «(shocked) …», считает слова/выборы/концовки |
| `tools/build_library.py` | цикл `build()` по `NOVELS` (id → название в сырье, название на сайте, жанр) + `thumb.jpg` 360px + `library.json` (бесплатные — `FREE`, сначала они, потом по длине) |
| `tests/test_tools.py` | unittest на синтетической истории |

## Потоки данных

```
Яндекс.Диск «Emotions Club» (сырьё, вне git)
  ├─ cover/scene/character/videocover/promo (<Title>).* ──build_assets.py──► assets/{story,covers,casts,videocovers,promo}
  └─ <id>.json + картинки (<Title>)          ──build_library.py → build_novel.build()──► assets/novels/<id>/{novel.json,*.webp|jpg,thumb.jpg}
                                                                                   └──► assets/novels/library.json
assets/** ──GitHub Pages (main)──► https://eyeanton.github.io/emotions-club/assets/…
          ──ссылки из projects.json (админка портфолио) и плеера novel──► страница кейса
```

## Формат `novel.json` (контракт с плеером портфолио — не менять без правки плеера)
`{id, title, genre, accent, start, length, cover, chars:{<id>:{name,img,side,emo:{<эмоция>:file}}},
screens:{<id>:{t, bg, text, p, title?, who?, emo?, by?, opts?:[{text,to}], next?}}}`

`library.json`: `{novels:[{id,title,genre,free,src,cover,thumb,minutes,choices,endings}]}`

## Связи с другими проектами
- `portfolio` (EyeAnton.github.io) — страница кейса и плеер, ссылается на файлы отсюда.
- `gamebook-editor/tools/import_emc.py` — тот же импорт историй Emotions Club для Стасика; таблицы `EMOTIONS`,
  `GENRES` и `emotion_of()` продублированы (см. «Переиспользуемое» в отчёте архитектора).
