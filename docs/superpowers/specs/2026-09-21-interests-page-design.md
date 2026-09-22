# Interests Page (Robotics / ML / Blockchain / IoT)

## Problem

The site owner has genuine personal interest in four fields — Robotics, Machine Learning, Blockchain, IoT — that isn't project work, but is real curiosity/learning worth surfacing honestly. It needs a home that's clearly distinct from `innovation.html`'s existing "Current Innovation Projects" section, which the site owner has decided to keep as-is (it represents work-related testing/QA innovation ideas) — the new research/interest content should not be folded into or blended with that section.

## Goals

- Give Robotics/ML/Blockchain/IoT an honest, dedicated home: a new page, `interests.html`, clearly separate from work-related content.
- Reuse the site's existing visual language (card + gold top-accent, per `.book-card`/`.project-card`) rather than introducing a new style system.
- Reuse the existing "detail modal" interaction pattern already proven on the Learn page, rather than inventing a new UI pattern.
- Add "Interests" as a new nav item, consistent with the site's existing short nav labels (Home, News, Let's Innovate, Projects, Resources, Learn).
- Content (intros, advanced topics, links) is clearly staged as an editable draft; nothing ships as "final" without the site owner reviewing and replacing placeholder text with their actual interests and real links.

## Non-goals

- Not claiming or implying shipped projects, published research, or professional experience in these fields.
- Not building a markdown/quiz content pipeline like Learn capsules — no quiz, no multi-page long-form content. Each field's detail is a fixed shape: intro, advanced topics list, curated external links.
- **Not modifying `innovation.html`'s content** — "Areas of Innovation," "Current Innovation Projects," and the "Share Your Innovation Ideas" form all stay exactly as they are today. The only change to `innovation.html` is the one-line nav addition described below (identical to the same addition on the other 5 existing pages) — this spec adds a new page and links to it; it does not otherwise modify the Innovation page.

## Design

### New page: `interests.html`

A new top-level page following the exact structural pattern every other page already uses (this site has no shared-include mechanism — each page owns its full `<head>`/nav/footer/scripts, e.g. compare `learn.html` and `resources.html`):

- `<head>`: title "Interests - Firat Selcuk", same meta/viewport/description pattern, same `main.css` + Font Awesome links as other pages, plus a page-local `<style>` block (no shared CSS file exists to extend).
- Header + nav: identical markup to every other page's nav, with one new `<li>` added (see Nav below).
- Banner: `<h1>Interests</h1>` + a short intro paragraph (site owner to write/approve — see Content below), following the same banner structure as `learn.html`/`projects.html`/`resources.html`.
- Main content: the card grid + modal (below).
- Footer + scripts: identical to every other page (jQuery, scrolly, scrollex, skel, util, main — no Learn-specific scripts like marked.js/Prism needed, since there's no markdown rendering here).

### Nav

Every one of the 6 existing pages (`index.html`, `news.html`, `innovation.html`, `projects.html`, `resources.html`, `learn.html`) has its own copy of:

```html
<ul class="links">
        <li><a href="index.html">Home</a></li>
        <li><a href="news.html">News</a></li>
        <li><a href="innovation.html">Let's Innovate</a></li>
        <li><a href="projects.html">Projects</a></li>
        <li><a href="resources.html">Resources</a></li>
        <li><a href="learn.html">Learn</a></li>
        <li><a href="index.html#footer">Contacts</a></li>
</ul>
```

All 6 files get the same new line added — `<li><a href="interests.html">Interests</a></li>` — inserted between the "Learn" and "Contacts" items, and `interests.html`'s own nav includes it in the same position. No page currently marks the "active" nav item (no `.active`/`.current` class exists on any `<li>`/`<a>` in the nav), so no active-state logic is needed for the new item either.

### Data

New file: `assets/interests/index.json`

```json
{
  "updated": "2026-09-21",
  "fields": [
    {
      "id": "robotics",
      "title": "Robotics",
      "icon": "fas fa-robot",
      "intro": "2-3 sentence draft intro — placeholder, to be replaced by site owner.",
      "advancedTopics": ["Draft topic 1", "Draft topic 2", "Draft topic 3"],
      "links": [
        { "label": "Draft course/article title", "url": "https://example.com", "type": "course" }
      ]
    }
    // ^ elided for brevity, not literal JSON — "ml", "blockchain", "iot" follow with the same shape; all 4 records ship in the initial file, none deferred
  ]
}
```

`type` on a link is one of `course`, `paper`, or `article` — used only to pick an icon in the modal (`fa-graduation-cap` for course, `fa-file-alt` for paper, `fa-newspaper` for article), no other behavioral difference. Since all link records are authored and reviewed pre-merge (not user-submitted), an unrecognized/missing `type` isn't a runtime case to design for — falling back to a generic `fa-link` icon if one ever appears is a reasonable implementation default, not a spec requirement.

This mirrors the existing `assets/learn/index.json` convention (a single JSON index, fetched client-side) but with a simpler, fixed record shape — no separate per-item file, since there's no long-form markdown body here.

### Card grid (always visible)

A 4-card grid, `id="interestsGrid"`, styled like the existing `.book-card` (`.interest-card` — new class, structurally the same: white background, `::before` gold gradient top bar, hover lift + shadow). Each card:

- Icon + title
- The `intro` text (draft or, once reviewed, final)
- A "Learn More" button (matches the visual weight of `.download-btn`/`.pdf-download-btn` — gold gradient pill)

Populated client-side by fetching `assets/interests/index.json` on `DOMContentLoaded`, same pattern as `loadCapsules()` in `learn.html`. Card click wiring follows Learn's actual pattern exactly (not a simplified version of it): render cards with a `data-field-id` attribute, attach `addEventListener('click', ...)` to each card after render (no inline `onclick`), and pass all JSON-sourced text (`title`, `intro`, `advancedTopics` entries, link `label`s) through the same `escapeHtml()` helper before injecting into `innerHTML` — matching `displayCapsules()` in `learn.html`. A fetch failure shows the same kind of inline error state already used elsewhere on the site (see `learn.html`'s `.no-results` / `index.html`'s news-load error block) — no separate design needed, reuse that convention.

### Modal (on "Learn More")

Reuses the existing `.capsule-detail-modal` / `.capsule-detail-content` / `.close-btn` CSS and open/close JS pattern from `learn.html` (dark overlay, centered white panel, `Escape` key and outside-click to close) — copied into `interests.html`'s own `<style>`/`<script>` blocks, same as every other page owns its own copy of shared-looking patterns.

Modal content, built directly from the JSON record (no markdown rendering needed):

1. `<h1>` field title
2. Intro paragraph — renders the same `intro` field used on the card (the schema has one `intro` field, not separate short/long variants); if the site owner wants more room in the modal specifically, that's a content-review decision about what to write into `intro`, not a schema change
3. `<h2>Advanced & Applied Topics</h2>` + `<ul>` of `advancedTopics`
4. `<h2>Go Deeper</h2>` + list of `links`, each opening in a new tab (`target="_blank" rel="noopener noreferrer"`) with an icon per `type`

### Content

This spec ships with the 4 JSON records containing clearly-marked placeholder intros/topics/links (drafted from general knowledge) so the mechanism can be built and reviewed end-to-end, plus placeholder banner/intro copy for the page itself. Before merge, the site owner replaces every placeholder field (intros, advanced topics, links) *and* signs off on the page's banner/intro wording with their actual interests, real links, and final wording. The implementation plan should call this out as one explicit review step covering both the JSON content and the page copy, not silently ship placeholder copy to production.

## Testing

- Manually load `interests.html` in a browser: confirm the 4 cards render, "Learn More" opens the correct field's modal, `Escape` and outside-click close it, and this matches the Learn page's existing modal behavior.
- Confirm all 6 existing pages' nav now includes a working "Interests" link, and `interests.html`'s own nav links back out correctly.
- Confirm `innovation.html`'s only diff is the new nav `<li>` (same one-line addition as the other 5 pages) — diff the rest of the file to confirm "Areas of Innovation," "Current Innovation Projects," and the "Share Your Innovation Ideas" form are unchanged.
- Confirm mobile layout (grid collapses to 1 column under 768px, matching the existing `@media (max-width: 768px)` pattern already used for `.capsules-grid`/`.projects-grid`/`.books-grid` on other pages).
- Confirm no placeholder/draft content — including the page's banner/intro text — ships without the site owner's explicit sign-off in review.
