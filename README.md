# localairegistry.com/research

Static site for Local AI Registry research. No build step: every file here is served as is.

## Contents

- `index.html`: research hub (lists studies)
- `local-answer-gap/index.html`: The Local Answer Gap report
- `local-answer-gap/images/`: 29 charts and illustrations, each as `.png` (shown on page, 2x resolution) and `.svg` (download)
- `local-answer-gap/data/local-answer-gap-data.csv`: data behind every chart (CC BY 4.0)
- `sitemap.xml`: page and image sitemap
- `robots.txt`: allows search and AI crawlers
- `llms.txt`: plain-text summary for AI systems
- `llms-full.txt` and `local-answer-gap/index.md`: the full report as Markdown for AI crawlers
- `.nojekyll`: REQUIRED. Stops GitHub Pages from running Jekyll, which would otherwise convert `index.md` into HTML and overwrite the report page. Make sure this hidden file gets committed.
- `404.html`: not-found page
- `favicon.ico`, `favicon.svg`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`: browser and search icons
- `assets/fonts/`: self-hosted brand fonts (faster than Google Fonts; no third-party request)

## Deploy (GitHub Pages, shown at localairegistry.com/research)

The site lives in its own repo and is shown on the main domain by a forwarding rule (a "rewrite") on the main site. Visitors, Google and AI tools only ever see `localairegistry.com/research/...`. Nothing in this repo can change the main site.

1. Create the repo `Local-AI-Registry/research` (the name must be `research`, so GitHub serves it at `/research/`) and push this folder to `main`.
2. Repo Settings > Pages: Source "Deploy from a branch", branch `main`, folder `/ (root)`. No custom domain. It will be live at `https://local-ai-registry.github.io/research/`.
3. Main site (developer, one time), for Vercel/Next.js:
   - Rewrites: `/research` and `/research/:path*` to `https://local-ai-registry.github.io/research/` and `https://local-ai-registry.github.io/research/:path*`.
   - Redirect `/research` (no trailing slash) to `/research/` so relative links work.
   - Add `Sitemap: https://localairegistry.com/research/sitemap.xml` to the main `robots.txt`.
   - Link "Research" in the main site's nav or footer, and link `https://localairegistry.com/research/llms.txt` from the main `llms.txt`.
   - If the org ever adds its own `local-ai-registry.github.io` site with a custom domain, check that `/research/` still loads (GitHub would otherwise redirect it).
4. Check that https://localairegistry.com/research/local-answer-gap loads and all images show.

## Official profiles (already added)

The report and hub already list Local AI Registry's official profiles from the localairegistry.com footer (LinkedIn, X, Instagram, Facebook, TikTok, Pinterest) plus Trustpilot, YouTube, Crunchbase and SaaSworthy. When a Wikidata entry exists, add it to the `"sameAs"` list in the JSON-LD of `local-answer-gap/index.html` and `index.html` and redeploy. Also add the same profiles as `sameAs` in the main localairegistry.com homepage JSON-LD, which currently has none.

## After launch

1. Google Search Console: add the property `localairegistry.com/research`, submit `https://localairegistry.com/research/sitemap.xml`, request indexing for `/local-answer-gap/`.
2. Bing Webmaster Tools: submit the same sitemap (Bing feeds ChatGPT search and Copilot).
3. Validate structured data at https://validator.schema.org and https://search.google.com/test/rich-results.
4. Link to the report from localairegistry.com (nav or footer "Research") and from relevant blog posts, so it gets crawled and passes authority.
5. Optional: add `https://localairegistry.com/research/local-answer-gap/` to the main site's `llms.txt`.


## Launch checklist (in order)

1. Deploy, then open https://localairegistry.com/research/local-answer-gap on a phone and check images, fonts and the favicon.
2. Google Search Console: add the property, submit `sitemap.xml`, and use URL Inspection > Request indexing on `/local-answer-gap/`.
3. Bing Webmaster Tools: import from Search Console, submit the sitemap, and use URL Submission (Bing powers ChatGPT search and Copilot).
4. Validate: https://search.google.com/test/rich-results and https://validator.schema.org on the live URL. Run PageSpeed Insights on the live URL (it scored 100 on mobile in testing).
5. Main site (localairegistry.com):
   - Add footer links to YouTube, Crunchbase and SaaSworthy (they are missing today).
   - Add Organization JSON-LD to the homepage with `"@id": "https://localairegistry.com/#organization"` and the same `sameAs` list as the report. Using the same `@id` ties both sites into one entity.
   - Link to the report from the main nav or footer ("Research") and from 2 to 3 relevant pages.
6. Update the Crunchbase, LinkedIn and YouTube "about" sections to mention the research and link to it.
7. Distribution, which is what actually earns AI mentions: press release (the Nasdaq/Yahoo Finance channel that covered the launch), LinkedIn post from the company page and Steve, a YouTube explainer, pitches to local-business and SEO publications with the ready-to-quote findings and chart embed codes, and partner and referral sites embedding a chart.
8. When the report is updated, change `dateModified` in the JSON-LD and the date on the page, then resubmit in Search Console and Bing.

## For Flávia: adding a new study

You only ever edit one file: `studies.json`.

1. Put the new study's page in its own folder, for example `/med-spa-ai-study/` (each study is its own page, like `/local-answer-gap/`).
2. On GitHub, open `studies.json` and click the pencil (Edit).
3. Copy the existing study block, from `{` to `}`, paste it at the top of the list, put a comma after it, and change the values. The instructions at the top of the file list the allowed types and AI assistant names.
4. Click "Commit changes". About a minute later the "Build research hub" automation rebuilds the hub page. If something is wrong (a missing field or a misspelled AI assistant name), the automation fails and the Actions tab says exactly which line to fix.
5. Add the new page to `sitemap.xml` and `llms.txt`.

Search and filters appear on the hub automatically once there are 10 studies.

The hero map lives in `simulations/quiktox-foot-traffic/`. The hub shows it with `?embed=1`, which hides the map's own title card so the hub headline sits on top.

## For Flávia: adding the 1-minute explainer video

Once the video is live on YouTube, add a `video` block to that study in `studies.json` (the example is at the top of the file) and commit. Within about a minute the site:

- adds the video under the study's short answer, as a click-to-play thumbnail (the page stays fast because YouTube only loads when someone presses play),
- shows the transcript under it (AI tools read text, not video),
- adds the video's structured data (VideoObject) and links it to the report,
- adds the video to `sitemap.xml`,
- adds a "Video (1:04)" link to the study in the research library.

### On YouTube, every time

1. **Title:** a plain question or finding, for example "Why Google's AI rarely cites your business website (1-minute study)".
2. **Description, first line:** "Read the full study: " followed by the study link. Then 2 or 3 sentences with the main numbers, then "Data and charts: " and the study link again, then "Local AI Registry: https://localairegistry.com".
3. **Captions:** upload the script as a caption file (Subtitles > Add > Upload file, or "Auto-sync" with the script). Don't rely on auto-captions.
4. **Chapters:** if the video has sections, list timestamps in the description starting at 0:00.
5. **Pinned comment:** "Full study, charts and data: " plus the study link.
6. **Playlist:** add it to a "Local AI Registry Research" playlist.
7. **Thumbnail:** a custom one with the headline number, readable on a phone.
8. **Transcript for the site:** copy it from YouTube (More > Show transcript) or use the script, and paste it into `transcript` in `studies.json`.
