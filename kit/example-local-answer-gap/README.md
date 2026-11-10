# Worked example: the code behind The Local Answer Gap

These are the real scripts used to make https://localairegistry.com/research/local-answer-gap. Read them to see how each PLAYBOOK step was done.
They are a record, not tools to run: file paths point at the original working folder, and some web addresses (research.localairegistry.com) are from before the site moved to localairegistry.com/research.

Order they ran in:
1. `extract.py`  pulls every AI answer, its citations and the page-one results out of the raw dataset files.
2. `classify.py` finds local business questions with keyword rules (then checked by hand).
3. `analyze.py`  local vs everything else: how often an AI answer appears, citations per answer, top domains.
4. `deep.py`     groups thousands of domains into source types (own site, newspapers, TV, portals, social).
5. `deep2.py`    reads the answer text: hedging ("check with your local store"), yes/no verdicts, ranked vs cited.
6. `deep3.py`    national framing, address or phone in the answer, unsupported claims, stability across days.
7. `deep4.py`    how faithful the AI's claims were to the pages it cited.
8. `extra.py`, `final.py`  per-category and per-brand breakdowns, the census of public datasets.
9. `figures.py`  every chart (uses `svgkit.py`). `illus.py` every illustration.
10. `render.py`  SVG to PNG. `page.py` builds the page, the schema, the FAQ, the glossary and the CSV.

For a new study use the tools one folder up (`kit/svgkit.py`, `kit/figkit.py`, `kit/illus_kit.py`, `kit/render.py`, `kit/figure_html.py`, `kit/share_card.py`).
