# Ruichen Xu — Academic Website

Source for [ru1ch3n.github.io](https://ru1ch3n.github.io/), a compact, dependency-free academic website.

The September 2026 redesign takes its layout cues from [Chenyu You’s academic homepage](https://chenyuyou.me/): grouped side navigation, serif typography, restrained blue links, ruled section headings, and dense research and publication lists. The implementation is original, responsive semantic HTML and CSS.

## Structure

- `index.html` — profile, introduction, research, recent news, and selected publications
- `research.html` — research topics and projects
- `papers.html` — arXiv preprints, publications, and submitted manuscripts
- `teaching.html` — teaching and mentoring
- `bio.html` — biography, education, experience, talks, and service
- `news.html` — research timeline
- `assets/academic.css` — shared responsive academic layout
- `assets/Ruichen_Xu_CV.pdf` — current curriculum vitae
- `data/papers.json` — 18 bibliography records, including 5 arXiv preprints and 1 submitted manuscript
- `data/news.json` — news records migrated from the existing site
- `data/service.json` — conference, journal, and workshop reviewing, plus the ICML 2026 Gold Reviewer recognition
- `assets/papers/` — one source figure for every publication and manuscript
- `data/figure-sources.json` — figure numbers, source versions, and provenance
- `scripts/build_site.py` — shared navigation, page copy, and static HTML renderer

## Editing

Edit publication and news records in `data/`. Edit other page copy and shared navigation in `scripts/build_site.py`, then run:

```bash
python scripts/build_site.py
```

Each paper’s `figure` record contains its local image path, dimensions, descriptive alt text, and display label. Figures appear beside the citation and open at full size. The active-learning visual is explicitly labeled as an author-poster overview; the other images come from the papers or their author manuscripts. Preserve this distinction when replacing an image. GAGA is listed under its published title, while the original `iaga` anchor remains stable.

Public arXiv records link to both their abstract and PDF. The earlier VI-HNN preprint and its later NYSDS proceedings paper have different titles and author lists and are explicitly distinguished. JENO links to the actual OpenReview submission with an access note and manuscript-request link; no arXiv identifier or public access is implied. Paper announcements in the news carry direct paper links, with additional arXiv links where available.

News uses bracketed year-month dates, colored category labels, and aligned announcement text following the reference homepage. The home page’s news list scrolls within a 480-pixel window; the news archive shows the full timeline.

Commit the generated root HTML along with the source changes. GitHub Pages continues to serve the root files directly; no framework, JavaScript runtime, or CI build is needed. All primary content and navigation work with JavaScript disabled.

For the private review Site, `python scripts/build_site.py --stage` also copies the published files into the ignored `dist/` directory. The Sites manifest selects that output directory. The canonical public URLs remain on `ru1ch3n.github.io`.

The `research.html#publications` anchor remains as a link to the dedicated publication page. Existing PDFs, images, and the separate `pdeobs/` benchmark site are preserved. Submission and reviewing roles use the CV and confirmed correspondence; public preprint metadata comes from arXiv. No acceptance outcomes or completed-review totals are inferred.

## Local preview

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

The redesign has no analytics, trackers, third-party font dependency, or runtime content fetches. Mobile navigation wraps above the content; desktop navigation stays in the left column. Print styles keep the research record readable.
