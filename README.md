<div align="center">

```
┌──────────────────────────────────────────────────────────────────┐
│  ●  ●  ●   setu-agent — trace: identify(user="Dhairya2112")       │
└──────────────────────────────────────────────────────────────────┘
```

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=17&duration=2800&pause=900&color=A855F7&center=true&vCenter=true&width=680&lines=%3E+QUERY%3A+%22who+is+dhairya_dave%2C+and+what+has+he+built%3F%22;%3E+routing+to+setu-agent+(self-hosted+ReAct+loop)...;%3E+reasoning..." alt="Typing SVG" />
</a>

</div>

<br/>

> **Thought 1 —** I don't know this user yet. I should pull core identity before anything else.
> **Action —** `get_identity(user="Dhairya2112")`
> **Observation:**

```yaml
name        : Dhairya Dave Amitkumar
role        : AI Engineer / ML Engineer (aspiring)
education   : B.Tech CSE — L.J. University, Sem 5 (Class of 2028, SPI 8.83)
location    : Ahmedabad, Gujarat, IN
build_style : industry-grade > assignment-grade
              unique systems > templated projects
```

<br/>

> **Thought 2 —** Identity alone doesn't say what he can actually build. Need his real capability set, not a buzzword list.
> **Action —** `get_capabilities(verified_only=true)`
> **Observation:**

| Layer | Confirmed |
|---|---|
| `languages` | Python · Java · JavaScript (ES6+) · C++ · SQL |
| `backend` | Django · DRF · Flask · JDBC |
| `data` | PostgreSQL · MySQL · MongoDB |
| `ml_ai` | PyTorch · scikit-learn · LangChain · LangGraph |
| `analysis` | pandas · NumPy · Matplotlib · Seaborn · NetworkX |
| `automation` | pdfplumber · reportlab · pypdf |
| `foundations` | DSA · OOP · Relational Schema Design |

<br/>

> **Thought 3 —** Capability claims mean nothing without shipped systems. Pulling deployed projects to verify.
> **Action —** `list_repositories(status="deployed")`
> **Observation — 3 records found:**

```
◆ case_01 · setu-workstation
──────────────────────────────────────────────────────────────────
  type      local-first, LAN-only AI automation agent
  core      stateful ReAct agent (LangGraph) · 19 tools
            → 15 OS-level + 4 Playwright browser automations
  reliability   self-healing terminal error-recovery loop
  voice     custom faster-whisper STT · VAD · phonetic correction
  serving   Django + React PWA over WebSockets, cross-device
  inference Llama-3.3-70B → Gemma-4-31B → Gemini-2.5-Flash
            (3-layer fallback, in-memory response cache)
```

```
◆ case_02 · finvest
──────────────────────────────────────────────────────────────────
  type      personal finance & investment portfolio platform
  tracks    income/expense w/ categories · multi-asset portfolio
            (stocks, bonds, crypto, real estate, gold, cash, vehicles)
  computes  real-time P&L · diversification & risk scoring
  budgeting monthly limits + isolated event-based budgets
  surface   glassmorphism UI · dark/light mode · live charts
  stack     Flask · MySQL · Bootstrap 5 · Matplotlib
```

```
◆ case_03 · hotel-management-system
──────────────────────────────────────────────────────────────────
  type      hotel + cafe operations manager
  handles   guest records · room allocation · check-in/check-out
  cafe      menu display · price-sort · name-search · billing
  dsa       ArrayList-based sort/search over cafe + order data
  persist   JDBC → PostgreSQL, relational schema
  paradigm  OOP — encapsulation, abstraction, modularity
```

<br/>

> **Thought 4 —** Should back this with live metrics. Pulling from GitHub directly — but the platform's raw "commits" stat counts cross-branch events, not contribution-graph totals, so I'm excluding it to avoid reporting a misleading number.
> **Action —** `fetch_github_metrics(hide=["commits"])`
> **Observation:**

<div align="center">
<img width="49%" src="https://github-readme-stats.vercel.app/api?username=Dhairya2112&show_icons=true&hide=commits&theme=radical&hide_border=true&bg_color=0D0417&title_color=A855F7&icon_color=A855F7&text_color=c9d1d9"/>
<img width="49%" src="https://github-readme-stats.vercel.app/api/top-langs/?username=Dhairya2112&layout=compact&theme=radical&hide_border=true&bg_color=0D0417&title_color=A855F7&text_color=c9d1d9"/>
</div>

<div align="center">
<img width="70%" src="https://github-readme-streak-stats.herokuapp.com/?user=Dhairya2112&theme=highcontrast&hide_border=true&background=0D0417&stroke=A855F7&ring=A855F7&fire=A855F7&currStreakLabel=A855F7"/>
</div>

<br/>

> **Final Answer —**
> Dhairya is a pre-final-year CSE student who builds full production systems, not tutorial clones — a self-healing AI agent with voice I/O, a full-stack fintech portfolio tracker, and a relational ops system in Java, each shipped end to end. Currently open to AI/ML engineering internships and roles.

```
[trace complete]  tools_called=4  cases_verified=3  confidence=0.97
```

<div align="center">

<a href="https://www.linkedin.com/in/dhairya-dave-077773340/">
  <img src="https://img.shields.io/badge/respond_to_user()→-LinkedIn-0D0417?style=for-the-badge&logo=linkedin&logoColor=A855F7"/>
</a>
<a href="https://github.com/Dhairya2112">
  <img src="https://img.shields.io/badge/respond_to_user()→-GitHub-0D0417?style=for-the-badge&logo=github&logoColor=A855F7"/>
</a>

<br/><br/>

<sub>runtime idle · will resume on next incoming query · also accepts Clash Royale meta debates 👑</sub>

</div>
