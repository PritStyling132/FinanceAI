# AI-Powered Financial Advisor
## Project Presentation

---

# SLIDE 1: Title Slide

## AI-Powered Personalized Financial Advisor
### Using RAG, LLM, and Real-Time Market Data

**Technologies:** Python | FastAPI | Flask | Ollama LLM | Qdrant | LangChain

---

# SLIDE 2: Table of Contents

1. Project Description
2. Problem Statement
3. Proposed Solution
4. **Key Features & Functionality**
5. System Design
   - Architecture
   - Context Flow Diagram
   - Process Flow Diagram
6. Implementation
   - Pseudocode

---

# SECTION 1: INTRODUCTION

---

# SLIDE 3: 1.1 Project Description

## What is this project?

The **AI-Powered Personalized Financial Advisor** is an intelligent web application designed to democratize financial guidance for everyday investors. Built using cutting-edge technologies including Large Language Models (LLM), Retrieval-Augmented Generation (RAG), and real-time market data integration, this system provides personalized investment advice tailored to each user's unique financial situation.

The application leverages **Ollama's llama3.2:3b model** for natural language understanding, enabling users to ask financial questions in plain English and receive contextually relevant, personalized responses. The **RAG pipeline** ensures accuracy by retrieving relevant information from a curated financial knowledge base stored in **Qdrant vector database**, while the **Alpha Vantage API** provides real-time stock prices, technical indicators, and market sentiment analysis.

Unlike traditional financial advisory services that charge premium fees, this application offers **free, 24/7 access** to intelligent financial guidance. Users can track their investment portfolios, set and monitor financial goals, manage monthly budgets, and receive personalized stock and mutual fund recommendations based on their risk tolerance and investment horizon.

---

# SLIDE 4: 1.1 Project Description (Continued)

## Target Users

This application is designed for **individual investors** who seek personalized financial advice without the high costs associated with professional financial advisors. It specifically caters to **beginners** entering the investment world who need clear, jargon-free guidance on mutual funds, stocks, SIPs, and tax-saving instruments like ELSS under Section 80C.

The platform is equally valuable for **busy professionals** who want quick, reliable financial insights without spending hours researching market trends. By combining AI-powered chat capabilities with real-time market data, users can make informed investment decisions in minutes rather than hours.

## Project Scope

The system integrates user profile data including age, income, risk tolerance, and financial goals with AI analysis through the RAG pipeline to generate personalized investment recommendations. This end-to-end solution covers everything from user registration and authentication to portfolio tracking, goal management, budget monitoring, and intelligent financial advisory services.

---

# SLIDE 5: 1.2 Problem Statement

## The Problem

In today's complex financial landscape, individual investors face significant challenges when seeking reliable investment guidance. The most pressing issue is the **lack of personalized advice** — most financial information available online is generic and fails to consider individual circumstances such as age, income level, risk tolerance, and specific financial goals. A one-size-fits-all approach simply cannot address the diverse needs of different investors.

**Professional financial advisors**, while capable of providing personalized guidance, charge **prohibitively high fees** that make their services inaccessible to middle-class families and first-time investors. This creates a significant barrier where those who need financial guidance the most are often unable to afford it.

The internet has created an **information overload** problem where users are bombarded with conflicting financial advice from countless sources. Distinguishing between trustworthy guidance and misleading information has become increasingly difficult, leading to confusion and poor investment decisions.

---

# SLIDE 6: 1.2 Problem Statement (Continued)

## Additional Challenges

Another critical challenge is that most available financial advice is **static and outdated**, failing to account for current market conditions. Traditional resources like books, articles, and pre-recorded videos cannot adapt to rapidly changing market sentiment, leaving investors to manually research current trends — a time-consuming and often overwhelming task.

Finally, the financial industry is plagued by **complex jargon and technical terminology** that confuses beginners. Terms like P/E ratio, RSI, asset allocation, and diversification are essential concepts, but they are often explained in ways that alienate newcomers rather than educate them.

## The Gap

There exists a clear gap in the market for an **affordable, personalized, and real-time financial advisory solution** that can understand individual user needs, provide contextually relevant advice based on current market conditions, and communicate in simple, jargon-free language. This gap represents the core problem that our AI-Powered Financial Advisor aims to solve.

---

# SLIDE 7: 1.3 Proposed Solution

## Our Solution: AI-Powered Financial Advisor

Our proposed solution is an **AI-Powered Personalized Financial Advisor** that addresses all identified problems through innovative use of modern AI/ML technologies. At its core, the system combines **Large Language Model (LLM)** capabilities with **Retrieval-Augmented Generation (RAG)** to deliver accurate, contextually relevant financial advice.

The application uses **Ollama's llama3.2:3b model** as the LLM engine, which understands natural language queries and generates human-like responses. The **RAG pipeline**, built using LangChain and Qdrant vector database, retrieves relevant information from a curated knowledge base of 20+ financial documents covering topics like mutual funds, SIP investments, tax saving under Section 80C, retirement planning, and risk management.

To ensure advice reflects current market conditions, the system integrates with **Alpha Vantage API** for real-time stock prices, company fundamentals, technical indicators like RSI and moving averages, and news sentiment analysis. User profiles stored in **SQLite database** capture individual financial details including age, income, savings, risk tolerance, and investment goals, enabling truly personalized recommendations.

---

# SLIDE 8: 1.3 Proposed Solution (Features)

## Solution Features

The system delivers **personalized investment recommendations** based on comprehensive user profiling. By analyzing factors such as age, annual income, current savings, debt levels, and investment horizon, the AI advisor can suggest appropriate asset allocation strategies tailored to each user's risk tolerance — whether conservative, moderate, or aggressive.

The **RAG-powered intelligence** ensures responses are grounded in factual financial knowledge rather than AI hallucinations. When a user asks a question, the system performs semantic search across the financial knowledge base, retrieves the most relevant documents, and uses this context to generate accurate, informative responses.

**Real-time market integration** sets this solution apart from static financial resources. Users can research specific stocks and receive current prices, P/E ratios, market capitalization, technical signals, and recent news sentiment — all synthesized into actionable insights.

A unique **Smart Fallback System** ensures the application remains functional even when the LLM service is unavailable. Using keyword matching and rule-based logic, the system can still provide specific stock and mutual fund recommendations based on the user's risk profile and current market sentiment.

Finally, the application includes **comprehensive financial tools** for portfolio tracking with real-time profit/loss calculations, financial goal setting with progress monitoring and SIP projections, and budget management with category-wise expense tracking and overspending alerts.

---

# SECTION 4: KEY FEATURES & FUNCTIONALITY

---

# SLIDE 9: Key Features Overview

## Application Functionality

```
+------------------------------------------------------------------+
|                    KEY FEATURES OVERVIEW                          |
+------------------------------------------------------------------+
|                                                                   |
|  +------------------+  +------------------+  +------------------+ |
|  |  AI CHAT         |  |  PORTFOLIO       |  |  FINANCIAL       | |
|  |  ADVISOR         |  |  MANAGEMENT      |  |  GOALS           | |
|  +------------------+  +------------------+  +------------------+ |
|                                                                   |
|  +------------------+  +------------------+  +------------------+ |
|  |  MARKET          |  |  BUDGET          |  |  USER            | |
|  |  ANALYSIS        |  |  TRACKING        |  |  PROFILE         | |
|  +------------------+  +------------------+  +------------------+ |
|                                                                   |
|  +------------------+  +------------------+  +------------------+ |
|  |  INVESTMENT      |  |  ALERTS &        |  |  ANALYTICS       | |
|  |  RECOMMENDATIONS |  |  NOTIFICATIONS   |  |  DASHBOARD       | |
|  +------------------+  +------------------+  +------------------+ |
|                                                                   |
+------------------------------------------------------------------+
```

---

# SLIDE 10: Feature 1 - AI Chat Advisor

## 1. AI-Powered Chat Advisor

### Functionality:
- **Natural Language Queries**: Ask financial questions in plain English
- **Context-Aware Responses**: Uses RAG to provide accurate answers
- **Personalized Advice**: Tailored to user's risk profile and goals
- **Chat History**: Maintains conversation context

### How It Works:
```
User Question ──► RAG Pipeline ──► LLM Processing ──► Personalized Response
                      │
                      ▼
              Knowledge Base + User Profile + Market Data
```

### Example Queries:
| User Query | AI Response |
|------------|-------------|
| "Where should I invest Rs.10,000?" | Personalized allocation based on risk |
| "Explain mutual funds" | Educational content from knowledge base |
| "Is RELIANCE a good buy?" | Real-time analysis with market data |
| "How to plan for retirement?" | Goal-based investment strategy |

---

# SLIDE 11: Feature 2 - Portfolio Management

## 2. Portfolio Management

### Functionality:
- **Add Holdings**: Track stocks, mutual funds, and other assets
- **Real-Time Valuation**: Live prices from Alpha Vantage API
- **P&L Tracking**: Profit/Loss calculation for each holding
- **Asset Allocation View**: Visual breakdown of portfolio

### Portfolio Dashboard:
```
+------------------------------------------------------------------+
|                    PORTFOLIO SUMMARY                              |
+------------------------------------------------------------------+
|                                                                   |
|  Total Invested: Rs. 5,00,000      Current Value: Rs. 5,75,000   |
|  Total Gain/Loss: +Rs. 75,000 (+15%)                             |
|                                                                   |
+------------------------------------------------------------------+
|  HOLDINGS                                                         |
+------------------------------------------------------------------+
| Symbol   | Qty  | Buy Price | Current | Gain/Loss | Change %    |
|----------|------|-----------|---------|-----------|-------------|
| RELIANCE | 50   | Rs. 2400  | Rs. 2650| +Rs.12,500| +10.4%      |
| TCS      | 30   | Rs. 3200  | Rs. 3500| +Rs. 9,000| +9.4%       |
| HDFC     | 100  | Rs. 1500  | Rs. 1750| +Rs.25,000| +16.7%      |
+------------------------------------------------------------------+
|                                                                   |
|  ASSET ALLOCATION:  [Stocks: 60%] [MF: 30%] [Others: 10%]        |
|                                                                   |
+------------------------------------------------------------------+
```

---

# SLIDE 12: Feature 3 - Financial Goals

## 3. Financial Goal Tracking

### Functionality:
- **Create Goals**: Retirement, Education, Home, Emergency Fund, etc.
- **Progress Tracking**: Visual progress bars and milestones
- **SIP Calculator**: Required monthly investment calculation
- **Projected vs Target**: Future value projections

### Goal Types Supported:
| Goal Type | Description | Typical Horizon |
|-----------|-------------|-----------------|
| Retirement | Build retirement corpus | 20-30 years |
| Education | Child's education fund | 10-18 years |
| Home Purchase | Down payment savings | 5-10 years |
| Emergency Fund | 6-month expense buffer | 1-2 years |
| Wealth Building | General investment growth | 5+ years |
| Vacation | Travel fund | 1-3 years |

### Goal Progress View:
```
+------------------------------------------------------------------+
| GOAL: Retirement Fund                                             |
+------------------------------------------------------------------+
| Target: Rs. 1,00,00,000          Target Date: 2045               |
| Current: Rs. 15,00,000           Monthly SIP: Rs. 25,000         |
|                                                                   |
| Progress: [██████████░░░░░░░░░░░░░░░░░░░░] 15%                   |
|                                                                   |
| Status: ON TRACK                                                  |
| Projected Amount: Rs. 1,25,00,000 (Exceeds Target!)              |
+------------------------------------------------------------------+
```

---

# SLIDE 13: Feature 4 - Market Analysis

## 4. Real-Time Market Analysis

### Functionality:
- **Stock Quotes**: Live price, change %, volume
- **Company Overview**: P/E ratio, market cap, sector info
- **Technical Indicators**: RSI, moving averages
- **News Sentiment**: Recent news with sentiment analysis

### Market Data Display:
```
+------------------------------------------------------------------+
|                    STOCK ANALYSIS: RELIANCE                       |
+------------------------------------------------------------------+
|                                                                   |
|  QUOTE                           OVERVIEW                         |
|  ─────                           ────────                         |
|  Price: Rs. 2,650.75             Sector: Energy                   |
|  Change: +45.30 (+1.74%)         Industry: Oil & Gas              |
|  Volume: 12.5M                   Market Cap: Rs. 18L Cr           |
|  Day High: Rs. 2,680             P/E Ratio: 28.5                  |
|  Day Low: Rs. 2,590              52W High: Rs. 2,850              |
|                                  52W Low: Rs. 2,180               |
|                                                                   |
+------------------------------------------------------------------+
|  TECHNICAL INDICATORS            NEWS SENTIMENT                   |
|  ────────────────────            ──────────────                   |
|  RSI (14): 58.2 (Neutral)        Overall: BULLISH                 |
|  SMA (50): Rs. 2,580             Recent News:                     |
|  SMA (200): Rs. 2,420            • Jio tariff hike positive       |
|                                  • Retail expansion on track      |
|  Signal: BUY                     • Green energy investments       |
|                                                                   |
+------------------------------------------------------------------+
```

---

# SLIDE 14: Feature 5 - Budget Management

## 5. Budget & Expense Tracking

### Functionality:
- **Monthly Budget**: Set income and category-wise budgets
- **Expense Tracking**: Log daily expenses with categories
- **Spending Analysis**: Visual charts and insights
- **Budget Alerts**: Notifications when overspending

### Budget Categories:
| Category | Typical % | Description |
|----------|-----------|-------------|
| Housing | 25-30% | Rent, EMI, maintenance |
| Food | 10-15% | Groceries, dining out |
| Transport | 10-15% | Fuel, public transport |
| Utilities | 5-10% | Electricity, internet, phone |
| Healthcare | 5-10% | Insurance, medicines |
| Entertainment | 5-10% | Movies, subscriptions |
| Savings | 20-30% | Investments, emergency fund |

### Budget Dashboard:
```
+------------------------------------------------------------------+
|                    MONTHLY BUDGET - JANUARY 2025                  |
+------------------------------------------------------------------+
|  Income: Rs. 1,00,000           Total Budget: Rs. 80,000         |
|  Spent: Rs. 52,000              Remaining: Rs. 28,000            |
+------------------------------------------------------------------+
|                                                                   |
|  Housing      [████████████████░░░░] Rs. 25,000 / 30,000  (83%)  |
|  Food         [██████████████░░░░░░] Rs. 8,000 / 12,000   (67%)  |
|  Transport    [████████░░░░░░░░░░░░] Rs. 4,000 / 10,000   (40%)  |
|  Utilities    [████████████████████] Rs. 5,000 / 5,000   (100%)  |
|  Healthcare   [████░░░░░░░░░░░░░░░░] Rs. 2,000 / 8,000    (25%)  |
|  Entertainment[██████████░░░░░░░░░░] Rs. 5,000 / 10,000   (50%)  |
|  Savings      [██████░░░░░░░░░░░░░░] Rs. 3,000 / 5,000    (60%)  |
|                                                                   |
+------------------------------------------------------------------+
```

---

# SLIDE 15: Feature 6 - Investment Recommendations

## 6. Personalized Investment Recommendations

### Functionality:
- **Risk-Based Suggestions**: Conservative, Moderate, Aggressive
- **Market-Aware**: Adjusts for bullish/bearish conditions
- **Specific Stocks & Funds**: Named recommendations with rationale
- **Asset Allocation**: Suggested portfolio mix

### Recommendation Engine:
```
+------------------------------------------------------------------+
|                 RECOMMENDATION ENGINE                             |
+------------------------------------------------------------------+
|                                                                   |
|  INPUT:                          OUTPUT:                          |
|  ┌──────────────────┐            ┌──────────────────────────┐    |
|  │ User Profile     │            │ Stock Recommendations    │    |
|  │ - Age: 35        │            │ - HDFC Bank (Banking)    │    |
|  │ - Risk: Moderate │ ────────►  │ - Infosys (IT)           │    |
|  │ - Horizon: 15yrs │            │ - Reliance (Energy)      │    |
|  └──────────────────┘            └──────────────────────────┘    |
|                                                                   |
|  ┌──────────────────┐            ┌──────────────────────────┐    |
|  │ Market Sentiment │            │ Mutual Fund Suggestions  │    |
|  │ - BULLISH        │ ────────►  │ - Nifty 50 Index Fund    │    |
|  │ - Positive news  │            │ - HDFC Balanced Advantage│    |
|  └──────────────────┘            │ - PPFAS Flexi Cap        │    |
|                                  └──────────────────────────┘    |
|                                                                   |
+------------------------------------------------------------------+
```

### Sample Recommendations by Risk:
| Risk Level | Equity % | Debt % | Gold % | Top Picks |
|------------|----------|--------|--------|-----------|
| Conservative | 30% | 60% | 10% | HDFC Bank, TCS, Debt Funds |
| Moderate | 60% | 30% | 10% | Reliance, Infosys, Balanced Funds |
| Aggressive | 80% | 15% | 5% | Tata Motors, Zomato, Small Caps |

---

# SLIDE 16: Feature 7 - User Profile & Authentication

## 7. User Profile Management

### Functionality:
- **Secure Registration**: Email and password with validation
- **JWT Authentication**: Secure token-based sessions
- **Risk Assessment**: Questionnaire to determine risk tolerance
- **Profile Customization**: Update financial details anytime

### User Profile Fields:
```
+------------------------------------------------------------------+
|                    USER PROFILE                                   |
+------------------------------------------------------------------+
|                                                                   |
|  PERSONAL INFO                   FINANCIAL INFO                   |
|  ─────────────                   ──────────────                   |
|  Name: John Doe                  Annual Income: Rs. 12,00,000    |
|  Email: john@email.com           Current Savings: Rs. 5,00,000   |
|  Age: 35                         Monthly Investment: Rs. 30,000  |
|                                  Debt Amount: Rs. 0              |
|                                                                   |
|  INVESTMENT PROFILE              GOALS                            |
|  ─────────────────               ─────                            |
|  Risk Tolerance: MODERATE        ☑ Retirement                    |
|  Investment Horizon: 15 years    ☑ Child Education               |
|  Has Emergency Fund: YES         ☑ Home Purchase                 |
|  Has Retirement Account: YES     ☐ Vacation                      |
|                                                                   |
+------------------------------------------------------------------+
```

---

# SLIDE 17: Feature 8 - Alerts & Analytics

## 8. Alerts, Notifications & Analytics

### Alerts Functionality:
- **Budget Alerts**: Overspending notifications
- **Goal Reminders**: Milestone achievements
- **Market Alerts**: Price movements, news
- **Portfolio Alerts**: Significant P&L changes

### Analytics Dashboard:
```
+------------------------------------------------------------------+
|                    ANALYTICS DASHBOARD                            |
+------------------------------------------------------------------+
|                                                                   |
|  USAGE STATISTICS                FINANCIAL HEALTH SCORE           |
|  ────────────────                ──────────────────────           |
|  Chat Sessions: 45               Score: 78/100 (GOOD)             |
|  Questions Asked: 120                                             |
|  Portfolio Updates: 15           Savings Rate: 25% ✓              |
|  Goals Created: 4                Emergency Fund: YES ✓            |
|                                  Debt Ratio: LOW ✓                |
|                                  Diversification: MODERATE ⚠      |
|                                                                   |
+------------------------------------------------------------------+
|                                                                   |
|  RECENT ALERTS                                                    |
|  ─────────────                                                    |
|  ⚠ Budget Alert: Food category exceeded by 15%                   |
|  ✓ Goal Update: Retirement fund reached 20% milestone            |
|  📈 Market: RELIANCE up 5% this week                              |
|  💡 Tip: Consider increasing SIP by Rs. 5,000                     |
|                                                                   |
+------------------------------------------------------------------+
```

---

# SLIDE 18: Features Summary Table

## All Features at a Glance

| # | Feature | Description | Technology Used |
|---|---------|-------------|-----------------|
| 1 | **AI Chat Advisor** | Natural language financial Q&A | Ollama LLM + RAG |
| 2 | **Portfolio Management** | Track holdings, P&L, allocation | Alpha Vantage API |
| 3 | **Financial Goals** | Create & track goals with projections | SQLite + Python |
| 4 | **Market Analysis** | Real-time quotes, technicals, news | Alpha Vantage API |
| 5 | **Budget Tracking** | Monthly budgets & expense logging | SQLite + Charts |
| 6 | **Recommendations** | Risk-based stock/fund suggestions | Rule Engine + AI |
| 7 | **User Profile** | Authentication & risk assessment | JWT + bcrypt |
| 8 | **Alerts & Analytics** | Notifications & usage insights | Event System |

### Unique Selling Points:
- **Works Offline**: Smart fallback when LLM unavailable
- **Indian Market Focus**: Stocks, mutual funds, tax saving (80C)
- **Beginner Friendly**: Simple UI, no jargon
- **Free & Open Source**: No subscription fees

---

# SECTION 5: SYSTEM DESIGN

---

# SLIDE 19: 5.1 Architecture Overview

## High-Level System Architecture

```
+------------------------------------------------------------------+
|                         USER LAYER                                |
|                    (Web Browser - Port 5000)                      |
+------------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
|                     PRESENTATION LAYER                            |
|                                                                   |
|   +---------------------------+                                   |
|   |     FLASK FRONTEND        |                                   |
|   |  - Jinja2 Templates       |                                   |
|   |  - Bootstrap 5 UI         |                                   |
|   |  - Chart.js Visualizations|                                   |
|   |  - API Proxy to Backend   |                                   |
|   +---------------------------+                                   |
+------------------------------------------------------------------+
                              |
                              v (HTTP - Port 8000)
+------------------------------------------------------------------+
|                      APPLICATION LAYER                            |
|                                                                   |
|   +---------------------------+                                   |
|   |     FASTAPI BACKEND       |                                   |
|   |  - REST API Endpoints     |                                   |
|   |  - JWT Authentication     |                                   |
|   |  - Business Logic         |                                   |
|   |  - AI Services            |                                   |
|   +---------------------------+                                   |
+------------------------------------------------------------------+
                              |
          +-------------------+-------------------+
          v                   v                   v
+----------------+   +----------------+   +----------------+
|   DATA LAYER   |   |   AI LAYER    |   | EXTERNAL APIs  |
|                |   |               |   |                |
| - SQLite DB    |   | - Ollama LLM  |   | - Alpha        |
| - Qdrant       |   | - Embeddings  |   |   Vantage      |
|   Vector DB    |   | - RAG Pipeline|   | - Market Data  |
+----------------+   +----------------+   +----------------+
```

---

# SLIDE 20: 5.1 Architecture - Component Details

## Detailed Component Architecture

```
+------------------------------------------------------------------+
|                    FRONTEND (Flask + Jinja2)                      |
+------------------------------------------------------------------+
| Pages:                                                            |
| +--------+ +----------+ +------+ +-------+ +--------+ +--------+  |
| | Login  | | Dashboard| | Chat | | Goals | | Market | | Budget |  |
| +--------+ +----------+ +------+ +-------+ +--------+ +--------+  |
+------------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
|                    BACKEND (FastAPI)                              |
+------------------------------------------------------------------+
| Routers:                                                          |
| +------+ +------+ +-------+ +-----------+ +--------+ +---------+  |
| | Auth | | Chat | | Goals | | Portfolio | | Budget | | Alerts  |  |
| +------+ +------+ +-------+ +-----------+ +--------+ +---------+  |
|                              |                                    |
| Services:                    v                                    |
| +------------------+ +------------------+ +------------------+    |
| | Financial        | | RAG Pipeline     | | Alpha Vantage    |    |
| | Advisor          | |                  | | Service          |    |
| +------------------+ +------------------+ +------------------+    |
|         |                    |                    |               |
|         v                    v                    v               |
| +------------------+ +------------------+ +------------------+    |
| | LLM Service      | | Vector Store     | | Embeddings       |    |
| | (Ollama)         | | (Qdrant)         | | (HuggingFace)    |    |
| +------------------+ +------------------+ +------------------+    |
+------------------------------------------------------------------+
```

---

# SLIDE 21: 5.1 Architecture - Technology Stack

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Flask 3.0, Jinja2, Bootstrap 5, Chart.js | Web UI |
| **Backend** | FastAPI, Python 3.11, Uvicorn | REST API |
| **Database** | SQLite + SQLAlchemy | User data storage |
| **Vector DB** | Qdrant | Semantic search |
| **LLM** | Ollama (llama3.2:3b) | AI responses |
| **Embeddings** | HuggingFace (all-MiniLM-L6-v2) | Text vectorization |
| **Market Data** | Alpha Vantage API | Real-time stocks |
| **Auth** | JWT + bcrypt | Security |

---

# SLIDE 22: 5.2 Context Flow Diagram

## System Context Diagram

```
+------------------------------------------------------------------+
|                      EXTERNAL ENTITIES                            |
+------------------------------------------------------------------+

                         +-------------+
                         |    USER     |
                         | (Investor)  |
                         +------+------+
                                |
            +-------------------+-------------------+
            |                   |                   |
            v                   v                   v
    +---------------+   +---------------+   +---------------+
    | Registration  |   | Financial     |   | Market        |
    | & Profile     |   | Queries       |   | Research      |
    | Setup         |   | & Chat        |   | Requests      |
    +-------+-------+   +-------+-------+   +-------+-------+
            |                   |                   |
            +-------------------+-------------------+
                                |
                                v
+------------------------------------------------------------------+
|                   AI FINANCIAL ADVISOR SYSTEM                     |
|                                                                   |
|  +------------------------------------------------------------+  |
|  |                    Core Processing                          |  |
|  |  - User Authentication    - RAG Pipeline                    |  |
|  |  - Profile Management     - LLM Integration                 |  |
|  |  - Portfolio Tracking     - Market Analysis                 |  |
|  +------------------------------------------------------------+  |
+------------------------------------------------------------------+
            |                   |                   |
            v                   v                   v
+------------------------------------------------------------------+
|                      EXTERNAL SYSTEMS                             |
+------------------------------------------------------------------+

    +---------------+   +---------------+   +---------------+
    | Alpha Vantage |   |    Ollama     |   |    Qdrant     |
    | (Market Data) |   |    (LLM)      |   | (Vector DB)   |
    +---------------+   +---------------+   +---------------+
```

---

# SLIDE 23: 5.2 Context Flow - Data Flows

## Data Flow Between Entities

```
+------------------------------------------------------------------+
|                    CONTEXT FLOW DIAGRAM                           |
+------------------------------------------------------------------+

  +--------+                                          +-------------+
  |  USER  |                                          | ALPHA       |
  |        |                                          | VANTAGE API |
  +---+----+                                          +------+------+
      |                                                      ^
      | 1. Login/Register                                    |
      | 2. Ask financial questions                           | 6. Request
      | 3. View portfolio/goals                              |    stock data
      |                                                      |
      v                                                      |
+-----+--------------------------------------------------+---+-----+
|                                                                   |
|                  AI FINANCIAL ADVISOR                             |
|                                                                   |
|   +------------------+          +------------------+              |
|   |   User Profile   |          |   RAG Engine     |              |
|   |   Management     |          |   + LLM          |              |
|   +--------+---------+          +--------+---------+              |
|            |                             |                        |
|            |   +------------------+      |                        |
|            +-->|   Recommendation |<-----+                        |
|                |   Engine         |                               |
|                +--------+---------+                               |
|                         |                                         |
+-------------------------+-----------------------------------------+
      |                   |
      | 4. Personalized   | 5. Retrieve knowledge
      |    advice         |    vectors
      v                   v
  +--------+       +-------------+
  |  USER  |       |   QDRANT    |
  | (Gets  |       | (Vector DB) |
  | advice)|       +-------------+
  +--------+
```

---

# SLIDE 24: 5.3 Process Flow Diagram

## Main Process Flow: User Query to Response

```
+------------------------------------------------------------------+
|                    PROCESS FLOW DIAGRAM                           |
|                  (AI Chat Interaction)                            |
+------------------------------------------------------------------+

    START
      |
      v
+-------------+
| User sends  |
| message     |
+------+------+
       |
       v
+-------------+     No     +------------------+
| User logged |---------->| Redirect to      |
| in?         |           | Login page       |
+------+------+           +------------------+
       | Yes
       v
+-------------+
| Validate    |
| JWT Token   |
+------+------+
       |
       v
+-------------+
| Load User   |
| Profile     |
+------+------+
       |
       v
+-------------+     No     +------------------+
| LLM         |---------->| Use Smart        |
| Available?  |           | Fallback System  |----+
+------+------+           +------------------+    |
       | Yes                                      |
       v                                          |
+-------------+                                   |
| RAG         |                                   |
| Pipeline    |                                   |
+------+------+                                   |
       |                                          |
       v                                          |
+-------------+                                   |
| 1. Embed    |                                   |
|    Query    |                                   |
+------+------+                                   |
       |                                          |
       v                                          |
+-------------+                                   |
| 2. Search   |                                   |
|    Qdrant   |                                   |
+------+------+                                   |
       |                                          |
       v                                          |
+-------------+                                   |
| 3. Build    |                                   |
|    Context  |                                   |
+------+------+                                   |
       |                                          |
       v                                          |
+-------------+                                   |
| 4. LLM      |                                   |
|    Generate |                                   |
+------+------+                                   |
       |                                          |
       +<-----------------------------------------+
       |
       v
+-------------+
| Apply       |
| Guardrails  |
+------+------+
       |
       v
+-------------+
| Add         |
| Disclaimer  |
+------+------+
       |
       v
+-------------+
| Save to     |
| Chat History|
+------+------+
       |
       v
+-------------+
| Return      |
| Response    |
+------+------+
       |
       v
     END
```

---

# SLIDE 25: 5.3 Process Flow - RAG Pipeline Detail

## RAG Pipeline Process Flow

```
+------------------------------------------------------------------+
|                  RAG PIPELINE PROCESS FLOW                        |
+------------------------------------------------------------------+

+------------------+
| User Question:   |
| "How to invest   |
| for retirement?" |
+--------+---------+
         |
         v
+------------------+     +------------------+     +------------------+
| STEP 1:          |     | STEP 2:          |     | STEP 3:          |
| Embed Query      |     | Vector Search    |     | Extract Symbols  |
|                  |     |                  |     |                  |
| HuggingFace      |     | Query Qdrant     |     | Find stock       |
| all-MiniLM-L6-v2 |     | Top-3 matches    |     | tickers in query |
| Query -> Vector  |     | Score > 0.3      |     | (AAPL, INFY...)  |
+--------+---------+     +--------+---------+     +--------+---------+
         |                        |                        |
         +------------------------+------------------------+
                                  |
                                  v
                    +---------------------------+
                    | STEP 4: BUILD CONTEXT     |
                    |                           |
                    | +---------------------+   |
                    | | User Profile:       |   |
                    | | Age: 35, Income: 1L |   |
                    | | Risk: Moderate      |   |
                    | +---------------------+   |
                    |                           |
                    | +---------------------+   |
                    | | Retrieved Docs:     |   |
                    | | - Retirement guide  |   |
                    | | - Asset allocation  |   |
                    | +---------------------+   |
                    |                           |
                    | +---------------------+   |
                    | | Market Data:        |   |
                    | | (if symbols found)  |   |
                    | +---------------------+   |
                    +-------------+-------------+
                                  |
                                  v
                    +---------------------------+
                    | STEP 5: LLM GENERATION    |
                    |                           |
                    | System Prompt +           |
                    | Context +                 |
                    | User Question             |
                    |        |                  |
                    |        v                  |
                    |  Ollama llama3.2:3b       |
                    +-------------+-------------+
                                  |
                                  v
                    +---------------------------+
                    | STEP 6: GUARDRAILS        |
                    |                           |
                    | - Input validation        |
                    | - Output sanitization     |
                    | - Add disclaimer          |
                    +-------------+-------------+
                                  |
                                  v
                    +---------------------------+
                    | FINAL RESPONSE            |
                    | Personalized retirement   |
                    | advice + disclaimer       |
                    +---------------------------+
```

---

# SLIDE 26: 5.3 Process Flow - Smart Fallback

## Smart Fallback Process Flow (When LLM Unavailable)

```
+------------------------------------------------------------------+
|                SMART FALLBACK PROCESS FLOW                        |
+------------------------------------------------------------------+

+------------------+
| User Message:    |
| "Give me stock   |
| recommendations" |
+--------+---------+
         |
         v
+------------------+
| KEYWORD MATCHING |
| (Priority-based) |
+--------+---------+
         |
    +----+----+----+
    |         |    |
    v         v    v
+-------+ +-------+ +-------+
|PRIORITY|PRIORITY|PRIORITY|
|   1    |   2    |   3    |
|        |        |        |
| Stock  | Fund   | Generic|
|Keywords|Keywords| Invest |
+---+----+---+----+---+----+
    |        |        |
    v        v        v
+----------------------------------+
| GET MARKET SENTIMENT             |
| from Alpha Vantage               |
|                                  |
| Returns: BULLISH / BEARISH /     |
|          NEUTRAL                 |
+----------------+-----------------+
                 |
                 v
+----------------------------------+
| GET USER RISK PROFILE            |
|                                  |
| Conservative / Moderate /        |
| Aggressive                       |
+----------------+-----------------+
                 |
                 v
+----------------------------------+
| GENERATE RECOMMENDATIONS         |
|                                  |
| +------------------------------+ |
| | Stock/Fund Tables with:      | |
| | - Specific names             | |
| | - Sectors                    | |
| | - Investment rationale       | |
| | - Risk levels                | |
| +------------------------------+ |
|                                  |
| +------------------------------+ |
| | Investment Strategy          | |
| +------------------------------+ |
|                                  |
| +------------------------------+ |
| | Disclaimer                   | |
| +------------------------------+ |
+----------------------------------+
```

---

# SECTION 7: IMPLEMENTATION

---

# SLIDE 27: 7.1 Pseudocode - Main Application

## Pseudocode: Application Initialization

```
ALGORITHM: Initialize_Financial_Advisor_Application

BEGIN
    // Step 1: Load Configuration
    config = LOAD_ENVIRONMENT_VARIABLES(".env")

    // Step 2: Initialize Database
    database = CREATE_SQLITE_CONNECTION(config.DATABASE_URL)
    CREATE_TABLES_IF_NOT_EXISTS(database)

    // Step 3: Initialize Vector Store
    qdrant_client = CONNECT_TO_QDRANT(config.QDRANT_HOST, config.QDRANT_PORT)

    IF NOT COLLECTION_EXISTS("financial_knowledge") THEN
        CREATE_COLLECTION("financial_knowledge", vector_size=384)
        knowledge_docs = LOAD_FINANCIAL_KNOWLEDGE()
        FOR EACH doc IN knowledge_docs DO
            vector = EMBED_TEXT(doc.content)
            STORE_IN_QDRANT(vector, doc.metadata)
        END FOR
    END IF

    // Step 4: Initialize LLM Service
    llm_service = INITIALIZE_OLLAMA_CLIENT(config.OLLAMA_BASE_URL)
    llm_available = CHECK_LLM_HEALTH(llm_service)

    // Step 5: Initialize Embedding Service
    embedding_model = LOAD_HUGGINGFACE_MODEL("all-MiniLM-L6-v2")

    // Step 6: Start API Server
    START_FASTAPI_SERVER(port=8000)

    PRINT("Financial Advisor System Initialized Successfully")
END
```

---

# SLIDE 28: 7.1 Pseudocode - User Authentication

## Pseudocode: User Registration & Login

```
ALGORITHM: User_Registration

INPUT: email, password, full_name
OUTPUT: success_status, user_object

BEGIN
    // Validate input
    IF NOT IS_VALID_EMAIL(email) THEN
        RETURN ERROR("Invalid email format")
    END IF

    IF LENGTH(password) < 8 THEN
        RETURN ERROR("Password must be at least 8 characters")
    END IF

    // Check if user exists
    existing_user = DATABASE.FIND_USER_BY_EMAIL(email)
    IF existing_user EXISTS THEN
        RETURN ERROR("User already registered")
    END IF

    // Hash password
    hashed_password = BCRYPT_HASH(password)

    // Create user
    new_user = CREATE_USER_OBJECT(
        email = email,
        hashed_password = hashed_password,
        full_name = full_name,
        risk_tolerance = "moderate",  // default
        is_active = TRUE
    )

    DATABASE.INSERT(new_user)

    RETURN SUCCESS(new_user)
END


ALGORITHM: User_Login

INPUT: email, password
OUTPUT: jwt_token, user_info

BEGIN
    // Find user
    user = DATABASE.FIND_USER_BY_EMAIL(email)

    IF user NOT EXISTS THEN
        RETURN ERROR("Invalid credentials")
    END IF

    // Verify password
    IF NOT BCRYPT_VERIFY(password, user.hashed_password) THEN
        RETURN ERROR("Invalid credentials")
    END IF

    // Generate JWT token
    token_payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": CURRENT_TIME + 24_HOURS
    }

    jwt_token = JWT_ENCODE(token_payload, SECRET_KEY)

    RETURN SUCCESS(jwt_token, user.to_dict())
END
```

---

# SLIDE 29: 7.1 Pseudocode - RAG Pipeline

## Pseudocode: RAG Pipeline for AI Chat

```
ALGORITHM: RAG_Pipeline_Query

INPUT: user_message, user_profile
OUTPUT: ai_response

BEGIN
    // Step 1: Input Validation (Guardrails)
    IF CONTAINS_HARMFUL_CONTENT(user_message) THEN
        RETURN SAFE_RESPONSE("I can only provide financial guidance.")
    END IF

    // Step 2: Embed the query
    query_vector = EMBEDDING_MODEL.ENCODE(user_message)

    // Step 3: Search Vector Database
    search_results = QDRANT.SEARCH(
        collection = "financial_knowledge",
        query_vector = query_vector,
        limit = 3,
        score_threshold = 0.3
    )

    // Step 4: Extract stock symbols (if any)
    symbols = EXTRACT_STOCK_SYMBOLS(user_message)
    market_data = {}

    IF symbols NOT EMPTY THEN
        FOR EACH symbol IN symbols DO
            market_data[symbol] = ALPHA_VANTAGE.GET_QUOTE(symbol)
        END FOR
    END IF

    // Step 5: Build Context
    context = BUILD_CONTEXT(
        user_profile = user_profile,
        retrieved_docs = search_results,
        market_data = market_data
    )

    // Step 6: Generate LLM Response
    system_prompt = LOAD_FINANCIAL_ADVISOR_PROMPT()

    response = OLLAMA.GENERATE(
        model = "llama3.2:3b",
        system = system_prompt,
        context = context,
        query = user_message
    )

    // Step 7: Apply Output Guardrails
    sanitized_response = SANITIZE_OUTPUT(response)

    // Step 8: Add Disclaimer
    final_response = sanitized_response + FINANCIAL_DISCLAIMER

    // Step 9: Save to Chat History
    DATABASE.SAVE_CHAT_MESSAGE(user_profile.id, user_message, final_response)

    RETURN final_response
END
```

---

# SLIDE 30: 7.1 Pseudocode - Build Context

## Pseudocode: Context Building for LLM

```
ALGORITHM: Build_Context

INPUT: user_profile, retrieved_docs, market_data
OUTPUT: formatted_context_string

BEGIN
    context_parts = []

    // Part 1: User Profile Context
    profile_context = FORMAT_STRING("""
        USER PROFILE:
        - Name: {user_profile.full_name}
        - Age: {user_profile.age}
        - Annual Income: Rs. {user_profile.annual_income}
        - Risk Tolerance: {user_profile.risk_tolerance}
        - Investment Horizon: {user_profile.investment_horizon} years
        - Financial Goals: {JOIN(user_profile.goals, ", ")}
        - Has Emergency Fund: {user_profile.has_emergency_fund}
        - Monthly Investment Capacity: Rs. {user_profile.monthly_investment}
    """)

    APPEND(context_parts, profile_context)

    // Part 2: Retrieved Knowledge
    IF retrieved_docs NOT EMPTY THEN
        knowledge_context = "RELEVANT FINANCIAL KNOWLEDGE:\n"

        FOR EACH doc IN retrieved_docs DO
            knowledge_context += "- " + doc.content + "\n"
        END FOR

        APPEND(context_parts, knowledge_context)
    END IF

    // Part 3: Market Data (if available)
    IF market_data NOT EMPTY THEN
        market_context = "CURRENT MARKET DATA:\n"

        FOR EACH symbol, data IN market_data DO
            market_context += FORMAT_STRING("""
                {symbol}:
                - Price: {data.price}
                - Change: {data.change_percent}%
                - P/E Ratio: {data.pe_ratio}
            """)
        END FOR

        APPEND(context_parts, market_context)
    END IF

    // Combine all parts
    full_context = JOIN(context_parts, "\n\n")

    RETURN full_context
END
```

---

# SLIDE 31: 7.1 Pseudocode - Smart Fallback

## Pseudocode: Smart Fallback System

```
ALGORITHM: Smart_Fallback_Response

INPUT: user_message, user_profile
OUTPUT: fallback_response

BEGIN
    message_lower = LOWERCASE(user_message)

    // Define keyword patterns
    stock_keywords = ["stock", "share", "equity", "nifty", "sensex"]
    fund_keywords = ["mutual fund", "sip", "elss", "index fund"]
    recommend_triggers = ["recommend", "suggest", "give me", "best"]

    // Determine response type
    wants_recommendation = ANY(trigger IN message_lower FOR trigger IN recommend_triggers)
    wants_stocks = ANY(keyword IN message_lower FOR keyword IN stock_keywords)
    wants_funds = ANY(keyword IN message_lower FOR keyword IN fund_keywords)

    // Get market sentiment
    sentiment = ALPHA_VANTAGE.GET_MARKET_SENTIMENT()

    // Get user risk level
    risk = user_profile.risk_tolerance  // "conservative", "moderate", "aggressive"

    // Generate appropriate recommendations
    response = ""

    IF wants_recommendation THEN
        IF wants_stocks THEN
            response = GENERATE_STOCK_RECOMMENDATIONS(risk, sentiment)
        ELSE IF wants_funds THEN
            response = GENERATE_FUND_RECOMMENDATIONS(risk)
        ELSE
            response = GENERATE_STOCK_RECOMMENDATIONS(risk, sentiment)
            response += GENERATE_FUND_RECOMMENDATIONS(risk)
        END IF
    ELSE
        // Generic financial guidance
        response = GET_GENERAL_FINANCIAL_TIP(message_lower)
    END IF

    // Add market sentiment indicator
    sentiment_indicator = GET_SENTIMENT_EMOJI(sentiment)
    response = sentiment_indicator + "\n\n" + response

    // Add disclaimer
    response += "\n\n" + FINANCIAL_DISCLAIMER

    RETURN response
END


ALGORITHM: Generate_Stock_Recommendations

INPUT: risk_level, market_sentiment
OUTPUT: formatted_stock_table

BEGIN
    // Stock pools by risk level
    conservative_stocks = [
        {"name": "HDFC Bank", "sector": "Banking", "reason": "Stable dividends"},
        {"name": "TCS", "sector": "IT", "reason": "Consistent growth"},
        {"name": "ITC", "sector": "FMCG", "reason": "Defensive stock"}
    ]

    moderate_stocks = [
        {"name": "Reliance", "sector": "Conglomerate", "reason": "Diversified"},
        {"name": "ICICI Bank", "sector": "Banking", "reason": "Growth + Value"},
        {"name": "Infosys", "sector": "IT", "reason": "Large deals"}
    ]

    aggressive_stocks = [
        {"name": "Tata Motors", "sector": "Auto", "reason": "EV potential"},
        {"name": "Adani Ports", "sector": "Infrastructure", "reason": "High growth"},
        {"name": "Zomato", "sector": "Tech", "reason": "Market leader"}
    ]

    // Select based on risk
    SWITCH risk_level:
        CASE "conservative": stocks = conservative_stocks
        CASE "moderate": stocks = moderate_stocks
        CASE "aggressive": stocks = aggressive_stocks

    // Adjust for market sentiment
    IF market_sentiment == "BEARISH" THEN
        ADD_DEFENSIVE_STOCKS(stocks)
    END IF

    // Format as markdown table
    table = "| Stock | Sector | Investment Thesis |\n"
    table += "|-------|--------|-------------------|\n"

    FOR EACH stock IN stocks DO
        table += "| {stock.name} | {stock.sector} | {stock.reason} |\n"
    END FOR

    RETURN table
END
```

---

# SLIDE 32: 7.1 Pseudocode - Portfolio Management

## Pseudocode: Portfolio Operations

```
ALGORITHM: Add_Holding_To_Portfolio

INPUT: user_id, symbol, quantity, purchase_price, asset_type
OUTPUT: holding_object

BEGIN
    // Validate symbol
    IF asset_type == "stock" THEN
        stock_data = ALPHA_VANTAGE.GET_QUOTE(symbol)
        IF stock_data IS NULL THEN
            RETURN ERROR("Invalid stock symbol")
        END IF
        current_price = stock_data.price
        stock_name = stock_data.name
    ELSE
        current_price = purchase_price
        stock_name = symbol
    END IF

    // Create holding record
    holding = CREATE_HOLDING(
        user_id = user_id,
        symbol = symbol,
        name = stock_name,
        asset_type = asset_type,
        quantity = quantity,
        purchase_price = purchase_price,
        current_price = current_price,
        purchase_date = CURRENT_DATE
    )

    DATABASE.INSERT(holding)

    RETURN holding
END


ALGORITHM: Get_Portfolio_Summary

INPUT: user_id
OUTPUT: portfolio_summary

BEGIN
    holdings = DATABASE.GET_ALL_HOLDINGS(user_id)

    total_invested = 0
    current_value = 0
    holdings_list = []

    FOR EACH holding IN holdings DO
        // Update current price for stocks
        IF holding.asset_type == "stock" THEN
            latest_price = ALPHA_VANTAGE.GET_QUOTE(holding.symbol).price
            holding.current_price = latest_price
            DATABASE.UPDATE(holding)
        END IF

        invested = holding.quantity * holding.purchase_price
        current = holding.quantity * holding.current_price
        gain_loss = current - invested
        gain_loss_percent = (gain_loss / invested) * 100

        total_invested += invested
        current_value += current

        APPEND(holdings_list, {
            "symbol": holding.symbol,
            "name": holding.name,
            "quantity": holding.quantity,
            "invested": invested,
            "current_value": current,
            "gain_loss": gain_loss,
            "gain_loss_percent": gain_loss_percent
        })
    END FOR

    // Calculate totals
    total_gain_loss = current_value - total_invested
    total_gain_loss_percent = (total_gain_loss / total_invested) * 100

    RETURN {
        "holdings": holdings_list,
        "total_invested": total_invested,
        "current_value": current_value,
        "total_gain_loss": total_gain_loss,
        "total_gain_loss_percent": total_gain_loss_percent
    }
END
```

---

# SLIDE 33: 7.1 Pseudocode - Goal Tracking

## Pseudocode: Financial Goal Management

```
ALGORITHM: Create_Financial_Goal

INPUT: user_id, name, goal_type, target_amount, target_date, monthly_contribution
OUTPUT: goal_object

BEGIN
    // Calculate months until target
    months_remaining = MONTHS_BETWEEN(CURRENT_DATE, target_date)

    // Calculate required monthly SIP (assuming 12% annual return)
    annual_return = 0.12
    monthly_return = annual_return / 12

    // Future Value of Annuity formula
    // required_monthly = target_amount / (((1+r)^n - 1) / r)
    required_monthly = target_amount / (
        (POWER(1 + monthly_return, months_remaining) - 1) / monthly_return
    )

    // Create goal
    goal = CREATE_GOAL(
        user_id = user_id,
        name = name,
        goal_type = goal_type,
        target_amount = target_amount,
        current_amount = 0,
        monthly_contribution = monthly_contribution,
        target_date = target_date,
        priority = "medium",
        is_achieved = FALSE
    )

    DATABASE.INSERT(goal)

    // Add recommendation if contribution is less than required
    IF monthly_contribution < required_monthly THEN
        goal.recommendation = FORMAT_STRING(
            "To reach your goal, consider increasing monthly SIP to Rs. {required_monthly}"
        )
    END IF

    RETURN goal
END


ALGORITHM: Calculate_Goal_Progress

INPUT: goal_id
OUTPUT: progress_details

BEGIN
    goal = DATABASE.GET_GOAL(goal_id)

    // Calculate progress percentage
    progress_percent = (goal.current_amount / goal.target_amount) * 100

    // Calculate time progress
    total_months = MONTHS_BETWEEN(goal.created_at, goal.target_date)
    elapsed_months = MONTHS_BETWEEN(goal.created_at, CURRENT_DATE)
    time_progress_percent = (elapsed_months / total_months) * 100

    // Projected final amount (with current monthly contribution at 12% return)
    months_remaining = total_months - elapsed_months
    projected_amount = goal.current_amount * POWER(1.01, months_remaining)
    projected_amount += goal.monthly_contribution * (
        (POWER(1.01, months_remaining) - 1) / 0.01
    )

    // Status determination
    IF goal.is_achieved THEN
        status = "ACHIEVED"
    ELSE IF projected_amount >= goal.target_amount THEN
        status = "ON_TRACK"
    ELSE
        status = "BEHIND"
    END IF

    RETURN {
        "goal": goal,
        "progress_percent": progress_percent,
        "time_progress_percent": time_progress_percent,
        "projected_amount": projected_amount,
        "months_remaining": months_remaining,
        "status": status
    }
END
```

---

# SLIDE 34: Summary

## Project Summary

### What We Built:
- **AI-Powered Financial Advisor** using modern AI/ML techniques
- **RAG Pipeline** for accurate, context-aware responses
- **Smart Fallback** ensuring reliability without LLM
- **Real-time Market Integration** for current data

### Technologies Used:
- Python, FastAPI, Flask, SQLite
- Ollama LLM, LangChain, Qdrant
- HuggingFace Embeddings, Alpha Vantage API

### Key Features:
1. Personalized investment recommendations
2. Portfolio and goal tracking
3. Budget management
4. Real-time market analysis

### Impact:
- Makes financial advice accessible to everyone
- Reduces dependency on expensive advisors
- Provides 24/7 intelligent financial guidance

---

# SLIDE 35: Thank You

## Thank You!

### Questions?

**Project Repository:** Financial-Advisor

**Technologies:**
- Frontend: Flask + Bootstrap
- Backend: FastAPI + Python
- AI/ML: Ollama + LangChain + Qdrant
- Data: Alpha Vantage API

---

# END OF PRESENTATION
