# research.localairegistry.com

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
- `CNAME`: custom domain for GitHub Pages
- `.nojekyll`: REQUIRED. Stops GitHub Pages from running Jekyll, which would otherwise convert `index.md` into HTML and overwrite the report page. Make sure this hidden file gets committed.
- `404.html`: not-found page
- `favicon.ico`, `favicon.svg`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`: browser and search icons
- `assets/fonts/`: self-hosted brand fonts (faster than Google Fonts; no third-party request)

## Deploy (GitHub Pages + Hostinger DNS, same as the audit subdomain)

1. Create a public repo (for example `localairegistry/research`) and push the contents of this folder to the root of `main`.
2. Repo Settings > Pages: Source "Deploy from a branch", branch `main`, folder `/ (root)`.
3. Custom domain: `research.localairegistry.com` (the CNAME file sets this). Tick "Enforce HTTPS" once the certificate is issued.
4. Hostinger DNS for localairegistry.com: add a CNAME record, name `research`, target `<github-org>.github.io`, TTL default.
5. Check that https://research.localairegistry.com/local-answer-gap/ loads and all images show.

## Official profiles (already added)

The report and hub already list Local AI Registry's official profiles from the localairegistry.com footer (LinkedIn, X, Instagram, Facebook, TikTok, Pinterest) plus Trustpilot, YouTube, Crunchbase and SaaSworthy. When a Wikidata entry exists, add it to the `"sameAs"` list in the JSON-LD of `local-answer-gap/index.html` and `index.html` and redeploy. Also add the same profiles as `sameAs` in the main localairegistry.com homepage JSON-LD, which currently has none.

## After launch

1. Google Search Console: add the property `research.localairegistry.com`, submit `https://research.localairegistry.com/sitemap.xml`, request indexing for `/local-answer-gap/`.
2. Bing Webmaster Tools: submit the same sitemap (Bing feeds ChatGPT search and Copilot).
3. Validate structured data at https://validator.schema.org and https://search.google.com/test/rich-results.
4. Link to the report from localairegistry.com (nav or footer "Research") and from relevant blog posts, so it gets crawled and passes authority.
5. Optional: add `https://research.localairegistry.com/local-answer-gap/` to the main site's `llms.txt`.

## Adding a new study

Create a new folder (for example `/next-study/`), add a card to `index.html`, and add the URL and images to `sitemap.xml` and `llms.txt`.

## Launch checklist (in order)

1. Deploy, then open https://research.localairegistry.com/local-answer-gap/ on a phone and check images, fonts and the favicon.
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
