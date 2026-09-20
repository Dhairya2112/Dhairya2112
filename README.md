<img src="https://raw.githubusercontent.com/Dhairya2112/Dhairya2112/assets/hero.svg" alt="Dhairya Dave, Software & AI Systems Engineer. Architecting resilient backends and local-first agentic systems. Core stack: LangGraph, PyTorch, Django 6, FastAPI, PostgreSQL." width="840">

Third-year CSE student at L.J. University, Ahmedabad (Class of '28) • Targeting AI & Backend Engineering Roles

<sub>[systems](#systems)&emsp;[deployments](#deployments)&emsp;[telemetry](#telemetry)&emsp;[stack](#stack)&emsp;[contact](#contact)</sub>

## systems

<details open>
<summary><b>setu-workstation</b>&emsp;local-first, LAN-only autonomous voice operating system</summary>

<br>

```text
mic ──► Silero VAD (0.35 threshold) ──► faster-whisper large-v3-turbo (int8, CPU)
                                        English + Hindi/Hinglish, wake word "setu"
                                                        │
            tier 0   pre-compiled regex router          <0.3 s   greetings, status, immediate controls
            tier 2   LangGraph ReAct agent              2-8 s    14 sandboxed tools + Playwright sub-agent
                                                        │
            LLM resilience   Gemini 3.1 Flash Lite 10 s ──► OpenRouter Gemma 2 27B 6 s ──► NVIDIA NIM Llama 3.1 8B 5 s
                                                        │
Kokoro 0.7 TTS (neural, local) ──► base64 WAV chunks, streamed sentence-by-sentence
                                                        │
Django 6 + Channels (Daphne ASGI, JWT WebSocket) ──► React 19 + Zustand + Three.js NeuralMesh client
```

- **Bounded Checkpoint Memory:** Custom `BoundedMemorySaver` caps thread checkpoint history at 50 to prevent memory exhaustion, coupled with autonomous checkpoint healing to repair dangling tool states.
- **3-Layer Provider Fallback:** Exponential back-off via Tenacity across Gemini $\rightarrow$ OpenRouter $\rightarrow$ NVIDIA NIM to survive upstream rate limits and outages without user disruption.
- **Sub-300ms Fast Router:** Pre-compiled regex router (`FastResponseRouter`) handles greetings, time queries, and status commands instantly, completely bypassing the cloud LLM pipeline.
- **14 Sandboxed OS Tools:** Three privilege tiers gate host access (Level 1 read-only, Level 2 permission-gated, Level 3 administrative). Features native Windows WASAPI master volume control, process lifecycle management, filesystem search, and sandboxed PowerShell execution.
- **100% Local Audio Engine:** Raw microphone data never leaves the host. Silero VAD (0.35 threshold, 200 ms min speech, 400 ms min silence) + `faster-whisper` (int8 CPU) + `Kokoro 0.7` neural TTS streaming sentence chunks over WebSockets.
- **Data Persistence & Client:** MongoDB Community Server (`setu_db`) stores conversation history, settings, and reminders. Reactive React 19 client with Three.js `NeuralMesh` background visualizer and Web Audio API stream visualizer.

</details>

<details>
<summary><b>signalscope</b>&emsp;multi-modal forensic detection laboratory for AI-generated media & deepfakes</summary>

<br>

A full-stack forensic inspection laboratory built to detect AI-generated images, deepfakes, and adversarial face-swaps using a consensus between visual semantics and camera physics.

- **Dual-Brain Consensus Architecture:**
  - *Brain 1 (Visual Semantic AI):* CLIP ViT-B/16 transformer extracts semantic inconsistencies, geometric warping, and synthetic texture artifacts.
  - *Brain 2 (Camera Physics AI):* 2D Fast Fourier Transform (FFT) azimuthal power decay profile (detecting GAN/Diffusion checkerboard upsampling) coupled with Spatial Rich Model (SRM) sensor noise residuals & PRNU (Photo-Response Non-Uniformity) sensor grain verification.
- **Smartphone Computational Shield:** Autonomous gating model that isolates and suppresses false positives induced by modern smartphone computational photography (portrait mode blur, night mode, aggressive multi-frame HDR).
- **Four-Panel Forensic Laboratory:** LayerCAM visual saliency heatmaps with dynamic alpha blend slider, 2D-FFT azimuthal profile plots, generator family attribution (Midjourney, Stable Diffusion, DALL-E, StyleGAN), and EXIF camera provenance extraction.
- **Natural Language Diagnostics:** Real-time dynamic diagnostic summaries generated via the summary engine for non-technical evaluators and court admissibility.
- **Production & Testing:** FastAPI backend, React 18 + Vite dashboard, automated testing pipeline, and a 42-case test suite (`pytest`).
- **Recognition:** Smart India Hackathon (SIH 2026) Institutional Finalist — ranked 8th of 108 teams in college evaluation.

[live demo](http://18.212.83.78:8000)&emsp;[source](https://github.com/Dhairya2112/SignalScope)

</details>

<details>
<summary><b>finvest-v2</b>&emsp;personal finance platform, portfolio tracker & vision receipt splitter</summary>

<br>

Full-stack personal finance platform featuring isolated event-based budgeting, multi-asset portfolio tracking, and automated receipt itemization.

- **Architecture:** Next.js 16 + React 19 front end with dark glassmorphism design system; Flask backend backed by Supabase (PostgreSQL) with row-level security.
- **Vision OCR Splitter:** Leverages Gemini Vision OCR to scan, parse, and itemize physical paper receipts directly into category ledger entries.
- **Live Financial Data:** Real-time multi-currency exchange rate feeds and multi-asset P&L analytics with interactive charts.
- **Authentication & Delivery:** Google OAuth 2.0 authentication and Progressive Web App (PWA) offline support.

[live](https://finvest-financial-buddy.vercel.app)&emsp;[source](https://github.com/Dhairya2112/FinVest-Financial-Buddy)

</details>

<details>
<summary><b>archive</b>&emsp;earlier systems work</summary>

<br>

Hotel and cafe management system engineered in Core Java, PostgreSQL, and JDBC, implementing custom $O(n \log n)$ sorting and searching algorithms over dynamic data structures for real-time room allocations, menu operations, and automated billing.

</details>

## deployments

Live production deployments and active systems engineered by Dhairya Dave:

| System | Architecture / Focus | Primary Stack | Environment | Status | Links |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SignalScope** | Dual-Brain Forensic Vision (CLIP + 2D-FFT + SRM) | FastAPI • PyTorch • React 18 | Cloud Production | `● Live Demo` | [Live App](http://18.212.83.78:8000) • [Code](https://github.com/Dhairya2112/SignalScope) |
| **FinVest** | Automated Ledger & Vision OCR Expense Splitter | Flask • Next.js 16 • Supabase • Postgres | Vercel Serverless | `● Live Production` | [Live App](https://finvest-financial-buddy.vercel.app) • [Code](https://github.com/Dhairya2112/FinVest-Financial-Buddy) |
| **Setu Workstation** | Local-First Autonomous Voice OS Agent | Django 6 Channels • LangGraph • Whisper | Local-First Host (LAN) | `○ Workstation Active` | [Architecture](#systems) |

## telemetry

<a href="https://github.com/Dhairya2112?tab=repositories">
  <img src="https://raw.githubusercontent.com/Dhairya2112/Dhairya2112/assets/telemetry.svg" alt="GitHub activity for the last 12 weeks, language share by bytes, and repository counts. Regenerated every six hours from the GitHub API." width="840">
</a>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Dhairya2112/Dhairya2112/output/github-contribution-grid-snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Dhairya2112/Dhairya2112/output/github-contribution-grid-snake.svg">
  <img alt="Contribution graph with a snake eating the commits" src="https://raw.githubusercontent.com/Dhairya2112/Dhairya2112/output/github-contribution-grid-snake-dark.svg">
</picture>

## stack

```text
languages      Python, JavaScript/TypeScript, SQL, Java
ai / ml        PyTorch, LangGraph, LangChain, faster-whisper, Silero VAD, Kokoro TTS, CLIP ViT, scikit-learn
backends       Django 6 (Channels / Daphne ASGI), FastAPI, Flask, REST APIs, WebSockets
databases      PostgreSQL, MongoDB, Supabase, SQLite, MySQL
frontend       React 19, Next.js 16, Vite 8, Three.js (R3F), Tailwind CSS v4, Zustand 5
tooling & ops  Git, GitHub Actions, Linux/Bash, Postman, CI/CD
```

## contact

Email: [davedhairya21@gmail.com](mailto:davedhairya21@gmail.com)  
LinkedIn: [dhairya-dave-077773340](https://www.linkedin.com/in/dhairya-dave-077773340/)  
GitHub: [@Dhairya2112](https://github.com/Dhairya2112)  
Resume: [PDF](resume/Dhairya_Dave_Resume_Python_Developer.pdf)
