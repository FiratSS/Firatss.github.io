# Interest Fields on the Innovation Page (Robotics / ML / Blockchain / IoT)

## Problem

The "Current Innovation Projects" section of `innovation.html` (4 cards: AI-Assisted Testing, Mobile Testing Automation, Performance Testing Innovation, Collaborative Testing Platform, each tagged "Research Phase" / "Prototype Development" / "Concept Phase" / "Planning Phase") describes work that doesn't exist — no real project, code, or research backs any of it. It reads as filler and undercuts the credibility of the rest of the site, which is otherwise backed by real, verifiable work.

Separately, the site owner has genuine personal interest in four fields — Robotics, Machine Learning, Blockchain, IoT — that isn't project work, but is real curiosity/learning worth surfacing honestly.

## Goals

- Replace the fabricated "Current Innovation Projects" section with something honest: a personal-interest showcase for Robotics, ML, Blockchain, and IoT that doesn't claim project work or expertise that doesn't exist.
- Reuse the site's existing visual language (card + gold top-accent, per `.book-card`/`.project-card`) rather than introducing a new style system.
- Reuse the existing "detail modal" interaction pattern already proven on the Learn page, rather than inventing a new UI pattern.
- Keep nav unchanged — this lives inside the existing Innovation page, not a new top-level page.
- Content (intros, advanced topics, links) is clearly staged as an editable draft; nothing ships as "final" without the site owner reviewing and replacing placeholder text with their actual interests and real links.

## Non-goals

- Not claiming or implying shipped projects, published research, or professional experience in these fields.
- Not building a markdown/quiz content pipeline like Learn capsules — no quiz, no multi-page long-form content. Each field's detail is a fixed shape: intro, advanced topics list, curated external links.
- Not touching the "Areas of Innovation" section (Testing Innovation / Software Development / Creative Solutions) above it, or the "Share Your Innovation Ideas" form below it — both are handled separately.
- Not adding a new nav item or new page.

## Design

### Placement

In `innovation.html`, the existing section:

```html
<!-- Current Innovations -->
<section class="wrapper style2">
  ...
  <h2>Current Innovation Projects</h2>
  ...
</section>
```

is replaced in place by a new section, same position in the page (between "Areas of Innovation" and the innovation-idea form), with a heading such as "Fields I'm Exploring" (exact copy TBD with site owner during content review).

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
    // ... "ml", "blockchain", "iot" — same shape
  ]
}
```

`type` on a link is one of `course`, "paper", or `article` — used only to pick an icon in the modal (e.g. `fa-graduation-cap` for course, `fa-file-alt` for paper), no other behavioral difference.

This mirrors the existing `assets/learn/index.json` convention (a single JSON index, fetched client-side) but with a simpler, fixed record shape — no separate per-item file, since there's no long-form markdown body here.

### Card grid (always visible)

A 4-card grid, `id="interestsGrid"`, styled like the existing `.book-card` (`.interest-card` — new class, structurally the same: white background, `::before` gold gradient top bar, hover lift + shadow). Each card:

- Icon + title
- The `intro` text (draft or, once reviewed, final)
- A "Learn More" button (matches the visual weight of `.download-btn`/`.pdf-download-btn` — gold gradient pill), `onclick` opens the modal for that field's `id`

Populated client-side by fetching `assets/interests/index.json` on `DOMContentLoaded`, same pattern as `loadCapsules()` in `learn.html`. A fetch failure shows the same kind of inline error state already used elsewhere on the site (see `learn.html`'s `.no-results` / `index.html`'s news-load error block) — no separate design needed, reuse that convention.

### Modal (on "Learn More")

Reuses the existing `.capsule-detail-modal` / `.capsule-detail-content` / `.close-btn` CSS and open/close JS pattern from `learn.html` (dark overlay, centered white panel, `Escape` key and outside-click to close) — copied into `innovation.html`'s own `<style>`/`<script>` blocks (this site has no shared-include mechanism; every page owns its CSS/JS, consistent with how `learn.html`, `resources.html`, etc. already do it).

Modal content, built directly from the JSON record (no markdown rendering needed):

1. `<h1>` field title
2. Intro paragraph (same text as the card, or a slightly longer version if the site owner wants more room here — left to content review)
3. `<h2>Advanced & Applied Topics</h2>` + `<ul>` of `advancedTopics`
4. `<h2>Go Deeper</h2>` + list of `links`, each opening in a new tab (`target="_blank" rel="noopener noreferrer"`) with an icon per `type`

### Content

This spec ships with the 4 JSON records containing clearly-marked placeholder intros/topics/links (drafted from general knowledge) so the mechanism can be built and reviewed end-to-end. Before merge, the site owner replaces every placeholder field with their actual interests and real links. The implementation plan should call this out as an explicit review step, not silently ship placeholder copy to production.

## Testing

- Manually load `innovation.html` in a browser: confirm the 4 cards render, "Learn More" opens the correct field's modal, `Escape` and outside-click close it, and this matches the Learn page's existing modal behavior.
- Confirm the replaced section no longer references any of the old "Current Innovation Projects" copy.
- Confirm mobile layout (grid collapses to 1 column under 768px, matching the existing `@media (max-width: 768px)` pattern already used for `.capsules-grid`/`.projects-grid`/`.books-grid` on other pages).
- Confirm no placeholder/draft content ships without the site owner's explicit sign-off in review.
