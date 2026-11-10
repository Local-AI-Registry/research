# Local AI Registry Research site: rules for Claude

This repo is the research section of Local AI Registry, shown at https://localairegistry.com/research/.
You are usually helping Flávia (growth marketing) add or update studies and their explainer videos.

**Making a new study? Read `PLAYBOOK.md` first and follow it step by step.** It is the exact method behind The Local Answer Gap:
raw public data, original findings, SVG charts (heatmaps, 2x2s, waffles), flat illustrations, PNGs, the page, schema and AEO.
The tools it uses are in `kit/` (use them, do not change them). Keep raw data and your analysis scripts in `work/<study-folder>/`; never commit `work/`.

## How publishing works (read this first)
- Push your work to the **`studies`** branch. Commit and push directly; no pull request needed.
- The live site only ever takes two things from `studies`: `studies.json` and study folders (a lowercase-with-dashes folder such as `local-answer-gap/`). Everything else on that branch is ignored when publishing.
- The hub page, header, footer, map, design and scripts come only from `main`, which only Steve can change. Do not try to change them.
- After you push, the "Study change" check runs. A red X means the study breaks the template; the live site keeps the last good version until it's fixed. A green check means it will be live within a few minutes.

## What you may change
- `studies.json` (the list of studies, including each study's optional `video` block).
- A study's own folder: its `index.html`, `index.md`, `images/` (charts, illustrations and `share.png`) and `data/`.

## What you must not change
- Anything in `scripts/`, `kit/`, `.github/`, `simulations/`, `assets/`, `og/`, or the root files (`index.html`, `404.html`, `robots.txt`, `sitemap.xml`, `llms.txt`, `CLAUDE.md`, `README.md`, `PLAYBOOK.md`).
  These are built automatically or need Steve's approval. If a task seems to need them, stop and say so.
- Never edit the root `index.html` by hand. It is rebuilt from `studies.json`.

## How to work
1. Work on the `studies` branch (`git checkout studies`). Never push to `main` (it is locked).
2. Before finishing, run the build and the check, and fix anything they report:
   `python scripts/build_hub.py && python scripts/site_files.py && python scripts/chrome.py && python scripts/video.py && python scripts/absolute_links.py && python scripts/check.py`
3. Only commit `studies.json` and the study folder you worked on. Discard any other files the build changed (`git checkout -- index.html sitemap.xml llms.txt llms-full.txt`).
4. Write commit messages in plain words (for example "Add study: How ChatGPT picks dentists").

## The study template
- A new study copies the structure of `local-answer-gap/index.html`: same head tags, the short answer box (`id="summary"`), the Report structured data, the header and footer markers (`<!--chrome-head-->`, `<!--chrome-foot-->`), and the closing note. The check rejects a page that is missing any of these.
- The canonical address must be `https://localairegistry.com/research/<folder>` (no slash at the end).
- The share image is `<folder>/images/share.png`, made with `kit/share_card.py` (the root `og/` folder is Steve's).
- Add the study to `studies.json` with `url` set to `<folder>/`.

## Content rules
- Never invent numbers, quotes, sources or dates. Every number in a summary must come from the study itself.
- Video block format (add after `data_url`):
  `"video": { "youtube": "https://youtu.be/XXXXXXXXXXX", "length": "1:04", "uploaded": "2026-11-12", "title": "Same title as on YouTube", "description": "Same first sentences as on YouTube", "chapters": [{"time": "0:00", "name": "First chapter"}, {"time": "0:20", "name": "Second chapter"}], "transcript": "First paragraph.\n\nSecond paragraph." }`
  `length` is minutes:seconds, `uploaded` is the date it went live on YouTube, and the transcript is YouTube's transcript or the script.
  `title`, `description` and `chapters` are optional but always use them; they must match YouTube (PLAYBOOK.md Step 11).
- Writing style: plain language, no em dashes, no hype words.
- Every study page ends with a note that AI changes every day and that the Local AI Registry research team keeps testing the best approach.
- Light mode only. No dark mode.
