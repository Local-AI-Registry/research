# Local AI Registry Research site: rules for Claude

This repo is the research section of Local AI Registry, shown at https://localairegistry.com/research/.
You are usually helping Flávia (growth marketing) add or update studies and their explainer videos.

## What you may change
- `studies.json` (the list of studies, including each study's optional `video` block).
- A study's own folder (for example `local-answer-gap/`) when adding a new study or fixing its content.

## What you must not change
- Anything in `scripts/`, `.github/`, `simulations/`, `assets/`, `og/`, or the root files (`index.html`, `404.html`, `robots.txt`, `sitemap.xml`, `llms.txt`, `CLAUDE.md`, `README.md`).
  These are built automatically or need Steve's approval. If a task seems to need them, stop and say so.
- Never edit the root `index.html` by hand. It is rebuilt from `studies.json`.

## How to work
1. Always work on a new branch and open a pull request. Never push to `main`.
2. Before finishing, run the build and the check, and fix anything they report:
   `python scripts/build_hub.py && python scripts/chrome.py && python scripts/video.py && python scripts/absolute_links.py && python scripts/check.py`
3. Do not commit the files the build changes (`index.html`, `sitemap.xml`, study pages). The site rebuilds itself when the pull request is merged. Only commit `studies.json` and the study folder you worked on.
4. In the pull request description, say in plain words what changed.

## Content rules
- Never invent numbers, quotes, sources or dates. Every number in a summary must come from the study itself.
- Video block format (add after `data_url`):
  `"video": { "youtube": "https://youtu.be/XXXXXXXXXXX", "length": "1:04", "uploaded": "2026-11-12", "transcript": "First paragraph.\n\nSecond paragraph." }`
  `length` is minutes:seconds, `uploaded` is the date it went live on YouTube, and the transcript is YouTube's transcript or the script.
- Writing style: plain language, no em dashes, no hype words.
- Every study page ends with a note that AI changes every day and that the Local AI Registry research team keeps testing the best approach.
- Light mode only. No dark mode.
