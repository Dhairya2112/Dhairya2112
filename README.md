<img src="https://raw.githubusercontent.com/Dhairya2112/Dhairya2112/assets/hero.svg" alt="Dhairya Dave, AI/ML and backend engineering, open to internships. I train ML models on raw, messy data and build the Django backends that serve them. Right now I'm building Setu, a local-first agent that runs on a LAN. Setu runtime values: VAD threshold 0.35, STT logprob -1.50, 13 agent tools, 3 LLM fallback layers." width="840">

Third-year CSE student at L.J. University, Ahmedabad, graduating 2028.

<sub>[systems](#systems)&emsp;[telemetry](#telemetry)&emsp;[signal](#signal)&emsp;[contact](#contact)</sub>

## systems

<details open>
<summary><b>setu-workstation</b>&emsp;local-first, LAN-only AI automation agent</summary>

<br>

```text
mic ─► Silero VAD ─► faster-whisper large-v3-turbo (int8, CPU)
                     English + Hindi/Hinglish, wake word "setu"
                                     │
        tier 0   regex router                <0.3 s   greetings, thanks, farewells
        tier 2   LangGraph ReAct agent       2-8 s    13 tools + Playwright browser sub-agent
                                     │
        LLM chain   Gemini 10 s ─► OpenRouter 6 s ─► NVIDIA NIM 5 s
                                     │
Kokoro TTS, local ─► base64 WAV chunks, streamed sentence by sentence
                                     │
Django 6 + Channels (Daphne, JWT WebSocket) ─► React 19 and Three.js client
```

- Runs on the local network only. Three permission levels gate the tools, and a safety layer blocks destructive shell patterns and restricts file paths.
- Tokens stream to the client, the desktop can cancel a reply mid-stream, and several devices stay in sync. A phone disconnecting does not cancel a running task.
- Speech settings: VAD threshold 0.35, minimum speech 200 ms, minimum silence 400 ms, logprob gate -1.50, beam size 5.

<!-- add the repository link here once it is public -->

</details>

<details>
<summary><b>finvest-v2</b>&emsp;personal finance platform, deployed</summary>

<br>

Next.js 16 and React 19 front end, Flask and Supabase (PostgreSQL) back end. Google OAuth 2.0 sign-in, a receipt splitter that reads photos with Gemini Vision OCR, live multi-currency exchange rates, and PWA support.

[source](https://github.com/Dhairya2112/FinVest-Financial-Buddy)&emsp;[live](https://finvest-financial-buddy.vercel.app)

</details>

<details>
<summary><b>signalscope</b>&emsp;forensic detector for AI-generated images and deepfakes</summary>

<br>

Two detectors run side by side and a consensus gate makes the call. One uses CLIP ViT-B/16 to catch semantic and visual inconsistencies. The other reads camera physics: 2D-FFT azimuthal power decay and SRM sensor-noise residuals. The gate suppresses false positives from smartphone portrait mode, night mode and beauty filters, and every verdict carries a calibrated confidence tier. FastAPI back end, React 18 dashboard.

Built for Smart India Hackathon 2026. 8th of 108 teams in the college round.

<!-- add the repository link here -->

</details>

<details>
<summary><b>archive</b>&emsp;earlier work</summary>

<br>

Hotel and cafe management system in Java, PostgreSQL and JDBC, with hand-written sorting and searching algorithms.

</details>

<details>
<summary><b>stack</b>&emsp;what I use, and what I am still learning</summary>

<br>

```text
languages  Python, JavaScript, SQL, Java
back end   Django, DRF, Flask, FastAPI, Express
front end  React, Next.js, Vite, Tailwind CSS
ml         PyTorch, scikit-learn, pandas, NumPy, LangChain, LangGraph
data       PostgreSQL, MySQL, MongoDB, Supabase
learning   Docker, AWS, GCP
```

</details>

## telemetry

<img src="https://raw.githubusercontent.com/Dhairya2112/Dhairya2112/assets/telemetry.svg" alt="GitHub activity for the last 12 weeks, language share by bytes, and repository counts. Regenerated every six hours from the GitHub API." width="840">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Dhairya2112/Dhairya2112/output/github-contribution-grid-snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Dhairya2112/Dhairya2112/output/github-contribution-grid-snake.svg">
  <img alt="Contribution graph with a snake eating the commits" src="https://raw.githubusercontent.com/Dhairya2112/Dhairya2112/output/github-contribution-grid-snake-dark.svg">
</picture>

## signal

<img src="https://raw.githubusercontent.com/Dhairya2112/Dhairya2112/assets/signals.svg" alt="Signal board: the latest one-line messages left by visitors." width="840">

[Post a signal](https://github.com/Dhairya2112/Dhairya2112/issues/new?template=signal.yml)

One line, 72 characters, plain ASCII, no links. It appears on the board about a minute after you submit.

## contact

Email: [davedhairya21@gmail.com](mailto:davedhairya21@gmail.com)  
LinkedIn: [dhairya-dave-077773340](https://www.linkedin.com/in/dhairya-dave-077773340/)  
Resume: [PDF](resume/Dhairya_Dave_Resume.pdf)
