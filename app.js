(() => {
  "use strict";

  /* ---------------- Data: file names come from tools/build_assets.py ---------------- */

  const SCENES = [
    ["01_a", "Scene 1"], ["01_b", ""], ["02_a", "Scene 2"], ["02_c", ""],
    ["03_a", "Scene 3"], ["04_a", "Scene 4"], ["04_b", ""], ["04_c", ""], ["04_d", ""], ["04_e", ""],
    ["05_a", "Scene 5"], ["06_a", "Epilogue"], ["06_b", ""],
  ];
  // straight from room_313.json → characters
  const CAST = [
    { n: "Anna", role: { ru: "игрок · героиня", en: "player · heroine" } },
    { n: "James", role: { ru: "игрок · герой", en: "player · hero" } },
    { n: "Unseen Intruder", role: { ru: "NPC", en: "NPC" } },
    { n: "Piers Lark", role: { ru: "NPC · злодей", en: "NPC · villain" } },
  ];
  const CASTS = [
    ["the_cursed_crown", "The Cursed Crown"],
    ["song_of_the_sea_court", "Song of the Sea Court"],
    ["daughter_of_the_flame", "Daughter of the Flame"],
    ["the_thirst_pact", "The Thirst Pact"],
  ];
  const COVERS = [
    ["room_313", "Room 313"], ["ghost_in_4b", "The Ghost in 4B"], ["the_cursed_crown", "The Cursed Crown"],
    ["song_of_the_sea_court", "Song of the Sea Court"], ["daughter_of_the_flame", "Daughter of the Flame"],
    ["moonlight_heist", "Moonlight Heist"], ["the_witch_next_door", "The Witch Next Door"],
    ["hotel_mix_up", "Hotel Mix-Up"], ["crimson_masquerade", "Crimson Masquerade"],
    ["the_thirst_pact", "The Thirst Pact"], ["raiders_of_the_forgotten_star", "Raiders of the Forgotten Star"],
    ["the_island_escape", "The Island Escape"],
    ["the_archivist_s_code", "The Archivist's Code"], ["threads_of_the_moon", "Threads of the Moon"],
    ["talk_on_the_plane", "Talk on the Plane"], ["stuck_in_the_elevator", "Stuck in the Elevator"],
    ["the_double_life", "The Double Life"], ["new_year_with_the_ex", "New Year with the Ex"],
    ["echoes_of_peru", "Echoes of Peru"], ["the_enchanted_stranger", "The Enchanted Stranger"],
    ["resort_fling", "Resort Fling"], ["midnight_pitch_for_two", "Midnight Pitch for Two"],
    ["morning_in_paris", "Morning in Paris"], ["rival_s_touch", "Rival's Touch"],
    ["share_the_bed", "Share the Bed?"], ["private_lesson", "Private Lesson"],
  ];
  const VCOVERS = [
    ["ghost_in_4b", "The Ghost in 4B"], ["moonlight_heist", "Moonlight Heist"],
    ["the_witch_next_door", "The Witch Next Door"],
    ["treasure_of_two", "Treasure of Two"], ["the_double_life", "The Double Life"],
  ];
  const PROMOS = ["promo_1", "promo_2", "promo_3"];

  /* ---------------- Language (shared with the portfolio site via localStorage) ---------------- */

  // Russian is the source: it is written in index.html and read from the DOM once.
  const EN = {
    "nav.home": "Home", "nav.work": "Projects", "nav.contact": "Contact",
    "crumb": "← All projects",
    "hero.eyebrow": "Case study · AI pipeline",
    "hero.lead": "Interactive visual novels for two players. An agent writes one JSON for the whole story, and one ComfyUI flow turns it into backgrounds, characters with emotions and covers — in one style, with the right file names from the start.",
    "hero.story": "See a novel ↓", "hero.how": "How it was made",
    "meta.role": "Role", "meta.company": "Format", "meta.companyV": "In-house · NDA", "meta.when": "Period", "meta.tools": "Tools",
    "stat.novels": "novels in one style", "stat.screens": "screens in a single story", "stat.json": "JSON per novel → every asset",
    "task.eyebrow": "The task",
    "task.title": "A novel you play together",
    "task.text": "Every story is hundreds of screens, several locations and a whole cast. Novels shipped in a steady stream, so the art had to come off a production line rather than be drawn one by one.",
    "task.1t": "Two players and a cast", "task.1d": "The heroine and the hero are two real players. Around them, NPCs: villains, maids, rulers, ghosts. All of them have to look like one story.",
    "task.2t": "Choices change the scene", "task.2d": "At every branch one player picks one of three options while the other waits. Each branch has its own backgrounds; premium branches get their own cutscenes.",
    "task.3t": "Emotion in every line", "task.3d": "Dialogue lives on faces: a character is angry, flustered, smiling. The emotion set is generated up front, and the face stays the same from the first scene to the finale.",
    "pipe.eyebrow": "Pipeline",
    "pipe.title": "One JSON, the whole novel",
    "pipe.text": "Hands-on work stayed where it matters: style and selection. Everything else — from prompts to putting files in the right folders — is done by the agent + ComfyUI pair.",
    "pipe.1t": "Script", "pipe.1d": "Scenes, branches, character and location descriptions",
    "pipe.2t": "Agent → JSON", "pipe.2d": "One file with markers: background prompt 1, character 1, cover…",
    "pipe.3t": "ComfyUI flow", "pipe.3d": "One flow routes every marker to the right generative model",
    "pipe.4t": "Characters + emotions", "pipe.4d": "A base sprite and an emotion set, all with the same face",
    "pipe.5t": "Naming", "pipe.5d": "Every file lands in its place for data.json right away",
    "pipe.6t": "Editor &amp; promo", "pipe.6d": "Screens are assembled in the editor, covers come alive as video",
    "code.files": "Assets of one novel", "code.json": "A screen in data.json points to a file by name",
    "story.eyebrow": "One novel, start to finish",
    "story.text": "A six-scene thriller: a hotel, a staged murder and an old enemy. Every background of the story in a row — from the corridor outside the room to the airport at dawn. Light, palette and manner don't drift from scene to scene.",
    "story.hint": "Scroll sideways →", "story.cover": "Cover", "story.cut": "Premium-branch cutscene",
    "casts.eyebrow": "The cast",
    "casts.title": "Every story has its own cast",
    "casts.text": "Fantasy, a sea kingdom, vampires — the genres differ, yet the characters of one novel always look like one company: the same light, the same manner, the same scale.",
    "lib.eyebrow": "Library",
    "lib.title": "29 novels in one style",
    "lib.text": "Thrillers, fantasy, mystery and rom-coms. Covers come from the same flow as the scenes, so the storefront looks whole.",
    "promo.eyebrow": "Promo",
    "promo.title": "Covers that move",
    "promo.text": "A static cover becomes a five-second video cover for the storefront. Scenes and AI video become vertical ad spots in 9:16 and 1:1, cut separately for male and female audiences.",
    "res.eyebrow": "Result",
    "res.title": "Novels ship in a steady stream",
    "res.1t": "Script → assets with no manual sorting", "res.1d": "The agent writes the JSON; the flow generates and names files exactly as data.json expects.",
    "res.2t": "Consistent characters", "res.2d": "One face across every emotion and scene — no redraws.",
    "res.3t": "Promo out of the box", "res.3d": "Video covers and ad spots made from the same assets.",
    "next.eyebrow": "Next project",
    "next.text": "A collection of animated 3D gifts for a social app: from one shared style to a package for developers.",
    "next.open": "Open the case →", "next.all": "All projects",
    "foot.note": "Built without frameworks · works on any device", "foot.ds": "Design system",
  };
  const NAV_LABEL = { ru: "Разделы", en: "Sections" };

  const store = {
    get(k) { try { return localStorage.getItem(k); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch {} },
  };
  const $i18n = [...document.querySelectorAll("[data-i18n]")];
  const RU = Object.fromEntries($i18n.map((n) => [n.dataset.i18n, n.innerHTML]));
  let lang = store.get("lang") || ((navigator.language || "ru").toLowerCase().startsWith("ru") ? "ru" : "en");
  const $lang = document.getElementById("lang");
  const langHooks = [];
  function applyLang() {
    const dict = lang === "ru" ? RU : EN;
    document.documentElement.lang = lang;
    for (const n of $i18n) n.innerHTML = dict[n.dataset.i18n] ?? RU[n.dataset.i18n];
    document.querySelector(".tabs")?.setAttribute("aria-label", NAV_LABEL[lang]);
    $lang.textContent = lang === "ru" ? "EN" : "RU";
    langHooks.forEach((f) => f());
  }
  $lang.addEventListener("click", () => {
    lang = lang === "ru" ? "en" : "ru";
    store.set("lang", lang);
    applyLang();
  });

  /* ---------------- Galleries ---------------- */

  const esc = (s) => s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const $ = (id) => document.getElementById(id);

  // hero: covers drifting right to left; the set is repeated so the loop has no seam
  const cloud = COVERS.slice(0, 14).map(([s]) => `<img src="assets/covers/${s}.webp" alt="">`).join("");
  $("cloud").innerHTML = cloud + cloud;

  $("strip").innerHTML = SCENES.map(([id, label], i) => `<figure>
      <img src="assets/story/scene_${id}.webp" alt="Room 313 — scene_${id}" loading="lazy">
      <figcaption><b>${label || "&nbsp;"}</b><code>scene_${id}.webp</code></figcaption>
    </figure>`).join("");

  function renderCast() {
    $("cast").innerHTML = CAST.map((c, i) => `<figure>
        <img src="assets/story/character_0${i + 1}.webp" alt="${esc(c.n)}" loading="lazy">
        <figcaption><b>${esc(c.n)}</b><span>${c.role[lang]}</span><code>character_0${i + 1}_base</code></figcaption>
      </figure>`).join("");
  }
  langHooks.push(renderCast);

  $("casts-list").innerHTML = CASTS.map(([s, t]) => {
    const imgs = [1, 2, 3, 4, 5, 6, 7].map((i) =>
      `<img src="assets/casts/${s}/character_0${i}.webp" alt="" loading="lazy" onerror="this.remove()">`).join("");
    return `<article class="ec-lineup reveal"><h3>${esc(t)}</h3><div>${imgs}</div></article>`;
  }).join("");

  $("covers").innerHTML = COVERS.map(([s, t]) => `<figure class="reveal">
      <img src="assets/covers/${s}.webp" alt="${esc(t)}" loading="lazy"><figcaption>${esc(t)}</figcaption>
    </figure>`).join("");

  $("vcovers").innerHTML = VCOVERS.map(([s, t]) => `<figure class="reveal">
      <video muted loop playsinline preload="none" poster="assets/videocovers/${s}.webp" src="assets/videocovers/${s}.mp4"></video>
      <figcaption>${esc(t)}</figcaption>
    </figure>`).join("");

  $("phones").innerHTML = PROMOS.map((p) => `<div class="ec-phone reveal">
      <video muted loop playsinline preload="none" poster="assets/promo/${p}.webp" src="assets/promo/${p}.mp4"></video>
    </div>`).join("");

  // a missing file drops its whole tile instead of leaving a hole in the grid
  document.querySelectorAll("#strip img, #covers img, #vcovers video, #phones video").forEach((m) =>
    m.addEventListener("error", () => (m.closest("figure, .ec-phone") || m).remove()));

  applyLang();
  $("year").textContent = new Date().getFullYear();

  /* ---------------- Reveal on scroll + play videos only while visible ---------------- */

  document.documentElement.classList.add("js");
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    }), { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    document.querySelectorAll(".reveal").forEach((n) => io.observe(n));

    if (!reduced) {
      const vo = new IntersectionObserver((entries) => entries.forEach((e) => {
        if (e.isIntersecting) e.target.play().catch(() => {});
        else e.target.pause();
      }), { threshold: 0.4 });
      document.querySelectorAll("video").forEach((v) => vo.observe(v));
    }
  } else {
    document.querySelectorAll(".reveal").forEach((n) => n.classList.add("in"));
  }
})();
