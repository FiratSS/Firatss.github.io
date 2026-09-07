# Daily News Fetch via GitHub Actions

## Problem

`data/daily-news.json` (consumed by `news.html`) is currently refreshed by a local n8n workflow that requires the user's machine to be on and n8n open, with a manual trigger. This means the file goes stale whenever the machine/app isn't running (confirmed stale since 2025-12-13). The n8n workflow itself is out of scope to inspect/replace in place — we are replacing *only* the daily news refresh job with a self-contained GitHub Actions workflow.

## Goals

- Daily automated refresh of `data/daily-news.json`, no local machine or app required.
- Preserve the existing JSON schema exactly, since `news.html` parses it directly.
- Keep the NewsAPI key server-side only (GitHub Actions secret) — never exposed to the client, consistent with the current architecture.
- Manual re-run option from the GitHub UI (`workflow_dispatch`).
- A bad fetch (API error, rate limit, etc.) must not overwrite good existing data with empty/partial data — fail loudly instead.

## Non-goals

- Migrating or decommissioning the existing n8n instance/workflow itself.
- Changing which categories are shown (`technology`, `business`, `sports` — hardcoded in `news.html:317`).
- Adding a build system / package.json to the repo.

## Design

### Trigger

`.github/workflows/daily-news.yml`:
- `schedule: cron("0 6 * * *")` — 06:00 UTC daily.
- `workflow_dispatch` — manual run button in the Actions tab.
- `permissions: contents: write` (needed to push the updated JSON back to `main`).

### Fetch script

`scripts/fetch_news.py` — Python 3 standard library only (`urllib.request`, `json`, `os`, `sys`), no third-party dependencies, so the workflow needs only `actions/setup-python` with no `pip install` step.

For each category in `["technology", "business", "sports"]`:
- Call `GET https://newsapi.org/v2/top-headlines?country=us&category={category}&pageSize=5` with header `X-Api-Key: $NEWS_API_KEY` (key read from the `NEWS_API_KEY` env var, sourced from the GitHub Actions secret of the same name — already added to the repo), using a 15-second request timeout (`urllib.request.urlopen(req, timeout=15)`).
- **Filter out NewsAPI's "removed" placeholder articles** before anything else: skip any article where `title == "[Removed]"` or `source.get("name") == "[Removed]"` or `url == "https://removed.com"`. NewsAPI returns these routinely for syndication-blocked content, and they must not reach the output file.
- From each remaining article, keep exactly the fields already present in `daily-news.json`: `title`, `description`, `url`, `source` (flattened from `source.name`), `publishedAt`, `image` (mapped from NewsAPI's `urlToImage`).
- `updated` is set from `datetime.now(timezone.utc).date()` — explicitly UTC, not the runner's local time (which is UTC anyway on GitHub-hosted runners, but the code should not rely on that implicitly).

Output shape (unchanged from current file):
```json
{
  "updated": "YYYY-MM-DD",
  "categories": {
    "technology": [ {title, description, url, source, publishedAt, image}, ... ],
    "business": [ ... ],
    "sports": [ ... ]
  }
}
```

### Error handling

- If any of the three API calls fails (non-200 response, network error, timeout, malformed JSON), the script prints the error to stderr and exits with a non-zero status **before** writing any file.
- This leaves `data/daily-news.json` untouched on failure, and the GitHub Actions run shows as failed (visible in the Actions tab / optionally notified by GitHub's default email-on-failure for workflow runs).
- A category returning fewer than 5 articles *after* removed-placeholder filtering (as `business` did historically) is not an error — write whatever remains for that category, unless it's zero articles after filtering, which is treated as a failure for that category (likely signals a bad API response rather than a genuinely quiet news day for a top-headlines category).

### Commit step

After a successful fetch, the workflow:
1. Configures git identity as `github-actions[bot]`.
2. `git pull --rebase` to pick up any commit that landed since checkout (guards against the scheduled run and a manual `workflow_dispatch` overlapping).
3. `git add data/daily-news.json`.
4. Commits only if there's a diff (`git diff --cached --quiet || git commit -m "Update daily news"`) — avoids empty commits when content is unchanged.
5. Pushes using the workflow's built-in `GITHUB_TOKEN` (scoped to this repo, expires with the run) — no third-party commit action, no PAT. Also set `concurrency: { group: daily-news, cancel-in-progress: false }` at the workflow level so two runs never execute this job simultaneously.

Assumption: `main` has no branch protection requiring PR review, so a direct push from `GITHUB_TOKEN` succeeds. If branch protection is later enabled on `main`, this workflow will need an exemption or a PAT with bypass rights — out of scope for this change, noted here so it isn't a silent failure surprise later.

## Testing

- Manually trigger via `workflow_dispatch` after merging and confirm:
  - `data/daily-news.json` is updated with a new `updated` date and fresh articles per category.
  - The commit appears on `main` authored by `github-actions[bot]`.
  - `news.html` (served from `raw.githubusercontent.com`) reflects the new data after the CDN cache clears.
- Verify failure path by temporarily using an invalid API key in a manual run (on a throwaway branch, not `main`) and confirming the run fails without touching the committed file.
