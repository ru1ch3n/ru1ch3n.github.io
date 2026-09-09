# Ruichen Xu — Academic Website

Source for [ru1ch3n.github.io](https://ru1ch3n.github.io/), a compact, dependency-free academic website.

The September 2026 redesign takes its layout cues from [Chenyu You’s academic homepage](https://chenyuyou.me/): grouped side navigation, serif typography, restrained blue links, ruled section headings, and dense research and publication lists. The implementation is original, responsive semantic HTML and CSS.

## Structure

- `index.html` — profile, introduction, research, recent news, and selected publications
- `research.html` — research topics and projects
- `papers.html` — complete publication record, with manuscripts separated
- `teaching.html` — teaching and mentoring
- `bio.html` — biography, education, experience, talks, and service
- `news.html` — research timeline
- `assets/academic.css` — shared responsive academic layout
- `assets/Ruichen_Xu_CV.pdf` — current curriculum vitae
- `data/papers.json` — the 14 publication and manuscript records migrated from the existing site
- `data/news.json` — news records migrated from the existing site
- `scripts/build_site.py` — shared navigation, page copy, and static HTML renderer

## Editing

Edit publication and news records in `data/`. Edit other page copy and shared navigation in `scripts/build_site.py`, then run:

```bash
python scripts/build_site.py
```

Commit the generated root HTML along with the source changes. GitHub Pages continues to serve the root files directly; no framework, JavaScript runtime, or CI build is needed. All primary content and navigation work with JavaScript disabled.

For the private review Site, `python scripts/build_site.py --stage` also copies the published files into the ignored `dist/` directory. The Sites manifest selects that output directory. The canonical public URLs remain on `ru1ch3n.github.io`.

The `research.html#publications` anchor remains as a link to the dedicated publication page. Existing PDFs, images, and the separate `pdeobs/` benchmark site are preserved. Manuscripts are labeled without asserting current submission venues or acceptance. No new publication outcomes are inferred.

## Local preview

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

The redesign has no analytics, trackers, third-party font dependency, or runtime content fetches. Mobile navigation wraps above the content; desktop navigation stays in the left column. Print styles keep the research record readable.
