# Architecture

Technical architecture of the automated profile portfolio. GitHub renders `README.md`; the scripts in `src/` generate the display panels.

## Rule

SVG is the display layer. Markdown is the interaction layer. GitHub strips JS and CSS from READMEs and does not deliver hover or clicks inside an `<img>`, so all hyperlinks, `<details>` drawers, and deployment tables live in `README.md`. The SVGs only draw.

## Page layout (840 px design width, scaled down by GitHub)

```
L1  hero.svg        840x328, generated
    +-----------------+  open to internships & engineering roles (status, amber dot)
    | ASCII portrait  |  Dhairya Dave                            (outlined Space Grotesk Bold, 56)
    | 280x280, 6 px   |  Software & AI Systems Engineer          (amber, 16)
    | text, revealed  |  three-line engineering pitch            (14)
    | row by row once |  -------------------------------------
    | in ~1.5 s       |  core engineering stack (3 pillars)
    +-----------------+  ai & agents | async backend | cloud & data
L2  plain text      education, role targets, anchor navigation
L3  systems         <details> rows: setu-workstation (open), signalscope, finvest-v2, archive
L4  deployments     markdown table: live cloud demos, Vercel, and local systems
L5  telemetry.svg   840x216, rebuilt every 6 h
    cadence (12 wk with avg baseline) | languages by bytes (stacked bar + chips) | systems metrics
    github-contribution-grid-snake*.svg   from snake.yml, `output` branch
L6  stack           clean taxonomy of languages, frameworks, AI/ML, databases, ops
L7  contact         plain text, real links
```

Mobile: an 840 px image shows at about 0.45x on a phone. Anything critical is 16 px or larger (name, role). Small type is limited to labels and secondary data.

## Tokens (src/tokens.py)

| name | value | use |
| --- | --- | --- |
| ink | #0B0E14 | panel background |
| paper | #E8E6E1 | text, data marks |
| amber | #F5A623 | values, status, the current week, the snake |
| cyan | #3FA9F5 | accents |
| slate | #5C6470 | hairlines, dividers |
| muted | #8B93A0 | secondary text (slate lightened for contrast) |

Type: JetBrains Mono (data, body) embedded as a subsetted woff2 in each SVG; Space Grotesk Bold for the name, converted to vector paths.

## Data flow

```
schedule (6 h) / push to src|data|source / workflow_dispatch
        |
   render.yml:  fetch.py (GitHub API) -> build.py -> dist/{hero,telemetry}.svg
        |                                                  |
        |                                       publish.sh: force-push to branch `assets`
        |
snake.yml (daily) -> branch `output`   (separate branch, never touched by the above)
```

README images point at `raw.githubusercontent.com/<user>/<repo>/assets/...`. `assets` holds one commit at a time, so history never grows.

## Files

```
README.md                     the only file GitHub renders
data/config.yml               name, pitch, stack values, portrait settings, telemetry limits
source/portrait.png           cut-out photo
resume/                       PDF resume
src/build.py                  entry point: python -m src.build [--offline]
src/fetch.py                  GitHub API: activity, languages, repos
src/particles.py              photo -> ASCII rows or point cloud
src/svgkit.py                 font subsetting, outlined text, SVG document
src/panels/                   hero.py, telemetry.py
src/publish.sh                orphan-commit push to `assets`
src/fonts/                    JetBrains Mono, Space Grotesk (SIL OFL)
.github/workflows/            render.yml, snake.yml
.github/ISSUE_TEMPLATE/       config.yml
```

## Budgets

hero.svg under 150 KB, telemetry.svg under 60 KB (build.py flags overruns). Currently ~20 KB and ~13 KB. No third-party image services.

## Local preview

```
pip install -r requirements.txt
python -m src.build --offline      # sample numbers, no API calls
```

Open the files in `dist/` in a browser. With `GH_TOKEN` set, it uses real data.
