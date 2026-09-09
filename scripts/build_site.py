#!/usr/bin/env python3
"""Render dependency-free academic pages, then optionally stage a Sites preview.

Edit the page copy below and the shared records in data/. Generated root HTML is
committed so GitHub Pages can serve the website without a build workflow.
"""
from pathlib import Path
import argparse
import html
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
PAPERS = json.loads((ROOT / 'data/papers.json').read_text())
NEWS = json.loads((ROOT / 'data/news.json').read_text())
SERVICE = json.loads((ROOT / 'data/service.json').read_text())
ESC = html.escape
DATE = 'September 2026'
PROFILES = [
    ('Google Scholar', 'https://scholar.google.com/citations?user=IBXYwoQAAAAJ'),
    ('GitHub', 'https://github.com/ru1ch3n'),
    ('OpenReview', 'https://openreview.net/profile?id=~Ruichen_Xu2'),
    ('LinkedIn', 'https://www.linkedin.com/in/ruichen-xu-b30b55197/'),
    ('CV', 'assets/Ruichen_Xu_CV.pdf'),
]


def link(label, url):
    return f'<a href="{ESC(url, quote=True)}">{ESC(label)}</a>'


def profile_links():
    return '<ul class="profile-links" aria-label="Academic profiles">' + ''.join(
        f'<li>{link(label, url)}</li>' for label, url in PROFILES) + '</ul>'


def navigation(current):
    groups = [
        ('', [('Home', 'index.html'), ('Bio', 'bio.html'), ('Academic service', 'bio.html#service')]),
        ('Research', [('Topics', 'research.html'), ('Papers', 'papers.html')]),
        ('Teaching', [('Courses & mentoring', 'teaching.html')]),
        ('Updates', [('News', 'news.html'), ('Curriculum vitae', 'assets/Ruichen_Xu_CV.pdf')]),
    ]
    parts = []
    for heading, items in groups:
        items_html = ''.join(
            f'<li><a href="{href}"' + (' aria-current="page"' if href == current else '')
            + f'>{ESC(label)}</a></li>' for label, href in items)
        title = f'<div class="nav-heading">{heading}</div>' if heading else ''
        parts.append(f'<div class="nav-group">{title}<ul>{items_html}</ul></div>')
    return ''.join(parts)


def page(filename, title, description, body, home=False):
    canonical = 'https://ru1ch3n.github.io/' + ('' if home else filename)
    heading = 'Ruichen Xu <span class="name-cn" lang="zh">徐瑞辰</span>' if home else ESC(title)
    document_title = 'Ruichen Xu | Stony Brook University' if home else title + ' | Ruichen Xu'
    result = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{ESC(document_title)}</title>
  <meta name="description" content="{ESC(description, quote=True)}">
  <meta name="theme-color" content="#244f79">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{ESC(document_title, quote=True)}">
  <meta property="og:description" content="{ESC(description, quote=True)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://ru1ch3n.github.io/assets/profile.jpg">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/academic.css?v=20260909-service">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="site-layout">
  <aside class="sidebar">
    <a class="site-name" href="index.html">Ruichen Xu</a>
    <nav aria-label="Primary navigation">{navigation(filename)}</nav>
    <div class="nav-foot">Applied Mathematics<br>Stony Brook University</div>
  </aside>
  <main class="main" id="main" tabindex="-1">
    <header class="page-title"><h1>{heading}</h1></header>
    {body}
    <footer class="footer"><p>© 2026 Ruichen Xu · Updated {DATE}</p><p>{link('Email', 'mailto:ruichen.xu@stonybrook.edu')} · {link('CV', 'assets/Ruichen_Xu_CV.pdf')}</p></footer>
  </main>
</div>
</body>
</html>
'''
    (ROOT / filename).write_text('\n'.join(line.rstrip() for line in result.splitlines()) + '\n')


def paper_item(p, selected=False):
    title = link(p['title'], p['links'][0]['url']) if p['links'] else ESC(p['title'])
    links_html = ' '.join(link(x['label'], x['url']) for x in p['links'])
    # Keep unpublished manuscripts separate without announcing unverified venues.
    venue = p['venue'].replace(' · Accepted', '')
    identifier = 'selected-' + p['id'] if selected else p['id']
    figure = p.get('figure')
    figure_html = ''
    if figure:
        image_path = ESC(figure['path'], quote=True)
        figure_html = f'''<figure class="paper-figure">
          <a href="{image_path}" target="_blank" rel="noopener" aria-label="View {ESC(figure['label'], quote=True)} from {ESC(p['title'], quote=True)} at full size">
            <img src="{image_path}" alt="{ESC(figure['alt'], quote=True)}" width="{figure['width']}" height="{figure['height']}" loading="lazy" decoding="async">
          </a>
          <figcaption>{ESC(figure['label'])}</figcaption>
        </figure>'''
    return f'''<li class="paper{' paper-with-figure' if figure else ''}" id="{identifier}">
      {figure_html}
      <div class="paper-copy">
      <h3 class="paper-title">{title}</h3>
      <p class="authors">{p['authors_html']}</p>
      <p class="venue"><strong>{ESC(venue)}</strong></p>
      {f'<p class="small subtle">{ESC(p["note"])}</p>' if p.get('note') else ''}
      {f'<div class="paper-links">{links_html}</div>' if links_html else ''}
      </div>
    </li>'''


def paper_list(items, selected=False):
    return '<ol class="paper-list">' + '\n'.join(paper_item(p, selected) for p in items) + '</ol>'


def news_list(items):
    rows = []
    for n in items:
        rows.append(f'''<li><p>
          <span class="news-prefix"><span class="news-date">[{ESC(n['display_date'])}]</span>
          <span class="news-tag tag-{ESC(n['tag'].lower())}">{ESC(n['tag'])}</span></span>
          <span class="news-text">{n['html']}</span>
        </p></li>''')
    return '<ul class="news-list">' + '\n'.join(rows) + '</ul>'


def service_list(group):
    rows = []
    for item in SERVICE[group]:
        note = ' · ' + ESC(item['note']) if item.get('note') else ''
        rows.append(f'<li>{link(item["venue"], item["url"])} — {ESC(item["years"])}{note}</li>')
    return '<ul class="service-list">' + ''.join(rows) + '</ul>'


def recognition():
    award = SERVICE['recognition']
    return f'<p class="reviewer-recognition"><strong>{link(award["title"], award["url"])}</strong> · {ESC(award["date"])}<br><span class="small">{ESC(award["description"])}</span></p>'


def jump_links(items):
    return '<nav class="on-this-page" aria-label="On this page">' + ''.join(link(label, '#' + identifier) for label, identifier in items) + '</nav>'


def courses(rows, caption):
    return '<div class="table-wrap"><table class="courses"><caption>' + caption + '</caption><thead><tr><th scope="col">Course</th><th scope="col">Title</th><th scope="col" class="term">Term</th></tr></thead><tbody>' + ''.join(
        f'<tr><td class="code">{code}</td><td>{title}</td><td>{term}</td></tr>' for code, title, term in rows) + '</tbody></table></div>'


INTRO = '''<p>I am a Ph.D. candidate in <strong>Computational Applied Mathematics</strong> at <a href="https://www.stonybrook.edu/">Stony Brook University</a>, advised by <strong>Yuefan Deng</strong>. My research lies at the intersection of machine learning and scientific computing, with a focus on <strong>AI for Science</strong>.</p>
<p>I study how learning systems can use incomplete observations and physical structure to solve scientific problems. My work spans neural operators, predictive representation learning, physics-aware generative models, and LLM-guided optimization. I also teach applied mathematics and mentor student research at Stony Brook.</p>'''

home = f'''<section class="profile" aria-label="Profile and contact">
  <img class="profile-photo" src="assets/profile.jpg" alt="Ruichen Xu" width="864" height="1152" fetchpriority="high">
  <div>
    <p class="position">Ph.D. Candidate</p>
    <p class="affiliation">Computational Applied Mathematics<br><a href="https://www.stonybrook.edu/commcms/ams/">Department of Applied Mathematics &amp; Statistics</a><br><a href="https://www.stonybrook.edu/">Stony Brook University</a></p>
    <p class="contact-line">Also known as Bill Xu<br>{link('ruichen.xu@stonybrook.edu', 'mailto:ruichen.xu@stonybrook.edu')}</p>
    {profile_links()}
  </div>
</section>
<section aria-labelledby="introduction"><h2 id="introduction">Introduction</h2>{INTRO}</section>
<section aria-labelledby="research"><h2 id="research">Research</h2>
<ul class="research-list">
  <li><strong>Learning from partial observations.</strong> Neural operators and benchmarks for reconstructing PDE fields from sparse and irregular measurements.
  <span class="related">{link('PartialObs–PDEBench', 'research.html#partialobs')} · {link('Discretization mismatch', 'papers.html#discretization')}</span></li>
  <li><strong>Predictive representations for scientific data.</strong> Joint-embedding learning for PDE inference and multi-resolution graph representations.
  <span class="related">{link('JENO', 'https://openreview.net/forum?id=npUQDuAT7l')} · {link('HP-JEPA', 'https://arxiv.org/abs/2608.00491')}</span></li>
  <li><strong>Physics-aware generation and optimization.</strong> Diffusion, simulated annealing, and LLM-guided search for physical systems and molecular design.
  <span class="related">{link('APOD', 'research.html#generative')} · {link('RL-QESA', 'papers.html#rl-qesa')} · {link('Molecular optimization', 'research.html#molecules')}</span></li>
</ul></section>
<section aria-labelledby="news"><div class="section-top"><h2 id="news">News</h2>{link('All news', 'news.html')}</div>
<div class="news-window" tabindex="0" role="region" aria-label="Recent news, scroll for older updates">{news_list(NEWS)}</div></section>
<section aria-labelledby="selected-publications"><div class="section-top"><h2 id="selected-publications">Selected publications</h2>{link('All publications', 'papers.html')}</div>
{paper_list([next(p for p in PAPERS if p['id'] == identifier) for identifier in ['hp-jepa', 'iaga', 'multistep-backmapping', 'discretization', 'kar-hnn', 'apod', 'dsfno']], selected=True)}
</section>
<section aria-labelledby="academic-service"><div class="section-top"><h2 id="academic-service">Academic service</h2>{link('Reviewing experience', 'bio.html#service')}</div>
{recognition()}
<p><strong>Conference reviewer:</strong> {link('ICLR', 'https://iclr.cc/')} (2026, 2027), {link('ICML', 'https://icml.cc/Conferences/2026')} (2026), {link('NeurIPS', 'https://neurips.cc/Conferences/2026')} (2026), and {link('IJCNN', 'https://www.inns.org/ijcnn-home')} (2025, 2026).</p>
<p><strong>Journal reviewer:</strong> {link('TMLR', 'https://jmlr.org/tmlr/')} (2026), {link('IEEE TNNLS', 'https://cis.ieee.org/publications/t-neural-networks-and-learning-systems')} (2025), and {link('Neurocomputing', 'https://www.sciencedirect.com/journal/neurocomputing')} (2026).</p>
<p><strong>Workshop reviewer:</strong> {link('AI for Math @ ICML', 'https://openreview.net/group?id=ICML.cc/2025/Workshop/AI4MATH')} (2025).</p>
</section>'''
page('index.html', 'Home', 'Ruichen Xu (Bill Xu), Ph.D. candidate at Stony Brook University. Research in scientific machine learning, neural operators, generative models, and optimization.', home, home=True)

research = jump_links([('Partial observations', 'partialobs'), ('Representations', 'jepa'), ('Generative models', 'generative'), ('Molecular optimization', 'molecules'), ('Publications', 'publications')]) + '''
<p>My research connects machine learning with scientific computing. I am particularly interested in learning from partial observations, representing physical structure, and evaluating models through reproducible experiments.</p>
<section class="project" aria-labelledby="partialobs"><h2 id="partialobs">Partial observations &amp; neural operators</h2>
<p>Many scientific systems are observed through sparse sensors or incomplete measurements. I study neural operators and inference methods that recover full fields from these observations, and how their predictions change across resolutions and observation patterns.</p>
<h3>PartialObs–PDEBench</h3>
<p>A benchmark for sparse, irregular, sensor-style, and masked PDE observations. It brings together datasets, observation configurations, and evaluation metrics for neural operators, diffusion models, and physics-aware baselines.</p>
<p class="project-meta">2025–present · PDE learning · Partial observations · Benchmarking</p>
<p><a href="https://ru1ch3n.github.io/PartialObs--PDEBench/">Project website</a> · <a href="https://github.com/ru1ch3n/PartialObs--PDEBench">Code</a> · <a href="pdeobs/index.html">Benchmark resources</a></p>
<p class="small">Related papers: <a href="papers.html#discretization">Discretization mismatch in neural operators</a> · <a href="papers.html#dsfno">Dynamic Schwartz–Fourier Neural Operator</a> · <a href="papers.html#ctfno">Coordinate Transform FNO</a></p>
</section>
<section class="project" aria-labelledby="jepa"><h2 id="jepa">Predictive representation learning</h2>
<p>I investigate joint-embedding predictive architectures for scientific data, including student–teacher learning, latent full-field prediction, and representations across spatial resolutions.</p>
<ul>
<li><a href="https://openreview.net/forum?id=npUQDuAT7l"><strong>JENO.</strong></a> Full-field latent prediction for sparse inverse PDE inference.</li>
<li><a href="https://arxiv.org/abs/2608.00491"><strong>HP-JEPA.</strong></a> Hierarchical partitioning for multi-resolution graph joint-embedding predictive learning.</li>
</ul>
<p class="project-meta">2026–present · JEPA · PDE inference · Graph representation learning</p>
<p><a href="papers.html#preprints">arXiv preprints</a> · <a href="papers.html#manuscripts">Submitted manuscripts</a></p>
</section>
<section class="project" aria-labelledby="generative"><h2 id="generative">Physics-aware generation &amp; optimization</h2>
<p>I develop sampling and optimization methods that incorporate physical constraints, combining diffusion models, simulated annealing, and reinforcement learning.</p>
<ul>
<li><strong>APOD.</strong> Adaptive PDE-observation diffusion for physics-constrained sampling.</li>
<li><strong>RL-QESA.</strong> Reinforcement-learning quasi-equilibrium simulated annealing.</li>
<li><strong>Structure-aware dynamics.</strong> Hamiltonian and symplectic learning, including Kolmogorov–Arnold representations and learning dynamics from position-only observations.</li>
</ul>
<p><a href="papers.html#apod">APOD paper</a> · <a href="papers.html#rl-qesa">RL-QESA paper</a> · <a href="papers.html#kar-hnn">KAR-HNN paper</a> · <a href="papers.html#vihn">Position-only dynamics</a></p>
</section>
<section class="project" aria-labelledby="molecules"><h2 id="molecules">Molecular generation &amp; LLM-guided search</h2>
<p>My work in molecular design combines generative modeling and optimization under structural and validity constraints.</p>
<h3>ORACLE: LLM-guided molecular optimization</h3>
<p>LLM-proposed molecular edits are combined with simulated annealing for multi-objective structure-based drug design. Evaluation considers docking, QED, synthetic accessibility, diversity, and Pareto trade-offs.</p>
<p class="project-meta">2025–present · LLMs · Simulated annealing · Molecular design</p>
<p class="small">Related work: <a href="papers.html#iaga">GAGA: 3D molecular generation</a> · <a href="papers.html#multistep-backmapping">Generative backmapping of coarse-grained structures</a></p>
</section>
<section aria-labelledby="publications"><h2 id="publications">Publications</h2><p>See the <a href="papers.html">complete publication list</a> for arXiv preprints, conference, journal, and workshop papers, and submitted manuscripts.</p></section>
'''
page('research.html', 'Research topics', 'Research by Ruichen Xu: partial-observation PDE learning, predictive representations, physics-aware generation, and molecular optimization.', research)

groups = [('preprints', 'arXiv preprints', 'preprints'), ('conference', 'Conference & proceedings papers', 'conferences'), ('journals', 'Journal articles', 'journals'), ('workshops', 'Workshop papers', 'workshops'), ('manuscripts', 'Submitted manuscripts', 'manuscripts')]
papers_body = jump_links([(name, identifier) for _, name, identifier in groups])
papers_body += '<p>My publications in scientific machine learning, computational physics, dynamical systems, and molecular generation. See also ' + link('Google Scholar', PROFILES[0][1]) + ' and ' + link('OpenReview', PROFILES[2][1]) + '.</p>'
for category, title, identifier in groups:
    records = [p for p in PAPERS if p['category'] == category]
    records.sort(key=lambda p: p['year'] or 0, reverse=True)
    note = '<p class="small subtle">Unpublished work, listed separately from accepted and published papers.</p>' if category == 'manuscripts' else ''
    papers_body += f'<section aria-labelledby="{identifier}"><h2 id="{identifier}">{title}</h2>{note}{paper_list(records)}</section>'
page('papers.html', 'Publications', 'Publications and manuscripts by Ruichen Xu, including conference, journal, and workshop papers.', papers_body)

teaching = jump_links([('Instructor', 'instructor'), ('Teaching assistant', 'ta'), ('NYU Courant', 'nyu'), ('Mentoring', 'mentoring')]) + '''
<p>I teach applied mathematics, numerical methods, probability, statistics, and computing. My teaching connects mathematical intuition with implementation, and emphasizes clear reasoning and reproducible computational work.</p>
<section aria-labelledby="instructor"><h2 id="instructor">Instructor · Stony Brook University</h2>
<p>I designed and delivered lectures, created assessments, graded coursework, and supported students in the Department of Applied Mathematics &amp; Statistics.</p>
''' + courses([
    ('<a href="https://www.stonybrook.edu/ams/academics/undergraduate/ug-courses/ams-361.html">AMS 361</a>', 'Applied Calculus IV: Differential Equations', 'Winter 2026'),
    ('AMS 326', 'Numerical Analysis', 'Summer 2025'),
    ('AMS 394', 'Statistical Laboratory', 'Summer 2025<br>Summer 2024<br>Winter 2024<br>Winter 2023'),
], 'Courses taught as instructor') + '''</section>
<section aria-labelledby="ta"><h2 id="ta">Teaching assistant · Stony Brook University</h2>
<p>Responsibilities included recitations, discussions, office hours, and grading.</p>
''' + courses([
    ('AMS 528', 'Numerical Methods', 'Spring 2025'),
    ('AMS 502', 'Differential Equations and Boundary Value Problems', 'Spring 2025'),
    ('AMS 510', 'Analytical Methods for Applied Mathematics', 'Fall 2024'),
    ('AMS 595', 'Foundations of Computing', 'Fall 2024'),
    ('AMS 326', 'Numerical Analysis', 'Spring 2024'),
    ('AMS 310', 'Probability and Statistics', 'Spring 2023<br>Fall 2022'),
], 'Teaching assistant appointments') + '''</section>
<section aria-labelledby="nyu"><h2 id="nyu">Recitations &amp; grading · NYU Courant</h2>
<ul class="record-list">
<li><div><h3>Recitation leader</h3><p>Mathematics for Economics II — Spring 2021 and Spring 2022.<br>Probability, Statistics &amp; Decision Making — Fall 2021 and Spring 2022.</p><p class="small subtle">Recitations, office hours, and grading.</p></div><div class="period">2021–2022</div></li>
<li><div><h3>Grader</h3><p>Analysis — Fall 2020.<br>Special Topics — Fall 2021.</p></div><div class="period">2020–2021</div></li>
</ul></section>
<section aria-labelledby="mentoring"><h2 id="mentoring">Research mentoring</h2>
<h3>AI3 REU · Stony Brook University</h3>
<p class="small subtle">Summer 2026</p>
<p>I mentored AI4Science research projects from initial scoping through presentation, supporting literature review, experiment design, technical implementation, and reproducible workflows.</p>
<ul><li>Formulating focused research questions and planning experiments.</li><li>Organizing code, recording configurations, and tracking results.</li><li>Interpreting outcomes and preparing research presentations.</li></ul>
<p>For teaching or mentoring inquiries: <a href="mailto:ruichen.xu@stonybrook.edu">ruichen.xu@stonybrook.edu</a>.</p>
</section>'''
page('teaching.html', 'Teaching & mentoring', 'Ruichen Xu’s teaching and research mentoring at Stony Brook University and NYU Courant.', teaching)

bio = jump_links([('Biography', 'biography'), ('Education', 'education'), ('Experience', 'experience'), ('Reviewing & service', 'service')]) + '''
<section aria-labelledby="biography"><h2 id="biography">Biography</h2>
<p>Ruichen Xu (Bill Xu) is a Ph.D. candidate in Computational Applied Mathematics at Stony Brook University, advised by Yuefan Deng. His research focuses on scientific machine learning, including neural operators for partial observations and inverse problems, predictive representation learning, physics-aware generative models, and LLM-guided optimization.</p>
<p>He received an M.S. in Mathematics from the Courant Institute at New York University, an M.S. in Statistics from the University of California, Davis, and a bachelor’s degree in Financial Mathematics from Beijing University of Chemical Technology.</p>
<p>Alongside research, he teaches applied mathematics and mentors AI4Science projects at Stony Brook University. His work is supported by reproducible training and evaluation pipelines for large-scale experiments.</p>
<p><a href="assets/Ruichen_Xu_CV.pdf">Curriculum vitae (PDF)</a> · <a href="mailto:ruichen.xu@stonybrook.edu">Email</a></p>
</section>
<section aria-labelledby="education"><h2 id="education">Education</h2>
<ul class="record-list">
<li><div><h3>Stony Brook University</h3><p>Ph.D., Computational Applied Mathematics</p><p class="small subtle">GPA 4.00/4.00 · Stony Brook, New York</p></div><div class="period">2022–present<br>Expected 2027</div></li>
<li><div><h3>New York University · Courant Institute</h3><p>M.S., Mathematics</p><p class="small subtle">GPA 4.00/4.00 · New York, New York</p></div><div class="period">2020–2022</div></li>
<li><div><h3>University of California, Davis</h3><p>M.S., Statistics</p><p class="small subtle">GPA 3.94/4.00 · Davis, California</p></div><div class="period">2019–2020</div></li>
<li><div><h3>Beijing University of Chemical Technology</h3><p>Bachelor’s degree, Financial Mathematics<br>Minor in Commercial Management</p><p class="small subtle">Beijing, China</p></div><div class="period">2015–2019</div></li>
</ul></section>
<section aria-labelledby="experience"><h2 id="experience">Research &amp; teaching experience</h2>
<ul class="record-list">
<li><div><h3>REU research mentor · AI3</h3><p>Stony Brook University. Mentored AI4Science projects, including experiment design, implementation, reproducible workflows, and presentations.</p></div><div class="period">June–July 2026</div></li>
<li><div><h3>Instructor &amp; teaching assistant</h3><p>Department of Applied Mathematics &amp; Statistics, Stony Brook University.</p><p><a href="teaching.html">Courses and appointments</a></p></div><div class="period">2022–present</div></li>
<li><div><h3>Recitation leader &amp; grader</h3><p>Courant Institute, New York University.</p></div><div class="period">2020–2022</div></li>
</ul></section>
<section aria-labelledby="service"><h2 id="service">Reviewing &amp; academic service</h2>
''' + recognition() + '''
<h3>Conference reviewer</h3>
''' + service_list('conference_reviewing') + '''
<h3>Journal reviewer</h3>
''' + service_list('journal_reviewing') + '''
<h3>Workshop reviewer</h3>
''' + service_list('workshop_reviewing') + '''
<h3>Talks at IACS</h3>
<ul><li>AI for PDEs — IACS Student Seminar, 2025.</li><li>Diffusion4PDE — IACS lightning talk, 2025.</li><li>Active learning for neural operators — IACS lightning talk, 2024.</li></ul>
</section>'''
page('bio.html', 'Biography', 'Biography, education, experience, talks, and academic service of Ruichen Xu (Bill Xu).', bio)

news_body = '<p>Research, publications, reviewing, teaching, and mentoring updates.</p>'
news_body += jump_links([(str(year), 'year-' + str(year)) for year in [2026, 2025, 2024]])
for year in [2026, 2025, 2024]:
    news_body += f'<section aria-labelledby="year-{year}"><h2 id="year-{year}">{year}</h2>' + news_list([n for n in NEWS if str(year) in n['date']]) + '</section>'
page('news.html', 'News', 'Research, publication, teaching, and mentoring updates from Ruichen Xu.', news_body)

# Retain the legacy introductory record with the same current homepage copy.
(ROOT / 'data/intro.json').write_text(json.dumps({'html': INTRO}, ensure_ascii=False, indent=2) + '\n')
urls = ['https://ru1ch3n.github.io/' + ('' if name == 'index.html' else name) for name in ['index.html', 'bio.html', 'research.html', 'papers.html', 'teaching.html', 'news.html']]
(ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{url}</loc><lastmod>2026-09-09</lastmod></url>\n' for url in urls) + '</urlset>\n')

parser = argparse.ArgumentParser()
parser.add_argument('--stage', action='store_true', help='Copy the published site to dist/ for private review.')
args = parser.parse_args()
if args.stage:
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    for name in ['index.html', 'bio.html', 'research.html', 'papers.html', 'teaching.html', 'news.html', 'robots.txt', 'sitemap.xml', '.nojekyll']:
        shutil.copy2(ROOT / name, dist / name)
    for name in ['assets', 'data', 'pdeobs', 'personal_webpage_teaching_mentoring']:
        shutil.copytree(ROOT / name, dist / name, dirs_exist_ok=True)
    # Preserve existing downloadable archives and legacy public files.
    for name in ['personal_webpage_teaching_mentoring.zip', 'assets111', 'news.html.bak']:
        if (ROOT / name).is_file():
            shutil.copy2(ROOT / name, dist / name)
print('Rendered six academic pages' + (' and staged static output.' if args.stage else '.'))
