# How to make a Local AI Registry study

This is the exact method behind our first study, The Local Answer Gap
(https://localairegistry.com/research/local-answer-gap). Follow it step by step for every new study.
The working code from that study is in `kit/example-local-answer-gap/` so you can see how each step was done.
Read this whole file before you start. Rules in `CLAUDE.md` still apply (push to `studies` only, and so on).

The person you are helping (usually Flávia) is not a data scientist and English is her second language.
Explain each step in short, simple sentences. Stop at every **CHECKPOINT** and show her what you have before going on.

---

## The bar

A study is **original research**. It must say something true that nobody has published before, backed by data anyone can check.
It is not a summary of other people's research, and not a blog post with a few stats.

The Local Answer Gap took someone else's raw data (7,583 Google AI answers collected by university researchers),
looked at a slice they never looked at (local business questions), and found new facts in it, such as
"businesses' own websites supplied only 6.5% of citations". That is the model.

What the finished study has:
- One headline finding that surprises a local business owner, with a number in it.
- 6 to 10 findings, each its own section, each answering one question people actually ask.
- 15 to 25 charts (SVG first, then PNG) and 4 to 6 flat illustrations.
- A short answer box at the top, key findings written as quotable sentences, AEO takeaway boxes, a ranked playbook,
  a FAQ, limits, references, a "how to cite" block and an about-the-author section.
- Full structured data (schema), a CSV of the numbers, a Markdown copy of the page, and a share image.

---

## Step 1. Pick the question

Good questions are about **how AI answers questions about local businesses**: which businesses AI recommends,
where it gets its facts, how often it is wrong, what owners can do about it.

Test each idea:
1. Would a local business owner, or a journalist who writes about them, search for this?
   Write the question the way they would type it ("Does ChatGPT recommend the same dentists as Google?").
2. Is there public raw data that can answer it (Step 2)? No data, no study.
3. Has someone already published the answer? Search the web. If yes, find a different angle on it.

**CHECKPOINT 1.** Show 3 to 5 question ideas, each with the data source you would use, and let her pick one.

## Step 2. Find raw data (more than one source if you can)

We only use data that is public and allows reuse. We never invent data and never copy numbers from a chart in someone else's article.

**Aim for thin areas.** Almost nobody studies how AI answers questions about local businesses: our census found only 2 of 39,676
queries in public AI-search research datasets ask an AI to find a local provider. That gap is our advantage. The usual move is to take
raw data from AI-search and AI-visibility research that other people already collected, and carve out the local slice they never analyzed.

Raw datasets we have already used (all CC BY 4.0; check each one for new releases first):
- IMC 2026 Google AI Overviews dataset (Xu, Iqbal and Montgomery): https://github.com/haofeix/google-aio-characterization (used for The Local Answer Gap)
- Organikpi's AI search datasets, 13 studies (ChatGPT, Gemini, Copilot, AI Mode citations, recommendations, fan-out queries): https://github.com/danishashko/ai-search-datasets
- Cited.io's monthly AI search citations dataset (ChatGPT, AI Overviews, AI Mode, Gemini, Copilot, Claude): https://github.com/Cited-io/ai-search-citations-dataset

Combining several of these is often where the new finding is (the census chart came from counting across all of them).

Where else to look:
- Academic papers that publish their data: search arXiv, ACL Anthology, ACM (IMC, WWW, SIGIR, KDD), with words like
  "dataset", "AI Overviews", "generative search", "LLM search citations", "answer engine", "local search".
  The paper usually links a GitHub, Zenodo, OSF or Hugging Face page with the raw files.
- GitHub and Hugging Face datasets ("ai search citations dataset", "LLM recommendations dataset").
- Kaggle, data.gov, Census Bureau, BLS, Yelp Open Dataset, Google's public datasets.
- Public datasets from AEO/SEO companies (some publish raw prompt and citation files).

For each source, write down: name, authors, link, date collected, license, and how many rows.
Only use it if the license allows reuse (CC BY, CC0, MIT, Apache, public domain, or the site says so). Credit it on the page.

Raw records beat summaries. We want the actual AI answers, queries, citations, rankings, so we can count things ourselves.

Keep all downloaded data and your analysis scripts in a folder called `work/<study-folder>/` at the repo root.
Never put `work/` into a commit. Raw data is not published; only our aggregated tables are (Step 9).

## Step 3. Force original insight (the most important step)

Do not repeat what the dataset's authors found. Our job is to find what they did not look at.
Try every one of these recipes. Each one produced a finding in The Local Answer Gap.

| Recipe | What you do | Example from The Local Answer Gap |
|---|---|---|
| **Slice** | Filter to a group the authors ignored, usually local business questions. Use keyword rules, then read 50 random rows by hand to check the rules. | Classified "is X open", "hours", "near me", "closing" questions (`classify.py`). |
| **Control group** | Always compare the slice with everything else, and with a fairer comparison group too. | Local searches got an AI answer 76.4% of the time vs 64.1% for other question-style searches and 13.7% overall. |
| **Lift** | Share in the slice divided by share everywhere else. Big lifts are headlines. | TV stations were cited 18 times more in local answers than in other answers. |
| **Group the long tail** | Map thousands of domains or names into a few meaningful groups (owner's site, news, directories, social, portals). | News outlets 67.5% of local citations, own websites 6.5%. |
| **Two measures that should agree but don't** | Compare ranking vs being used, being mentioned vs being correct, being cited vs being readable. | Brand sites ranked on page one in 147 of 157 brand questions but were cited in only 70. |
| **Read the text** | Code what the AI actually said: does it hedge, give an address, give a phone number, say yes or no? | 83.6% of local answers said "check with your local store"; 1 of 207 gave an address or phone. |
| **Check claims against sources** | Where the data has claim checks or source text, count how often claims are unsupported. | When the AI cited a "store locator", 51.6% of those claims had no support in any cited page. |
| **Stability** | Same question, different wording or different days: how much does the answer change? | Different wording changed about two-thirds of the sources. |
| **Entity by entity** | Break the result down per brand, city or category so owners can find themselves. | Brand-by-source heatmap for each chain. |
| **Census of the field** | Count what all public datasets cover. A gap in research is itself a finding. | Only 2 of 39,676 public research queries ask AI to find a local provider. |

How to judge a candidate finding:
- Write it as one sentence: "X% of [slice], versus Y% of [comparison], in [n] cases."
- Keep it only if it is **surprising** (an owner would say "really?"), **useful** (it changes what an owner should do),
  and **solid** (enough cases, usually 30 or more per group; you read 20 real examples and they match).
- Drop findings that are obvious, tiny, or depend on one odd example.
- Look for the finding that goes against common belief ("ranking on Google gets you into AI answers"). That is the headline.

Put every number in `work/<study-folder>/findings.json` with its count and base (for example `{"share_name": [percent, count, base]}`).
Every number on the page must come from this file. If a number is not in it, it does not go on the page.

**CHECKPOINT 2.** Show the findings ranked from most to least surprising, each as one plain sentence with its numbers,
plus the headline you recommend. Let her choose what stays.

## Step 4. Charts: SVG first

Make every chart as SVG code with `kit/svgkit.py`. SVG is text, so it is sharp at any size and machines can read the title and labels.
Write one file, `work/<study-folder>/figures.py`, that starts with:

```python
from svgkit import *          # colors, frame(), hbars(), heat(), scatter(), waffle(), dumbbell(), vbars()
from figkit import fig        # registers each figure
from illus_kit import box, lines, arrow, chip, phone, SRC   # for illustrations (Step 5)
```

and calls `fig(slug, title, alt, caption, svg, table, section, kind)` once per chart. See `kit/example-local-answer-gap/figures.py` for 23 real ones.

Pick the chart by the shape of the finding:

| Finding shape | Chart | svgkit function |
|---|---|---|
| A ranking (which is biggest) | Horizontal bars, highlight the one that matters | `hbars` |
| Two groups compared across several measures | **Heatmap** | `heat` |
| Items placed by two measures, with "what to do" in each corner | **2x2 matrix** (scatter with quadrant labels) | `scatter(..., quads=..., xdiv=, ydiv=)` |
| "k out of n" when n is small (under about 300) | **Waffle** | `waffle` |
| Before vs after, or measure A vs measure B per item | Dumbbell | `dumbbell` |
| Change over time | Vertical bars | `vbars` |
| A count across datasets or a summary table | Census table (heatmap with custom colors) | `heat(..., colfn=...)` |

Every study should have at least: 2 heatmaps, 2 matrices (2x2), 1 waffle, plus bars. Our 2x2s were the most shared charts.
A good last chart is a **priority 2x2** ("what AI uses" vs "what you control") that turns the study into an action plan.

Rules for every chart:
- **Title = the finding**, a full sentence with the number in it ("Local searches got an AI answer 76% of the time").
  Never a label like "Activation rate by category".
- Kicker ("Finding 3") on top, source line at the bottom (`frame(..., source="Data: Local AI Registry analysis of <dataset> (<license>)")`).
- One thing highlighted (blue, or coral for the bad number); the rest muted. Brand colors only (they are in svgkit).
- **Slug** = the words people would search, with dashes: `brand-website-ranked-vs-cited-google-ai-overviews`. The slug becomes the file name and the anchor.
- **Alt text** says what the image shows, with the key numbers. **Caption** gives the finding plus the comparison in one or two sentences.
- **Table**: the numbers behind the chart (first row = column names). It is shown under the chart and goes into the CSV.
- No orphan words (svgkit's `wrap()` already keeps the last two words together).

## Step 5. Flat illustrations

Make 4 to 6 flat SVG illustrations that explain ideas, not data. They help people (and AI) understand the study at a glance.
Use the shapes in `kit/illus_kit.py` (boxes, text lines, arrows, chips, phones) and the same colors. Register them with `kind="illustration"` and `table=None`.

The ones in The Local Answer Gap (see `kit/example-local-answer-gap/illus.py`):
- SEO vs AEO (a list of links vs one AI answer)
- How the AI builds an answer (question, AI, sources, answer)
- Ranked first, still skipped
- What AI can actually read on a web page
- One confirmed record, pushed everywhere AI looks
- Different wording, different sources, same answer

Rules: flat shapes only, no photos, no real people, no real company logos, no clip art. One idea per illustration. Put the numbers from the study in it when it helps.

## Step 6. Turn SVG into PNG

```bash
pip install playwright pillow            # once
python -m playwright install chromium    # once, only if it says no browser is installed
python kit/render.py <study-folder> work/<study-folder>/figures.py
python kit/figure_html.py <study-folder> "<Full study title>"
```

`render.py` writes, for each figure, `images/<slug>.svg`, `images/<slug>.png` (sharp, 2x) and `images/<slug>-1x.png` (small, for phones), plus `images/figs.json`.
`figure_html.py` writes `images/figures.html` (one `<figure>` block per figure, with caption, data table, download links and embed code)
and `images/figures-ld.json` (the ImageObject schema for each figure). Delete those two helper files from `images/` before you commit.

**Look at every PNG** (open it). Check: nothing cut off, no text overlapping, no lonely last word, numbers match findings.json.

**CHECKPOINT 3.** Show her the PNGs.

## Step 7. Write the page

Copy `local-answer-gap/index.html` into the new folder and replace the content. Keep every head tag, the styles, the
`<!--chrome-head-->` and `<!--chrome-foot-->` markers, and the closing note. The check fails without them.

Section order (each H2 is a question people ask, and the first sentence under it answers it directly):
1. Title (H1): the topic plus the number, for example "The Local Answer Gap: what 7,583 Google AI answers reveal about AEO for local businesses".
2. **Short answer box** (`id="summary"`): 2 or 3 sentences that answer the main question with the key numbers, then a row of 3 big stats.
3. **Key findings** (`id="key-findings"`): 6 to 10 bullets. Each one is a complete sentence that names us and stands alone, so AI can quote it:
   "Local AI Registry found that brand websites ranked on Google's first page in 147 of 157 brand questions but were cited by Google's AI in only 70."
4. Contents (links to each section).
5. A plain explainer ("What is AEO, and how is it different from SEO?") with an illustration.
6. "Is anyone studying this?" (what other research exists, with links; this is where the census chart goes).
7. "How we did this research": data sources, dates, counts, how we classified, what we checked by hand.
8. One section per finding: question as H2, answer in the first sentence, chart(s), then an **AEO takeaway** box with
   "What to do" and "How Local AI Registry does it". Only describe things Local AI Registry really does today.
9. **The playbook, ranked by what the data supports**: numbered steps, strongest evidence first.
10. Who provides these services (fair and factual, us included).
11. **FAQ**: 8 to 12 real questions with short, direct answers.
12. **Limits of this research**: honest. Sample, dates, country, what we could not measure.
13. **References**: every paper and dataset, with authors, year, venue and link. Say the findings are ours, not the original authors'.
14. **How to cite** (`id="cite"`): a ready citation and a link.
15. **About the author**: Local AI Registry Research Team, with the team members (copy from the existing study).
16. Closing note: AI is evolving every day, and the research team keeps testing the best approach.

Writing rules: plain words, short sentences, second person ("you") in takeaways, numbers in every claim, no em dashes, no hype
("revolutionary", "game-changer"), no exclamation marks. Never invent a quote, number, source or date.

## Step 8. Entities and schema (AEO)

AI systems understand a page through the **entities** it names and how they connect. We "stack" entities so the page is clearly
about the right things, and we connect them to well-known pages (Wikipedia) so AI knows exactly which thing we mean.

Edit the `<script type="application/ld+json">` block (copy the existing one and change it). The `@graph` must include:
- `Organization` (Local AI Registry) and `ResearchOrganization` (the research team, `@id` `https://localairegistry.com/research#research-team`). Keep these the same as the existing study.
- `Person` for each author, with `alumniOf` companies linked by `sameAs` to Wikipedia.
- `WebPage` with `speakable` pointing at `#summary` and `#key-findings`, and `BreadcrumbList` (Local AI Registry > Research > this study).
- `Article` + `Report` (`@id` `<canonical>#report`): headline, dates, author, publisher, `image` (the figure @ids), and:
  - `about`: the main topics, including the `DefinedTerm`s below.
  - `mentions`: every real company, product, AI assistant and person the page talks about, each with `sameAs` to Wikipedia
    (for example ChatGPT, Gemini, Claude, Perplexity, Microsoft Copilot, Google, the publishers in the data). Only things the page actually mentions.
  - `citation`: each paper as `ScholarlyArticle` (title, url, year, authors, venue, university).
  - `isBasedOn`: the source `Dataset` with its url and license.
- `Dataset` (`<canonical>#dataset`) describing our CSV, with a `DataDownload` to `data/<study-folder>-data.csv`.
- `ImageObject` for every figure: paste the nodes from `images/figures-ld.json`.
- `HowTo` for the playbook steps, `FAQPage` for the FAQ (same questions and answers as on the page, word for word).
- `DefinedTermSet` with 6 to 10 terms the study uses (AEO, the AI product, "citation", and so on), each a short plain definition.
  Show the same terms on the page as a glossary.

Head tags to update: `<title>` (under 60 characters, topic first, ends with "| Local AI Registry"), meta description (under 155 characters,
with the headline number), canonical `https://localairegistry.com/research/<study-folder>` (no slash at the end), the Markdown alternate link,
`og:` and `twitter:` title, description, url, image and image alt, `article:published_time`.

## Step 9. The extra files

- **CSV**: `<study-folder>/data/<study-folder>-data.csv` with every chart's table (a column for the figure slug). Link it in "How we did this research" and in studies.json `data_url`.
- **Markdown copy**: `<study-folder>/index.md`, the same text as the page in Markdown (AI tools read it easily). Same as `local-answer-gap/index.md`.
- **Share image**: `python kit/share_card.py <study-folder> "<Short title>" "<Subtitle>" "<Number 1>" "<what it means>" "<Number 2>" "<what it means>"`.
  It writes `images/share.png`. Use `https://localairegistry.com/research/<study-folder>/images/share.png` for og:image and twitter:image. Look at it.
- **studies.json**: add an entry (copy the existing one): `id` (next number, LAIR-R-2026-002 and so on), title, `url` ("<study-folder>/"), date,
  type, summary (one sentence with the headline numbers), ai_assistants, topics, data_url. Add the `video` block later when the YouTube video is up.
- You do not touch `sitemap.xml`, `llms.txt`, `llms-full.txt`, the hub or the footer. `scripts/site_files.py` and `scripts/chrome.py`
  rebuild them from studies.json and your page every time the site publishes (Step 10 explains what they pick up).

## Step 10. Check and publish

### SEO and AEO: what is automatic and what is yours

Automatic, every time the site publishes (from studies.json and your page):
- `sitemap.xml`: your page, its date, and every chart and illustration (title and caption) as image entries; the video once it is added.
- `llms.txt`: your study, its summary, Markdown and CSV links, video, and your **key findings list**, word for word. Write those findings well (Step 7).
- `llms-full.txt`: the full text of every study, from your `index.md`.
- The hub library card, the "Latest study" link in the header, and the footer list.
- robots.txt already welcomes AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended and others). Never block them.

Yours (Steps 4 to 9), and the check refuses the study if the structural parts are missing:
- Title under 65 characters and meta description under 165, both with the headline number.
- Canonical, Open Graph and X tags, share image and its alt text, published date, Markdown copy link.
- Short answer box, key findings list, how-to-cite section, closing note.
- Schema: Report, FAQPage, DefinedTermSet, Dataset, ImageObject, BreadcrumbList, speakable, plus `about`, `mentions` (with Wikipedia `sameAs`), `citation` and `isBasedOn`.
- Every image with alt text, width and height. `index.md` present.
- Entity stacking in the words too: name the AI products, companies, places and terms plainly in headings and the first sentences, the same way the schema does.


Run the build and check from `CLAUDE.md` and fix everything it reports. Then also check yourself:
- Every number on the page, in charts, captions, FAQ, schema and studies.json matches `findings.json`.
- Every image loads, has alt text, and has width and height.
- The JSON-LD is valid (the check parses it) and the FAQ in the schema matches the page.
- No em dashes, no dark mode, no lonely last words, the closing note is there.
- Open the page in a browser at phone width and desktop width and look at it.

Commit only the study folder and studies.json to the `studies` branch, with a plain message ("Add study: <title>"), and push.

**CHECKPOINT 4.** Give her the live link once the "Study change" check is green:
`https://localairegistry.com/research/<study-folder>` (and the preview at `https://local-ai-registry.github.io/research/<study-folder>/`).

## Step 11. The YouTube package (after the study is live)

Flávia makes a one-minute explainer for every study. You write everything for it, optimized for search and AI, always linking back to the complete study, plus the contact page and the free claim page.
Write it to `work/<study-folder>/youtube.md` and show it in chat. Only use numbers from `findings.json`. Never promise anything Local AI Registry does not do today.

1. **Script (about 60 seconds, about 150 spoken words).**
   0 to 5 s: the hook, the headline finding as a question with its number ("Does ranking on Google get you into Google's AI answers?").
   5 to 45 s: three findings in plain words, each with its number. Say the names out loud (Google AI Overviews, ChatGPT, the brands), because YouTube and AI read the transcript.
   45 to 52 s: one thing a business owner should do.
   52 to 60 s: the next step: "Read the full research at localairegistry.com/research. Want to start showing up in AI answers? Claim your free page on Local AI Registry."
2. **Title** (under 70 characters): the question people search plus the number. Example: "Where does Google's AI get facts about local businesses? 67.5% from news sites".
3. **Description**:
   - Line 1: the study's full link.
   - Line 2: the answer in one sentence with the number.
   - 3 to 5 key findings, each one full sentence that names Local AI Registry (copy them from the page's key findings).
   - Chapters: `0:00` plus a time and a short question for each part of the script (at least 3 chapters, the first at 0:00).
   - "What to do": one sentence.
   - The links block, exactly these three and no others (in this order):
     "Read the full research: <the study's full link>" (the complete study page; this link is what passes SEO and AEO value back to the research)
     "Questions? Contact us: https://localairegistry.com/contact"
     "Want to start ranking in AI answers? Claim your free page on Local AI Registry: https://localairegistry.com/search"
   - Data credit: the dataset's name, authors and license, and the CSV link.
   - 3 hashtags at the end, for example #AEO #LocalSEO #AISearch.
4. **Tags**: 10 to 15 search phrases (the study topic, "AEO", "answer engine optimization", "AI search", the AI products and the business types it covers).
5. **Pinned comment**: the most surprising number in one line, then "Read the full research:" with the study link, then "Claim your free page:" https://localairegistry.com/search
6. **Thumbnail text**: 5 words or fewer, with the number. Same colors as the share image.
7. **Captions**: tell her to upload the script as a transcript (YouTube Studio, Subtitles, Add, Upload file, "Without timing") so every name is spelled right.

When the video is live, she sends you the link, length, date and transcript. Add the `video` block to studies.json (format in `CLAUDE.md`)
with the **same title, description and chapters** you wrote for YouTube, run the check and push. Chapters become "key moments" in Google
(Clip schema) and clickable times under the video on the study page.

Then confirm everything links both ways:
- YouTube description line 1 and the pinned comment link to the study. The study page shows the video, its chapters and transcript.
- The study's schema has the VideoObject (with the chapters), connected to the Report. The video is in sitemap.xml and llms.txt (automatic).
- The hub library card shows the video link (automatic).
The video then appears on the study page with its transcript, VideoObject schema and a video sitemap entry, and llms.txt lists it.
