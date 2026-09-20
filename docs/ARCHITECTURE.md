# Architecture

Not shown on the profile. GitHub only renders `README.md`; everything else in this repo exists to build the three images it embeds.

## Rule

SVG is the display layer. Markdown is the interaction layer. GitHub strips JS and CSS from READMEs and does not deliver hover or clicks inside an `<img>`, so every link, every `<details>` and the signal form live in `README.md`. The SVGs only draw.

## Page layout (840 px design width, scaled down by GitHub)

```
L1  hero.svg        840x328, generated
    +-----------------+  open to internships                 (status, amber dot)
    | ASCII portrait  |  Dhairya Dave                        (outlined Space Grotesk Bold, 56)
    | 280x280, 6 px   |  AI/ML and backend engineering       (amber, 16)
    | text, revealed  |  three-line pitch                    (14)
    | row by row once |  ---------------------------------
    | in ~1.5 s       |  setu-workstation runtime values
    +-----------------+  vad threshold | stt logprob | agent tools | llm fallback
L2  plain text      one line: education. one line: anchor links.
L3  systems         <details> rows: setu (open), finvest-v2, signalscope, archive, stack
L4  telemetry.svg   840x216, rebuilt every 6 h
    activity bars (12 wk) | languages by bytes | repository facts | footer: source, synced time
    github-contribution-grid-snake*.svg   from snake.yml, `output` branch
L5  signals.svg     840x216, rebuilt when an issue is accepted
    latest 5 rows: time, github login (cyan), message
L6  contact         plain text, real links
```

Mobile: an 840 px image shows at about 0.45x on a phone. Anything critical is 16 px or larger (name, role). Small type is limited to labels and secondary data.

## Tokens (src/tokens.py)

| name | value | use |
| --- | --- | --- |
| ink | #0B0E14 | panel background |
| paper | #E8E6E1 | text, data marks |
| amber | #F5A623 | values, status, the current week, the snake |
| cyan | #3FA9F5 | visitor names only |
| slate | #5C6470 | hairlines |
| muted | #8B93A0 | secondary text (slate lightened for contrast) |

Type: JetBrains Mono (data, body) embedded as a subsetted woff2 in each SVG; Space Grotesk Bold for the name, converted to vector paths. Scale: 11, 12, 14, 16, 20, 56. One radius (10), 1 px hairlines, no shadows, no gradients.

Motion: one moment. The ASCII portrait reveals row by row on load (about 1.5 s). The status dot pulses three times. Both stop under `prefers-reduced-motion`.

## Portrait

`source/portrait.png` is a cut-out (transparent background) of the photo. Its alpha channel is the mask, so a busy backdrop never leaks into the picture. To use a new photo: remove the background with any tool (remove.bg, Photoshop, Canva, or `pip install rembg`), save as PNG in `source/`, then tune `zoom`, `focus_x`, `focus_y` and `fade_from` in `data/config.yml` until the face fills the box. A plain JPG also works (mode `auto`), but only if the wall behind you is plain.

Each row is pinned to its exact width with `textLength`, because Chrome on Linux rounds glyph widths and would otherwise stretch the picture. `style: particles` switches to the dot version.

## Data flow

```
schedule (6 h) / push to src|data|source / manual
        |
   render.yml:  fetch.py (GitHub API) -> build.py -> dist/{hero,telemetry,signals}.svg
        |                                                     |
        |                                          publish.sh: force-push to branch `assets`
        |
issue "signal: ..." opened from the form
        |
   signal.yml:  signal_update.py (validate) -> data/signals.json -> build.py -> publish.sh -> comment + close

snake.yml (daily) -> branch `output`   (separate branch, never touched by the above)
```

README images point at `raw.githubusercontent.com/<user>/<repo>/assets/...`. `assets` holds one commit at a time, so history never grows.

## Files

```
README.md                     the only file GitHub renders
data/config.yml               name, pitch, Setu values, portrait settings, limits
data/signals.json             stored signals (written by the workflow)
source/portrait.png           your cut-out photo
resume/                       your PDF (you add it)
src/build.py                  entry point: python -m src.build [--offline]
src/fetch.py                  GitHub API: activity, languages, repos
src/particles.py              photo -> ASCII rows or point cloud
src/svgkit.py                 font subsetting, outlined text, SVG document
src/panels/                   hero.py, telemetry.py, signals.py
src/signal_update.py          validates one issue and records it
src/publish.sh                orphan-commit push to `assets`
src/fonts/                    JetBrains Mono, Space Grotesk (SIL OFL, licences included)
.github/workflows/            render.yml, signal.yml, snake.yml
.github/ISSUE_TEMPLATE/       signal.yml (the form), config.yml
```

## Budgets

hero.svg under 150 KB, telemetry.svg and signals.svg under 60 KB each (build.py flags overruns). Currently about 71, 10 and 13 KB. No third-party image services.

## Signal board rules

72 characters, printable ASCII only, no links or email addresses, one per visitor per 24 hours (you are exempt), no repeats of the last five lines. Bots are rejected. The issue text only reaches the script through environment variables. To remove an entry, delete it from `data/signals.json` and run `render`.

## Local preview

```
pip install -r requirements.txt
python -m src.build --offline      # sample numbers, no API calls
```

Open the files in `dist/` in a browser. With `GH_TOKEN` set, it uses real data.

## Known limits

- Fonts are embedded as data URIs. If GitHub ever blocks them, text falls back to the system monospace stack; the name is vector and unaffected.
- `raw.githubusercontent.com` caches for about 5 minutes, so panels can lag a few minutes behind a build.
- Two signal issues opened within seconds can leave one unprocessed (Actions keeps one pending run per concurrency group). Re-run that workflow from the Actions tab.
- Scheduled workflows are paused by GitHub after 60 days without repo activity. Any commit to `main` re-enables them.
