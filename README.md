# firatselcuk.dev

Personal portfolio site for Firat Selcuk, a Software Development Engineer in Test.

**Live site:** https://www.firatselcuk.dev

## Stack

Static HTML/CSS/JS — no framework, no build step. Pages are edited directly and deployed via GitHub Pages.

- **Frontend:** Plain HTML/CSS with jQuery + Skel (HTML5 UP template base)
- **Hosting:** GitHub Pages, custom domain via DNS + CNAME
- **Contact form:** Formspree
- **Daily news:** `scripts/fetch_news.py` (Python, stdlib only) fetches headlines from NewsAPI and writes `data/daily-news.json`, run daily by `.github/workflows/daily-news.yml` (GitHub Actions cron + manual trigger)

## Structure

- `index.html`, `projects.html`, `learn.html`, `resources.html`, `innovation.html`, `news.html` — site pages
- `assets/` — CSS, JS, images
- `data/daily-news.json` — auto-refreshed daily news data consumed by `news.html`
- `scripts/` — the news-fetching script and its tests
- `.github/workflows/` — CI/automation

## Running locally

No build step — open any `.html` file directly, or serve the folder with any static file server (e.g. VS Code's Live Server).

To run the news script's tests:

```bash
python3 -m unittest scripts.test_fetch_news -v
```
