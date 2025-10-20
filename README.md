# Personal Website Update (Data‑Driven Sections)

This package updates three parts of your site:
1. **Introduction** — richer description of your current research.
2. **Papers** — each item shows a direct paper link when available; if missing, it automatically shows the **homepage of the journal/conference**.
3. **News** — a **single merged feed** (paper announcements + other news), **ordered by time (newest first)**. Each news item includes a link.

## How to Edit

- Edit `data/intro.json` → `html` field accepts HTML (you can paste formatted text).
- Edit `data/papers.json` — for each paper:
  - Set `"url"` to the paper (arXiv/DOI/proceedings/publisher).
  - If you don’t have a paper link yet, set `"venue_url"` to the homepage of the journal/conference (fallback used automatically).
  - Optional: `"badges"` shows small tags under the entry.
- Edit `data/news.json` — each item needs:
  - `"date"` (YYYY-MM-DD),
  - `"text"` (one‑line summary),
  - `"link"` and `"link_text"` (if the paper isn’t online, set the link to the venue homepage).
  - `"tag"` (e.g., Paper, Submission, Talk, Award).

## Drop-In Usage

You can copy this folder into your site (e.g., `ru1ch3n.github.io/`), or merge files into your existing structure:
- Place `index.html` at the root or merge the `<section>` blocks into your template.
- Keep `assets/style.css` and `assets/script.js` paths consistent.
- Keep the three JSON files in `/data` (or update the paths in `assets/script.js`).

## Notes

- All example entries are **placeholders**—please replace titles, authors, and links with your latest records.
- The viewer will **prefer the paper link** (`url`), otherwise it **falls back** to `venue_url`.
