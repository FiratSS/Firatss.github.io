# Interests Page (Robotics / ML / Blockchain / IoT) Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a new `interests.html` page showcasing four personal-interest fields (Robotics, ML, Blockchain, IoT) as honest curated cards with a detail modal, linked from a new nav item on all 7 pages, without touching `innovation.html`'s content.

**Architecture:** Static HTML/CSS/JS, no build step, no shared includes — matches every existing page's pattern exactly (each page owns its full `<head>`/nav/footer/`<style>`/`<script>`). Content is data-driven from a new `assets/interests/index.json`, fetched client-side and rendered into a card grid; clicking a card opens a detail modal — both patterns copied from the already-working `learn.html` (`loadCapsules()`/`displayCapsules()`/`escapeHtml()`/modal open-close), adapted to the simpler fixed-shape record (no markdown, no quiz).

**Tech Stack:** Plain HTML/CSS/JS (no framework), Font Awesome 6.0.0-beta3 (already loaded site-wide via CDN), `fetch()` for the JSON data.

**Spec:** `docs/superpowers/specs/2026-09-21-interests-page-design.md`

---

## Chunk 1: Interests page

### Task 1: Create the interests data file

**Files:**
- Create: `assets/interests/index.json`

This is the data source for the page — a flat JSON object with one record per field. Content below is **explicit draft placeholder text** (per spec's Content section) that the site owner must replace before this ships; every placeholder value is prefixed `DRAFT:` so it's unmistakable in review.

- [ ] **Step 1: Write the JSON file**

```json
{
  "updated": "2026-09-21",
  "fields": [
    {
      "id": "robotics",
      "title": "Robotics",
      "icon": "fas fa-robot",
      "intro": "DRAFT: Placeholder intro — replace with your own words on why robotics interests you (2-3 sentences).",
      "advancedTopics": [
        "DRAFT: Placeholder topic — e.g. a specific sub-area of robotics you're curious about",
        "DRAFT: Placeholder topic — e.g. a specific robotics technique or platform",
        "DRAFT: Placeholder topic — e.g. how robotics connects to your testing background"
      ],
      "links": [
        { "label": "DRAFT: Placeholder course/article title", "url": "https://example.com", "type": "course" }
      ]
    },
    {
      "id": "ml",
      "title": "Machine Learning",
      "icon": "fas fa-brain",
      "intro": "DRAFT: Placeholder intro — replace with your own words on why machine learning interests you (2-3 sentences).",
      "advancedTopics": [
        "DRAFT: Placeholder topic — e.g. a specific ML technique you're exploring",
        "DRAFT: Placeholder topic — e.g. an ML application area",
        "DRAFT: Placeholder topic — e.g. how ML connects to testing/QA"
      ],
      "links": [
        { "label": "DRAFT: Placeholder course/article title", "url": "https://example.com", "type": "course" }
      ]
    },
    {
      "id": "blockchain",
      "title": "Blockchain",
      "icon": "fas fa-cubes",
      "intro": "DRAFT: Placeholder intro — replace with your own words on why blockchain interests you (2-3 sentences).",
      "advancedTopics": [
        "DRAFT: Placeholder topic — e.g. a specific blockchain concept",
        "DRAFT: Placeholder topic — e.g. a blockchain platform or protocol",
        "DRAFT: Placeholder topic — e.g. how blockchain connects to software testing"
      ],
      "links": [
        { "label": "DRAFT: Placeholder course/article title", "url": "https://example.com", "type": "course" }
      ]
    },
    {
      "id": "iot",
      "title": "IoT",
      "icon": "fas fa-microchip",
      "intro": "DRAFT: Placeholder intro — replace with your own words on why IoT interests you (2-3 sentences).",
      "advancedTopics": [
        "DRAFT: Placeholder topic — e.g. a specific IoT protocol or platform",
        "DRAFT: Placeholder topic — e.g. an IoT application area",
        "DRAFT: Placeholder topic — e.g. how IoT connects to your testing background"
      ],
      "links": [
        { "label": "DRAFT: Placeholder course/article title", "url": "https://example.com", "type": "course" }
      ]
    }
  ]
}
```

- [ ] **Step 2: Validate the JSON is well-formed**

Run: `python3 -m json.tool assets/interests/index.json`
Expected: pretty-printed JSON is echoed to stdout, exit code 0, no `json.decoder.JSONDecodeError`.

- [ ] **Step 3: Commit**

```bash
git add assets/interests/index.json
git commit -m "Add Interests page data file with draft placeholder content"
```

---

### Task 2: Scaffold the interests.html page shell

**Files:**
- Create: `interests.html`

Build the page shell first (head, nav, banner, empty main container, footer, scripts) — same skeleton every existing page uses, no card/modal content or custom CSS yet. This isolates "does the page load and match the site chrome" from "does the dynamic content work," matching the site's existing per-page structure (compare `resources.html`'s shell).

- [ ] **Step 1: Write the page shell**

```html
<!DOCTYPE HTML>
<html>

<head>
        <title>Interests - Firat Selcuk</title>
        <meta charset="utf-8">
        <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="description" content="Robotics, machine learning, blockchain, and IoT — personal interests and curated resources from Firat Selcuk.">
        <link rel="stylesheet" href="assets/css/main.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>

<body>
        <!-- Header -->
        <header id="header" class="alt">
                <div class="logo"><a href="index.html">Interests <span>by Firat</span></a></div>
                <a href="#menu">Menu</a>
        </header>

        <!-- Nav -->
        <nav id="menu">
                <ul class="links">
                        <li><a href="index.html">Home</a></li>
                        <li><a href="news.html">News</a></li>
                        <li><a href="innovation.html">Let's Innovate</a></li>
                        <li><a href="projects.html">Projects</a></li>
                        <li><a href="resources.html">Resources</a></li>
                        <li><a href="learn.html">Learn</a></li>
                        <li><a href="interests.html">Interests</a></li>
                        <li><a href="index.html#footer">Contacts</a></li>
                </ul>
        </nav>

        <!-- Banner -->
        <section id="banner">
                <div class="inner">
                        <header>
                                <h1>Interests</h1>
                                <p>DRAFT: Placeholder banner text — replace with your own framing of these as personal interests, not project work.</p>
                        </header>
                        <a href="#main" class="button big scrolly">Explore</a>
                </div>
        </section>

        <div id="main" class="container">
                <section class="wrapper style1">
                        <div class="inner">
                                <div class="section-header">
                                        <h2>Fields I'm Exploring</h2>
                                        <p>DRAFT: Placeholder section subtext — replace during content review.</p>
                                </div>

                                <div id="interestsGrid" class="interests-grid">
                                        <div class="loading">
                                                <i class="fas fa-spinner fa-spin" style="font-size: 2rem; margin-bottom: 1rem; display: block;"></i>
                                                <p>Loading...</p>
                                        </div>
                                </div>
                        </div>
                </section>
        </div>

        <!-- Footer -->
        <footer id="footer">
                <div class="copyright">
                        <ul class="icons">
                                <li><a href="https://www.linkedin.com/in/firat-selcuk-64b4b6231/" class="icon fab fa-linkedin"
                                                target="_blank"><span class="label">Linkedin</span></a></li>
                                <li><a href="https://github.com/FiratSS" class="icon fab fa-github" target="_blank"><span
                                                        class="label">GitHub</span></a></li>
                                <li><a href="mailto:firatselcuk010@gmail.com" class="icon fas fa-envelope" target="_blank"><span
                                                        class="label">Email</span></a></li>
                        </ul>
                </div>
        </footer>
        <div class="copyright">
                <p>&copy; 2026 Firat Selcuk. All rights reserved.</p>
        </div>

        <!-- Scripts -->
        <script src="assets/js/jquery.min.js"></script>
        <script src="assets/js/jquery.scrolly.min.js"></script>
        <script src="assets/js/jquery.scrollex.min.js"></script>
        <script src="assets/js/skel.min.js"></script>
        <script src="assets/js/util.js"></script>
        <script src="assets/js/main.js"></script>

</body>

</html>
```

- [ ] **Step 2: Verify the shell serves and loads without console errors**

Run: `python3 -m http.server 8000` (from repo root, leave running)
Open `http://localhost:8000/interests.html` in a browser (use the claude-in-chrome tooling if available in this session; otherwise open manually and report what you see).
Expected: page loads with the same header/nav/footer chrome as every other page, banner shows "Interests" + placeholder text, a "Loading..." spinner shows where the grid will be, no JS errors in the browser console (nothing calls the not-yet-defined interest functions yet, so there should be none).
Stop the server (`Ctrl+C`) when done, or leave it running for the next task's verification.

- [ ] **Step 3: Commit**

```bash
git add interests.html
git commit -m "Add interests.html page shell (nav, banner, empty grid container)"
```

---

### Task 3: Add card grid and modal CSS to interests.html

**Files:**
- Modify: `interests.html` (add a `<style>` block in `<head>`)

Add the page-local styles for the card grid and detail modal, adapted from `resources.html`'s `.book-card` pattern and `learn.html`'s `.capsule-detail-modal` pattern (per spec's Design section), renamed to this page's own vocabulary (`.interest-card`, `.interest-detail-modal`) rather than reusing Learn's "capsule" terminology.

- [ ] **Step 1: Insert the `<style>` block**

In `interests.html`, insert this block immediately before `</head>` (after the two `<link rel="stylesheet">` tags):

```html
        <style>
                .section-header {
                        text-align: center;
                        margin-bottom: 3rem;
                }

                .section-header h2 {
                        font-size: 2.5rem;
                        margin-bottom: 1rem;
                        color: #333;
                }

                .section-header p {
                        font-size: 1.2rem;
                        color: #666;
                        max-width: 600px;
                        margin: 0 auto;
                }

                .interests-grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                        gap: 2rem;
                        margin: 2rem 0;
                }

                .interest-card {
                        background: #fff;
                        border: 1px solid #e9ecef;
                        border-radius: 12px;
                        padding: 2rem;
                        transition: all 0.3s ease;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                        position: relative;
                        overflow: hidden;
                        cursor: pointer;
                        display: flex;
                        flex-direction: column;
                }

                .interest-card::before {
                        content: '';
                        position: absolute;
                        top: 0;
                        left: 0;
                        right: 0;
                        height: 4px;
                        background: linear-gradient(90deg, #B9852B, #96691C);
                }

                .interest-card:hover {
                        transform: translateY(-8px);
                        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
                        border-color: #B9852B;
                }

                .interest-card h3 {
                        margin-top: 0;
                        color: #333;
                        display: flex;
                        align-items: center;
                        gap: 0.75rem;
                        font-size: 1.4rem;
                }

                .interest-intro {
                        color: #555;
                        line-height: 1.6;
                        margin: 1rem 0;
                        flex: 1;
                }

                .learn-more-btn {
                        background: linear-gradient(135deg, #B9852B, #96691C);
                        color: white;
                        padding: 0.75rem 1.5rem;
                        border-radius: 25px;
                        font-weight: 500;
                        display: inline-flex;
                        align-items: center;
                        gap: 0.5rem;
                        align-self: flex-start;
                        margin-top: auto;
                }

                .loading {
                        text-align: center;
                        padding: 3rem;
                        color: #666;
                        grid-column: 1 / -1;
                }

                .no-results {
                        text-align: center;
                        padding: 3rem;
                        color: #888;
                        grid-column: 1 / -1;
                }

                .interest-detail-modal {
                        display: none;
                        position: fixed;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background: rgba(0,0,0,0.85);
                        z-index: 1000;
                        overflow-y: auto;
                        padding: 2rem;
                        backdrop-filter: blur(4px);
                }

                .interest-detail-modal.active {
                        display: flex;
                        align-items: flex-start;
                        justify-content: center;
                        padding-top: 3rem;
                }

                .interest-detail-content {
                        background: white;
                        border-radius: 16px;
                        max-width: 700px;
                        width: 100%;
                        max-height: 85vh;
                        overflow-y: auto;
                        padding: 3rem;
                        position: relative;
                        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                        margin-bottom: 2rem;
                }

                .close-btn {
                        position: absolute;
                        top: 1.5rem;
                        right: 1.5rem;
                        background: #f8f9fa;
                        border: 2px solid #e9ecef;
                        width: 42px;
                        height: 42px;
                        border-radius: 50%;
                        cursor: pointer;
                        font-size: 1.5rem;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        transition: all 0.3s ease;
                        color: #495057;
                        z-index: 10;
                }

                .close-btn:hover {
                        background: #e9ecef;
                        transform: rotate(90deg);
                        border-color: #B9852B;
                }

                .interest-detail-content h1 {
                        margin-top: 0;
                        color: #333;
                }

                .interest-detail-content h2 {
                        color: #B9852B;
                        margin-top: 2rem;
                        margin-bottom: 1rem;
                        font-size: 1.4rem;
                }

                .interest-detail-content ul {
                        margin: 1rem 0;
                        padding-left: 1.5rem;
                        line-height: 1.8;
                }

                .interest-links {
                        list-style: none;
                        padding-left: 0 !important;
                }

                .interest-links li {
                        margin: 0.75rem 0;
                }

                .interest-links a {
                        color: #B9852B;
                        text-decoration: none;
                        display: inline-flex;
                        align-items: center;
                        gap: 0.5rem;
                }

                .interest-links a:hover {
                        text-decoration: underline;
                }

                @media (max-width: 768px) {
                        .interests-grid {
                                grid-template-columns: 1fr;
                        }

                        .interest-detail-content {
                                padding: 1.5rem;
                                margin: 1rem;
                        }
                }
        </style>
```

- [ ] **Step 2: Verify no CSS parse errors**

Run: `python3 -m http.server 8000` (from repo root, if not already running from Task 2)
Open `http://localhost:8000/interests.html` in a browser.
Expected: page still loads with the same appearance as Task 2 (no cards yet since the grid still just shows the "Loading..." spinner — the JS to populate it doesn't exist until Task 4), no red/broken-CSS console warnings.

- [ ] **Step 3: Commit**

```bash
git add interests.html
git commit -m "Add card grid and detail modal CSS to interests.html"
```

---

### Task 4: Add the modal markup and the data-fetch/render/modal JS to interests.html

**Files:**
- Modify: `interests.html` (add modal `<div>` before `</body>`, add `<script>` block before `</body>`)

This wires up the actual behavior: fetch `assets/interests/index.json`, render the 4 cards, open/close the detail modal — following `learn.html`'s `loadCapsules()`/`displayCapsules()`/`escapeHtml()`/modal-open-close pattern exactly (data attribute + `addEventListener`, not inline `onclick`; all JSON-sourced text passed through `escapeHtml()` before being injected into `innerHTML`), per the spec's Card grid and Modal sections.

- [ ] **Step 1: Insert the modal markup**

In `interests.html`, insert this immediately after the closing `</div>` of `<div id="main" class="container">` (i.e., right before the `<!-- Footer -->` comment):

```html
        <!-- Interest Detail Modal -->
        <div id="interestModal" class="interest-detail-modal">
                <div class="interest-detail-content">
                        <button class="close-btn" onclick="closeInterestModal()">&times;</button>
                        <div id="interestDetailContent"></div>
                </div>
        </div>
```

- [ ] **Step 2: Insert the script block**

In `interests.html`, insert this immediately before the closing `</body>` tag (after the existing `<script src="assets/js/main.js"></script>` line):

```html
        <!-- Interests data and interaction -->
        <script>
                let allFields = [];

                async function loadFields() {
                        try {
                                const response = await fetch('assets/interests/index.json');
                                const data = await response.json();
                                allFields = data.fields;
                                displayFields();
                        } catch (error) {
                                console.error('Error loading interests:', error);
                                document.getElementById('interestsGrid').innerHTML =
                                        '<div class="no-results"><i class="fas fa-exclamation-circle" style="font-size: 2rem; margin-bottom: 1rem; display: block;"></i><p>Unable to load interests. Please try again later.</p></div>';
                        }
                }

                function displayFields() {
                        const container = document.getElementById('interestsGrid');

                        if (allFields.length === 0) {
                                container.innerHTML = '<div class="no-results"><p>No interests to show yet.</p></div>';
                                return;
                        }

                        let html = '';
                        allFields.forEach(field => {
                                html += `
                                        <div class="interest-card" data-field-id="${field.id}">
                                                <h3><i class="${field.icon}"></i> ${escapeHtml(field.title)}</h3>
                                                <p class="interest-intro">${escapeHtml(field.intro)}</p>
                                                <span class="learn-more-btn">Learn More <i class="fas fa-arrow-right"></i></span>
                                        </div>
                                `;
                        });
                        container.innerHTML = html;

                        container.querySelectorAll('.interest-card').forEach(card => {
                                card.addEventListener('click', function() {
                                        const fieldId = this.getAttribute('data-field-id');
                                        showFieldDetail(fieldId);
                                });
                        });
                }

                function iconForLinkType(type) {
                        switch (type) {
                                case 'course': return 'fas fa-graduation-cap';
                                case 'paper': return 'fas fa-file-alt';
                                case 'article': return 'fas fa-newspaper';
                                default: return 'fas fa-link';
                        }
                }

                function showFieldDetail(fieldId) {
                        const field = allFields.find(f => f.id === fieldId);
                        if (!field) {
                                console.error('Field not found:', fieldId);
                                return;
                        }

                        const topicsHtml = field.advancedTopics.map(topic => `<li>${escapeHtml(topic)}</li>`).join('');
                        const linksHtml = field.links.map(link => `
                                <li><a href="${link.url}" target="_blank" rel="noopener noreferrer"><i class="${iconForLinkType(link.type)}"></i> ${escapeHtml(link.label)}</a></li>
                        `).join('');

                        document.getElementById('interestDetailContent').innerHTML = `
                                <h1><i class="${field.icon}"></i> ${escapeHtml(field.title)}</h1>
                                <p>${escapeHtml(field.intro)}</p>
                                <h2>Advanced & Applied Topics</h2>
                                <ul>${topicsHtml}</ul>
                                <h2>Go Deeper</h2>
                                <ul class="interest-links">${linksHtml}</ul>
                        `;

                        const modal = document.getElementById('interestModal');
                        modal.classList.add('active');
                        document.body.style.overflow = 'hidden';
                }

                function closeInterestModal() {
                        document.getElementById('interestModal').classList.remove('active');
                        document.body.style.overflow = '';
                }

                document.getElementById('interestModal').addEventListener('click', (e) => {
                        if (e.target.id === 'interestModal') {
                                closeInterestModal();
                        }
                });

                document.addEventListener('keydown', (e) => {
                        if (e.key === 'Escape') {
                                closeInterestModal();
                        }
                });

                function escapeHtml(text) {
                        const div = document.createElement('div');
                        div.textContent = text;
                        return div.innerHTML;
                }

                document.addEventListener('DOMContentLoaded', loadFields);
        </script>
```

- [ ] **Step 3: Verify end-to-end in a browser**

Run: `python3 -m http.server 8000` (from repo root, if not already running)
Open `http://localhost:8000/interests.html` in a browser (use the claude-in-chrome tooling if available in this session to actually click through it; otherwise open manually and report what you see — do not claim this step passed without having actually observed it).

Check each of the following and confirm before moving on:
- The 4 cards render (Robotics, Machine Learning, Blockchain, IoT), each with its icon, DRAFT intro text, and a "Learn More" pill.
- Clicking anywhere on a card opens the modal, showing that field's title, intro, "Advanced & Applied Topics" list, and "Go Deeper" links list.
- The "Go Deeper" link opens `https://example.com` in a new tab (expected, since link content is still placeholder).
- Pressing `Escape` closes the modal.
- Clicking the dark overlay outside the modal panel closes it.
- Clicking the `×` close button closes it.
- Resizing the browser to under 768px width collapses the grid to a single column.
- No errors in the browser console.

- [ ] **Step 4: Commit**

```bash
git add interests.html
git commit -m "Wire up interests.html data fetch, card rendering, and detail modal"
```

---

### Task 5: Add the "Interests" nav link to all 6 existing pages

**Files:**
- Modify: `index.html`
- Modify: `news.html`
- Modify: `innovation.html`
- Modify: `projects.html`
- Modify: `resources.html`
- Modify: `learn.html`

Every one of these files has the identical nav block:

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

- [ ] **Step 1: Confirm the exact match count before editing**

Run: `grep -c '<li><a href="learn.html">Learn</a></li>' index.html news.html innovation.html projects.html resources.html learn.html`
Expected: each of the 6 files reports `1` (one match each) — confirms the anchor line for the edit exists exactly once per file before you start.

- [ ] **Step 2: Edit each file**

In each of the 6 files, find:

```html
                        <li><a href="learn.html">Learn</a></li>
                        <li><a href="index.html#footer">Contacts</a></li>
```

Replace with:

```html
                        <li><a href="learn.html">Learn</a></li>
                        <li><a href="interests.html">Interests</a></li>
                        <li><a href="index.html#footer">Contacts</a></li>
```

Apply this identical one-line insertion to `index.html`, `news.html`, `innovation.html`, `projects.html`, `resources.html`, and `learn.html`.

- [ ] **Step 3: Verify the insertion landed in all 6 files, and nowhere else**

Run: `grep -c '<li><a href="interests.html">Interests</a></li>' index.html news.html innovation.html projects.html resources.html learn.html interests.html`
Expected: each of the 7 files (the 6 just edited, plus `interests.html` itself from Task 2) reports `1`.

- [ ] **Step 4: Confirm `innovation.html`'s only diff is the nav line**

Run: `git diff innovation.html`
Expected: the diff shows exactly the 3-line nav hunk from Step 2 (one added line, two lines of context) and nothing else — no changes to "Areas of Innovation," "Current Innovation Projects," or the "Share Your Innovation Ideas" form. If the diff shows anything else, stop and investigate before committing.

- [ ] **Step 5: Spot-check in a browser**

With the local server still running from Task 4 (`python3 -m http.server 8000`), open `http://localhost:8000/innovation.html` and `http://localhost:8000/index.html`.
Expected: the nav menu on each now includes "Interests" between "Learn" and "Contacts," and clicking it navigates to `interests.html`.

- [ ] **Step 6: Commit**

```bash
git add index.html news.html innovation.html projects.html resources.html learn.html
git commit -m "Add Interests nav link to all existing pages"
```

---

### Task 6: Final verification against the spec's Testing checklist

**Files:** none (verification only)

- [ ] **Step 1: Confirm the full nav is consistent across all 7 pages**

Run: `grep -A9 '<ul class="links">' index.html news.html innovation.html projects.html resources.html learn.html interests.html`
Expected: all 7 files show the identical 8-item list (Home, News, Let's Innovate, Projects, Resources, Learn, Interests, Contacts) in the same order.

- [ ] **Step 2: Re-confirm `innovation.html`'s content is untouched**

Run: `git diff main -- innovation.html` (or `git diff <base-branch> -- innovation.html` if the branch was cut from something other than `main`)
Expected: only the one-line nav addition appears in the diff — no other lines changed.

- [ ] **Step 3: Re-run the JSON validation**

Run: `python3 -m json.tool assets/interests/index.json`
Expected: still valid, no errors.

- [ ] **Step 4: Full manual pass in a browser**

With the local server running, click through `interests.html` one more time end-to-end (cards → modal → close via all three methods → mobile-width layout), and click "Interests" from at least two other pages' nav menus to confirm the link works site-wide.

- [ ] **Step 5: Flag the placeholder content for review**

This plan intentionally ships DRAFT placeholder content (per the spec's Content section) — the banner text, section subtext, and all 4 JSON records' intros/topics/links. **Before this branch is merged, tell the site owner explicitly which files contain DRAFT text** (`interests.html`'s banner/section-header copy, and every field in `assets/interests/index.json`) so they can review and replace it. Do not represent this task as "content complete" — only "mechanism complete, content pending owner review."

- [ ] **Step 6: Stop the local server**

If still running, stop it with `Ctrl+C` in its terminal.
