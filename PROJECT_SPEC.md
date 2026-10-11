# MarketPulse AI — Project Specification

Version: 1.0
Project Type: Student Portfolio / Educational Research Platform
Primary Goal: Financial, News, AI/NLP, Geopolitical and Market Intelligence
Status: Under Development

---

# 1. PROJECT OVERVIEW

## Project Name

MarketPulse AI

## Project Description

MarketPulse AI is a student-built financial and geopolitical intelligence platform designed to demonstrate how financial market data, news, sentiment analysis, natural language processing, macroeconomic information, geopolitical events and AI-assisted research can be combined into one unified research environment.

The platform is intended for:

- Educational purposes
- AI/ML demonstration
- Financial data analysis
- NLP experimentation
- Market research
- Geopolitical intelligence
- Data engineering demonstration
- Full-stack development demonstration
- Personal GitHub portfolio

The platform is NOT intended to function as:

- An investment adviser
- A broker
- A trading platform
- A portfolio manager
- A securities exchange
- A personalized financial advisory service
- A guaranteed prediction engine

The platform must not execute trades.

---

# 2. CORE PRODUCT IDEA

MarketPulse AI combines:

Market Data
+
News
+
Sentiment
+
Announcements
+
Macro Data
+
Geopolitical Events
+
AI/NLP
+
Analytics
+
Risk Scenarios

into:

MARKET INTELLIGENCE

The objective is not simply to display stock prices.

The objective is to help a user understand:

- What is happening in markets?
- What news is driving attention?
- What sentiment is present?
- Which sectors are receiving attention?
- What geopolitical events are relevant?
- Which companies or sectors may be exposed to those themes?
- What macroeconomic developments are occurring?
- What evidence supports an AI-generated research insight?
- What risks and uncertainties exist?

---

# 3. TARGET USER

Primary user:

A student, researcher, learner, analyst or technically curious user who wants to explore financial and geopolitical information.

The platform should remain understandable to a student and should be explainable during:

- College viva
- Technical interview
- GitHub project review
- Portfolio demonstration
- Academic presentation

---

# 4. PROJECT PHILOSOPHY

The project must prioritize:

1. Correctness
2. Explainability
3. Maintainability
4. Responsible AI
5. Free/no-cost operation
6. Clear data provenance
7. Good UI/UX
8. Educational value
9. Modular architecture
10. Reproducibility

Avoid unnecessary enterprise complexity.

Do not introduce technologies simply to make the architecture look impressive.

Every major technology should have a clear purpose.

---

# 5. PRIMARY FEATURES

The completed platform must contain:

- Landing page
- Animated disclaimer
- Overview dashboard
- Market intelligence
- Stock/company research
- News intelligence
- Sentiment analysis
- AI intelligence
- Geopolitical intelligence
- Announcements
- Macroeconomic dashboard
- Financial analytics
- Risk/scenario laboratory
- Research workspace
- Global search
- System/status page
- About/project information

---

# 6. LANDING PAGE

The landing page must be visually impressive.

It should feel like a premium financial intelligence application.

It must contain:

## Dynamic Greeting

The greeting should depend on the user's local time.

Examples:

Good Morning, Researcher.

Good Afternoon, Researcher.

Good Evening, Researcher.

## Hero Heading

SEE THE MARKET.
UNDERSTAND THE WORLD.

## Hero Description

MarketPulse AI connects market data, news, sentiment, announcements and geopolitical context into one research environment.

## Primary Actions

Explore Intelligence

View Markets

## System Indicators

Examples:

SYSTEM ONLINE

RESEARCH ENVIRONMENT

DEMO DATA

or:

FREE API DATA

The application must never falsely label demo data as live data.

---

# 7. DISCLAIMER

A disclaimer must appear when the application is opened for the first time.

The disclaimer should use an elegant animation.

Animation requirements:

- Fade-in backdrop
- Background blur
- Smooth card entrance
- Subtle icon animation
- Smooth text appearance
- Responsive mobile layout

The disclaimer must state that:

MarketPulse AI is an educational and research demonstration created as a student portfolio project.

It does not provide:

- Investment advice
- Personalized financial recommendations
- Guaranteed predictions
- Brokerage services
- Trade execution

Information may be:

- Delayed
- Incomplete
- Simulated
- Generated algorithmically
- Obtained from free/public sources

Users should verify information with authoritative sources.

The disclaimer must contain:

"I Understand"

The acknowledgement should be stored in localStorage.

After acknowledgement, it should not appear every time.

The user must still be able to reopen it from the System/About section.

---

# 8. RESPONSIBLE FINANCIAL LANGUAGE

The system must NEVER generate instructions such as:

- Buy XYZ
- Sell XYZ
- Hold XYZ
- Guaranteed return
- Guaranteed prediction
- This stock will rise
- This stock will fall
- You should invest in...

Instead use language such as:

- Market observation
- Research insight
- Potential exposure
- Historical relationship
- Observed trend
- Scenario
- Hypothetical impact
- Potential market relevance
- Research score
- Confidence
- Uncertainty

All AI insights must communicate uncertainty.

---

# 9. INDIAN MARKET CONTEXT

The platform should support Indian-market examples such as:

- NIFTY 50
- SENSEX
- NIFTY BANK
- NIFTY IT
- NIFTY ENERGY

Example securities may include:

RELIANCE
TCS
INFY
HDFCBANK
ICICIBANK
ITC
SBIN
BHARTIARTL
LT
HINDUNILVR

These are examples for educational demonstration.

Do not imply official affiliation with:

- NSE
- BSE
- SEBI
- RBI
- Any Indian government organization

Do not use official logos unless their use is legally appropriate.

---

# 10. FREE API REQUIREMENT

The project must be usable without spending money.

No paid API may be mandatory.

The application must work in:

DEMO MODE

without:

- API keys
- paid services
- cloud infrastructure
- paid databases
- paid LLMs

Free/public APIs can be optionally configured.

The system must not depend on one external provider.

---

# 11. PROVIDER ARCHITECTURE

Use an adapter/provider architecture.

Required interfaces:

MarketDataProvider

NewsProvider

MacroDataProvider

GeopoliticalProvider

AnnouncementProvider

Providers should be replaceable.

Example:

FreeMarketProvider

DemoMarketProvider

FreeNewsProvider

DemoNewsProvider

FreeMacroProvider

DemoMacroProvider

FreeGeopoliticalProvider

DemoGeopoliticalProvider

---

# 12. PROVIDER FALLBACK

The preferred data flow is:

Free API
    ↓
Validation
    ↓
Normalization
    ↓
Cache
    ↓
Demo fallback

If an external provider fails:

- Do not crash the application.
- Do not display misleading live data.
- Fall back to cached/demo data.
- Clearly indicate the source state.

Example:

DATA SOURCE: DEMO FALLBACK

or:

DATA SOURCE: FREE API

or:

DATA SOURCE: CACHED

---

# 13. DATA SOURCE TRANSPARENCY

Every externally sourced record should support:

- Provider
- Source
- Source URL when available
- Published timestamp
- Retrieved timestamp
- Data status
- Confidence where appropriate

The frontend should show data provenance.

Never fabricate URLs.

Never fabricate sources.

---

# 14. MARKET DATA

Market functionality should include:

- Market overview
- Stock/company search
- Quotes
- Historical prices
- Market indices
- Watchlist
- Sector information
- Market movers

Possible free/public providers may include:

- yfinance where appropriate
- Stooq
- other publicly accessible educational sources

Providers must be isolated behind adapters.

Do not assume any third-party API will remain free forever.

---

# 15. MARKET PAGE

The Markets page should include:

Search

Watchlist

Market overview

Indices

Top gainers

Top decliners

Most active

Stock/company detail

Price chart

Historical data

Technical indicators

Data source

Timestamp

Demo/live/free status

---

# 16. STOCK DETAIL

A stock/company detail view should display:

- Company name
- Symbol
- Sector
- Current/latest price
- Change
- Percentage change
- Volume when available
- Timestamp
- Provider
- Data status

Historical chart ranges:

- 1D
- 5D
- 1M
- 3M
- 6M
- 1Y

If a provider does not support a timeframe, clearly communicate that.

---

# 17. TECHNICAL ANALYTICS

Educational technical analytics should include:

- SMA
- EMA
- RSI
- MACD
- Momentum
- Volatility
- Maximum drawdown
- Returns
- Correlation
- Beta where sufficient data exists

These must be presented as analytical tools.

They must not be converted into automated investment recommendations.

---

# 18. NEWS INTELLIGENCE

The News page must provide:

- News feed
- Search
- Categories
- Date filtering
- Source filtering
- Sentiment filtering
- Importance filtering
- Entity association
- Topic association

Categories:

- Markets
- Economy
- Technology
- Finance
- Corporate
- Government
- International
- Geopolitics
- Energy

Each article should contain:

- Headline
- Source
- Published timestamp
- Summary
- Sentiment
- Importance
- Related entities
- Related topics
- Source URL when available

---

# 19. NEWS DATA SOURCES

Possible free/public sources include:

- RSS feeds
- GDELT
- Free/development news APIs where available
- Public government feeds
- Public corporate feeds

Provider implementations must be modular.

If a source requires an API key:

- It must be optional.
- Demo mode must still work.

---

# 20. SENTIMENT ANALYSIS

The platform should contain an NLP sentiment system.

Potential approaches:

- VADER
- TF-IDF
- scikit-learn classifier
- NLTK
- optional transformer model

The system should distinguish:

Positive

Neutral

Negative

It should provide:

- Sentiment score
- Sentiment distribution
- Sentiment trend
- Sector sentiment
- Topic sentiment
- Article-level sentiment

---

# 21. NLP PIPELINE

Possible pipeline:

Raw Text
↓
Cleaning
↓
Normalization
↓
Tokenization
↓
Stopword Handling
↓
Feature Representation
↓
Classification / Sentiment
↓
Aggregation
↓
Visualization

Possible feature representation:

TF-IDF

If additional embeddings are implemented, document their purpose.

Do not add unnecessarily large models.

---

# 22. MACHINE LEARNING

Where appropriate, use:

- scikit-learn
- pandas
- numpy
- NLTK

Possible models:

- Logistic Regression
- Naive Bayes
- Linear SVM

The system should be explainable.

Where trained models are used, document:

- Dataset
- Features
- Algorithm
- Training process
- Evaluation
- Accuracy
- Precision
- Recall
- F1-score
- Limitations

---

# 23. AI INTELLIGENCE PAGE

The AI page is one of the main platform features.

It should provide:

"What Matters Now?"

with research-oriented insights.

Possible sections:

- Market overview
- News themes
- Sentiment
- Geopolitical context
- Cross-domain relationships
- Risk factors
- Uncertainties

Every insight should contain:

Insight

Explanation

Evidence

Confidence

Uncertainty

Risk flags

Sources

---

# 24. AI RESEARCH ENGINE

The research engine must work without a paid LLM.

It may use:

- Deterministic rules
- Statistical analysis
- NLP
- Sentiment
- Topic classification
- Market analytics
- Geopolitical scoring
- Template-based synthesis

It must not pretend deterministic output is generated by an LLM.

If an optional LLM is added later, it must be:

- Optional
- Environment-controlled
- Disabled by default
- Clearly documented

---

# 25. AI RESEARCH QUESTIONS

The system should support questions such as:

Why is the technology sector receiving attention?

What are the major geopolitical risks right now?

What themes are appearing in financial news?

Which sectors are associated with energy-related events?

What are the dominant news themes?

What changed in market sentiment?

The system should answer using available application data.

If insufficient evidence exists, say:

"Insufficient evidence available."

Do not invent information.

---

# 26. AI EVIDENCE REQUIREMENT

Every generated research insight should show evidence.

Example:

Insight:
Energy-related geopolitical attention has increased.

Evidence:

- Relevant news article
- Relevant geopolitical event
- Relevant market observation

Confidence:

72%

Uncertainty:

Medium

Risk Flags:

- Limited data
- Correlation does not imply causation
- Data may be delayed

---

# 27. GEOPOLITICAL INTELLIGENCE

Create a dedicated Geopolitics page.

It should monitor:

- Countries
- Regions
- Events
- Severity
- Recency
- Market relevance
- Related sectors
- Related themes

Regions:

- India
- South Asia
- Middle East
- Europe
- North America
- East Asia
- Africa

---

# 28. GEOPOLITICAL EVENT CATEGORIES

Categories include:

- Conflict
- Trade
- Sanctions
- Diplomacy
- Elections
- Energy
- Supply Chain
- Regulation
- Technology
- Security

Each event should contain:

- Event title
- Country/region
- Category
- Severity
- Date
- Market relevance
- Related sectors
- Related themes
- Source
- Confidence

---

# 29. GEOPOLITICAL RISK SCORE

Create:

MarketPulse Research Score

This is NOT an official risk rating.

Score components may include:

- Severity
- Market exposure
- Recency
- Uncertainty

Normalize to:

0–100

Example:

Severity: 80

Market Exposure: 70

Recency: 90

Uncertainty: 75

Research Score: 79

The calculation must be explainable.

---

# 30. GEOPOLITICAL LANGUAGE

Use:

Potential market relevance

Potential exposure

Observed relationship

Research signal

Scenario

Do NOT say:

"This event will cause the market to crash."

Do NOT make deterministic claims about future prices.

---

# 31. ANNOUNCEMENTS

Create an Announcements page covering:

- Corporate announcements
- Government announcements
- Regulatory announcements
- Central bank announcements
- Macro announcements
- Economic calendar events

Each announcement should contain:

- Title
- Category
- Date
- Importance
- Source
- Source URL
- Related sectors
- Related themes

---

# 32. MACROECONOMICS

Create a Macro page.

Potential indicators:

- Inflation
- GDP
- Interest rates
- Unemployment
- Currency
- Oil
- Gold
- Bond yields where available

Show:

- Current/latest
- Previous
- Change
- Trend
- Source
- Timestamp
- Data status

Distinguish:

LIVE

LATEST AVAILABLE

HISTORICAL

DEMO

---

# 33. ANALYTICS

Create an Analytics page.

Include:

- Returns
- Volatility
- Moving averages
- Momentum
- Drawdown
- Correlation
- Beta
- Sector comparison
- Event studies

Charts should be meaningful.

Do not add charts purely for decoration.

---

# 34. EVENT STUDY

Provide an educational event-study tool.

Inputs:

- Asset
- Event date
- Observation window

Outputs:

- Pre-event price
- Post-event price
- Cumulative return
- Volatility comparison

Clearly state:

This is historical/educational analysis.

It does not establish causation.

---

# 35. RISK LAB

Create a scenario analysis tool.

Inputs:

- Portfolio value
- Market shock
- Beta
- Volatility assumptions

Scenarios:

- Market shock
- Interest-rate shock
- Oil shock
- Geopolitical escalation
- Currency shock
- Technology-sector decline

Outputs:

- Hypothetical impact
- Percentage change
- Explanation
- Assumptions

The feature must NOT execute trades.

It must be clearly labeled:

HYPOTHETICAL SCENARIO

---

# 36. RESEARCH WORKSPACE

Create a Research page.

Users should be able to select:

- Company
- Sector
- Topic
- Region

Generate:

- Summary
- Observations
- Evidence
- Risks
- Uncertainties

Allow export to:

- Markdown
- JSON

Local storage is sufficient initially.

---

# 37. GLOBAL SEARCH

Implement global search across:

- Companies
- Securities
- News
- Geopolitical events
- Announcements
- Topics

Results should be grouped by type.

Keyboard shortcut:

/

should focus the search input.

---

# 38. SYSTEM PAGE

The System page should show:

Application status

Backend status

Database status

Provider status

Data mode

Last update

NLP status

Research engine status

Example:

Backend:
ONLINE

Database:
ONLINE

Market Provider:
DEMO

News Provider:
DEMO

NLP:
ONLINE

Research Engine:
ONLINE

---

# 39. ABOUT SECTION

Show:

MarketPulse AI

Student-built educational financial and geopolitical intelligence platform.

Mission:

Explore how AI, NLP, financial analytics, data engineering and geopolitical intelligence can be combined into a unified research environment.

Include technology cards:

- Python
- FastAPI
- React
- SQLAlchemy
- Pandas
- NumPy
- scikit-learn
- NLTK
- REST APIs

---

# 40. FRONTEND TECHNOLOGY

Preferred stack:

React

Vite

TypeScript

React Router

Recharts

Lucide React

Use modern CSS or Tailwind if appropriate.

Do not introduce unnecessary frontend libraries.

---

# 41. BACKEND TECHNOLOGY

Preferred stack:

Python

FastAPI

Pydantic

SQLAlchemy

SQLite

Pandas

NumPy

scikit-learn

NLTK

httpx

pytest

Optional:

spaCy

APScheduler

Do not make optional dependencies mandatory unless required.

---

# 42. DATABASE

Use SQLAlchemy.

Primary models should include:

- Company
- Security
- MarketPrice
- Index
- NewsArticle
- NewsEntity
- SentimentResult
- GeopoliticalEvent
- Country
- Announcement
- MacroIndicator
- AIInsight
- DataSource
- AuditLog
- Watchlist
- SavedResearch

Models should support:

- created_at
- updated_at

External data should support:

- provider
- source
- source_url
- published_at
- retrieved_at
- data_status

---

# 43. BACKEND ARCHITECTURE

Use layered architecture:

API
↓
Schemas
↓
Services
↓
Repositories / Database
↓
Providers / Adapters

Analytics and ML should remain modular.

Avoid putting business logic directly inside FastAPI routes.

---

# 44. BACKEND API

Required endpoints:

GET /api/health

GET /api/system/status

GET /api/dashboard

GET /api/markets/overview

GET /api/markets/search

GET /api/markets/quote/{symbol}

GET /api/markets/history/{symbol}

GET /api/markets/indicators/{symbol}

GET /api/news

GET /api/news/search

GET /api/news/{id}

GET /api/sentiment

GET /api/sentiment/trends

GET /api/sentiment/sectors

GET /api/geopolitics

GET /api/geopolitics/events

GET /api/geopolitics/regions

GET /api/announcements

GET /api/macro

GET /api/macro/{indicator}

GET /api/analytics

GET /api/analytics/correlation

GET /api/analytics/event-study

POST /api/risk/scenario

GET /api/ai/insights

POST /api/ai/research

GET /api/search

---

# 45. API QUALITY

All endpoints should have:

- Validation
- Pydantic schemas
- Correct HTTP status codes
- Error handling
- Logging
- Timeout handling
- External API retry logic where appropriate
- Clear response formats

API keys must never be exposed to the frontend.

---

# 46. ENVIRONMENT CONFIGURATION

Create:

.env.example

Example configuration:

APP_ENV=development

DATA_MODE=demo

MARKET_PROVIDER=demo

NEWS_PROVIDER=demo

MACRO_PROVIDER=demo

GEOPOLITICAL_PROVIDER=demo

ANNOUNCEMENT_PROVIDER=demo

Optional API keys may be included as empty variables.

No API key should be required to run the demo.

---

# 47. DEMO MODE

DEMO_MODE is mandatory.

The project must work without internet access where practical.

Demo data must be realistic enough to demonstrate:

- Charts
- News
- Sentiment
- Geopolitics
- Analytics
- Risk scenarios
- AI insights

Demo data must be clearly labeled:

DEMO DATA

Never present synthetic data as live information.

---

# 48. ERROR HANDLING

If an external provider fails:

Show:

Provider unavailable.

Then use fallback if available.

Frontend must not show a blank screen.

Every page needs:

Loading state

Error state

Empty state

Retry action where appropriate.

---

# 49. FRONTEND DESIGN

The design should be:

- Premium
- Dark
- Minimal
- Technical
- Professional
- Modern
- Financial
- AI-oriented

Avoid looking like:

- Generic admin dashboard
- Cryptocurrency exchange
- Gaming UI
- Excessively neon interface

---

# 50. COLOR SYSTEM

Background:

#050811
#070B14
#0A101C

Panels:

#0C1421
#101927

Borders:

#1B2A40
#243650

Accent:

Cyan / Electric Blue

Secondary:

Indigo / Violet

Positive:

Green

Negative:

Red

Warning:

Amber

Text:

White / Light Grey

Muted:

Blue-grey

Colors should be used consistently.

---

# 51. UI/UX

The application must include:

- Responsive design
- Smooth transitions
- Loading skeletons
- Hover states
- Tooltips
- Error states
- Empty states
- Animated counters
- Responsive charts
- Accessible buttons
- Keyboard navigation
- Consistent spacing
- Consistent typography

Do not overuse animation.

Animations should improve the experience rather than distract.

---

# 52. NAVIGATION

Primary navigation:

Overview

AI Intelligence

Markets

News

Sentiment

Geopolitics

Announcements

Macro

Analytics

Risk Lab

Research

System

Navigation should show the current active page.

Mobile navigation must be responsive.

---

# 53. REUSABLE COMPONENTS

Create reusable components such as:

Navbar

Sidebar

PageHeader

MetricCard

StatusBadge

DataSourceBadge

ChartCard

NewsCard

InsightCard

GeoEventCard

LoadingSkeleton

ErrorState

EmptyState

DisclaimerModal

SearchBar

FilterBar

Tabs

Modal

Button

---

# 54. CHARTS

Use reusable chart components.

Charts must have:

- Responsive sizing
- Tooltips
- Labels
- Legends where useful
- Empty state
- Loading state
- Error state

Do not use charts only for decoration.

---

# 55. RESPONSIVENESS

Support:

1920px

1440px

1280px

1024px

768px

Mobile

Tables should become:

- Scrollable
- Stacked
- Card-based

where appropriate.

---

# 56. ACCESSIBILITY

Use:

- Semantic HTML
- Keyboard navigation
- Focus states
- ARIA labels where appropriate
- Adequate color contrast
- Buttons instead of clickable divs

---

# 57. PERFORMANCE

Avoid unnecessary complexity.

Use:

- API caching where useful
- Pagination
- Limited response sizes
- Lazy loading where appropriate
- Efficient React rendering

Do not introduce Redis unless there is a real requirement.

---

# 58. SECURITY

Implement basic security practices:

- Environment variables
- No secrets in Git
- CORS configuration
- Input validation
- API timeouts
- Safe external requests
- No arbitrary URL fetching
- Logs must not contain secrets

Authentication is optional for the first version.

If authentication is not implemented, document that.

---

# 59. PRIVACY

Do not collect:

- Brokerage credentials
- Payment information
- Sensitive financial account information
- Unnecessary personal information

Research notes may be stored locally.

---

# 60. TESTING

Backend tests should cover:

- Health
- System status
- Markets
- News
- Sentiment
- Geopolitics
- Announcements
- Analytics
- Risk
- AI

Also test:

- Invalid input
- Provider failure
- Demo fallback
- Empty data
- Missing data

Frontend should have at least basic smoke/build validation.

---

# 61. DOCKER

Provide:

backend/Dockerfile

frontend/Dockerfile

docker-compose.yml

Docker must be optional.

The project must also run directly on Windows without Docker.

---

# 62. GITHUB REQUIREMENTS

Repository must include:

README.md

PROJECT_SPEC.md

.env.example

.gitignore

LICENSE

docs/

tests/

The README must explain:

- Problem
- Solution
- Features
- Architecture
- Tech stack
- AI/NLP
- Analytics
- Geopolitics
- Data sources
- Free API strategy
- Responsible AI
- Disclaimer
- Limitations
- Setup
- Testing
- Future roadmap

---

# 63. DOCUMENTATION

Create:

docs/ARCHITECTURE.md

docs/DATA_SOURCES.md

docs/AI_METHODOLOGY.md

docs/RESPONSIBLE_AI.md

docs/API.md

docs/LIMITATIONS.md

docs/ROADMAP.md

docs/VIVA.md

Documentation should explain advanced concepts in student-friendly language.

---

# 64. VIVA / INTERVIEW PREPARATION

The documentation should explain:

Why FastAPI?

Why React?

Why SQLite?

Why SQLAlchemy?

Why provider adapters?

Why NLP?

Why TF-IDF?

Why sentiment analysis?

How is confidence calculated?

How does the AI research engine work?

How is hallucination risk reduced?

How does provider fallback work?

How is demo data distinguished from real data?

How is geopolitical risk calculated?

Why are buy/sell recommendations excluded?

How could the platform scale?

What are the limitations?

---

# 65. NO FAKE FUNCTIONALITY

Do not create buttons that do nothing.

Do not create pages that contain only placeholder text.

Do not create fake API calls.

Do not hardcode the entire dashboard in React.

Do not fabricate news.

Do not fabricate source URLs.

Do not claim synthetic data is live.

Do not claim AI capabilities that are not implemented.

---

# 66. AI RESPONSIBILITY

AI-generated information must:

- Be evidence-oriented
- Communicate uncertainty
- Show confidence
- Show sources
- Show timestamps
- Identify demo data
- Avoid financial instructions
- Avoid guaranteed predictions
- Avoid fabricated citations

If insufficient evidence exists:

"Insufficient evidence available."

---

# 67. DATA QUALITY

Implement validation for:

- Missing values
- Duplicate records
- Invalid timestamps
- Invalid prices
- Invalid symbols
- Provider failures

Where practical, expose a data quality indicator.

---

# 68. LOCAL DEVELOPMENT

Backend should be runnable using:

python -m venv .venv

Install dependencies.

uvicorn app.main:app --reload

Frontend should be runnable using:

npm install

npm run dev

The exact commands should be documented.

---

# 69. EXPECTED PROJECT STRUCTURE

Preferred structure:

marketpulse_ai/

├── README.md
├── PROJECT_SPEC.md
├── .env.example
├── .gitignore
├── LICENSE
├── docker-compose.yml
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── adapters/
│   │   ├── analytics/
│   │   ├── ml/
│   │   └── utils/
│   └── tests/
│
├── frontend/
│   ├── package.json
│   ├── vite.config.*
│   ├── index.html
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── layouts/
│       ├── charts/
│       ├── services/
│       ├── hooks/
│       ├── utils/
│       └── styles/
│
├── data/
│   └── demo/
│
├── models/
│
├── scripts/
│
└── docs/

The implementation may improve this structure if there is a clear architectural reason.

---

# 70. DEVELOPMENT APPROACH

The project should be implemented incrementally.

Recommended order:

PHASE 1
Repository and backend foundation

PHASE 2
Database and provider architecture

PHASE 3
Market and macro data

PHASE 4
News and announcements

PHASE 5
NLP and sentiment

PHASE 6
Geopolitical intelligence

PHASE 7
Analytics and risk

PHASE 8
AI research engine

PHASE 9
Frontend foundation

PHASE 10
Individual frontend pages

PHASE 11
Landing page and animations

PHASE 12
Integration

PHASE 13
Testing

PHASE 14
UI/UX polish

PHASE 15
Documentation

PHASE 16
Final audit

---

# 71. DEVELOPMENT RULES FOR AI CODING AGENT

The coding agent must:

1. Inspect existing files before modifying them.
2. Avoid deleting working functionality.
3. Reuse existing components.
4. Avoid duplicate implementations.
5. Keep backend business logic outside routes.
6. Keep API keys out of frontend.
7. Keep demo mode functional.
8. Test after major changes.
9. Fix errors rather than merely reporting them.
10. Update PROJECT_STATE.md after major phases.
11. Avoid unnecessary dependencies.
12. Avoid unnecessary architectural complexity.
13. Never fabricate data sources.
14. Never fabricate API results.
15. Never fabricate AI capabilities.

---

# 72. DEFINITION OF DONE

The project is considered complete only when:

- Landing page works
- Dynamic greeting works
- Animated disclaimer works
- Disclaimer acknowledgement persists
- Overview works
- AI page works
- Markets works
- News works
- Sentiment works
- Geopolitics works
- Announcements works
- Macro works
- Analytics works
- Risk Lab works
- Research works
- System page works
- Search works
- Backend works
- Database works
- Demo mode works
- Free provider architecture works
- Provider fallback works
- NLP works
- Sentiment works
- Analytics works
- AI research engine works
- Evidence is displayed
- Confidence is displayed
- Uncertainty is displayed
- Source attribution works
- No paid API is required
- No trade execution exists
- No buy/sell recommendation exists
- Tests exist
- README exists
- Documentation exists
- Docker configuration exists
- Frontend builds successfully
- Backend starts successfully
- No secrets are committed

---

# 73. QUALITY BAR

The final project should NOT look like:

- A basic CRUD application
- A college assignment dashboard
- A generic admin panel
- A cryptocurrency trading UI
- A collection of disconnected pages

It should feel like:

A serious student-built financial intelligence and AI research platform.

The project should demonstrate:

- Full-stack engineering
- Data engineering
- AI/ML
- NLP
- Financial analytics
- Geopolitical analysis
- API integration
- Responsible AI
- Modern UI/UX

while remaining understandable and explainable by a BTech AI & Data Science student.

---

# 74. FUTURE EXTENSIBILITY

The architecture should allow future additions such as:

- More market providers
- More news providers
- More geopolitical data
- Advanced NLP
- Embeddings
- Vector search
- Local LLM
- Optional cloud LLM
- Portfolio simulation
- Advanced event studies
- More macroeconomic indicators
- User accounts
- Saved dashboards
- Advanced research reports

These are future features unless explicitly implemented.

Do not over-engineer the first version for them.

---

# 75. FINAL PRODUCT POSITIONING

The official project description should be:

"MarketPulse AI is a student-built financial and geopolitical intelligence platform combining market analytics, news intelligence, NLP-based sentiment analysis, geopolitical event monitoring, macroeconomic context and evidence-oriented AI research."

The project should be presented as:

Educational
Research-oriented
Experimental
Portfolio-focused

It must not be presented as:

Financial advice
Investment advice
Trading software
Official exchange software
Regulatory-approved financial software

---

# END OF PROJECT SPECIFICATION