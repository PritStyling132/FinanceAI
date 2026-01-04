"""
AI Advisor chat API routes with smart fallback responses.
Integrates Alpha Vantage for real-time market data recommendations.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
import re

from sqlalchemy.orm import Session
from app.database import get_db, User, ChatHistory
from app.routers.auth import get_current_user_from_header
from app.models.user_profile import UserProfile, RiskTolerance, UserGoal


router = APIRouter(prefix="/api/chat", tags=["Chat"])

# Initialize services lazily
_financial_advisor = None
_llm_available = None
_alpha_vantage = None


def get_alpha_vantage():
    """Get Alpha Vantage service instance."""
    global _alpha_vantage
    if _alpha_vantage is None:
        try:
            from app.services.alpha_vantage import AlphaVantageService
            _alpha_vantage = AlphaVantageService()
        except Exception as e:
            print(f"Warning: Could not initialize AlphaVantageService: {e}")
            _alpha_vantage = None
    return _alpha_vantage


def get_financial_advisor():
    global _financial_advisor
    if _financial_advisor is None:
        try:
            from app.services.financial_advisor import FinancialAdvisor
            _financial_advisor = FinancialAdvisor()
        except Exception as e:
            print(f"Warning: Could not initialize FinancialAdvisor: {e}")
            _financial_advisor = None
    return _financial_advisor


def check_llm_available():
    """Check if Ollama LLM is available."""
    global _llm_available
    try:
        from app.services.llm_service import LLMService
        llm = LLMService()
        _llm_available = llm.is_available()
    except Exception:
        _llm_available = False
    return _llm_available


# Smart rule-based responses for when LLM is unavailable
# These will be enhanced with user profile data

def fetch_live_stock_data(symbols: list) -> dict:
    """Fetch live stock data from Alpha Vantage for Indian stocks."""
    av = get_alpha_vantage()
    if not av:
        return {}

    stock_data = {}
    # Note: Alpha Vantage uses .BSE or .NSE suffix for Indian stocks
    for symbol in symbols[:5]:  # Limit to 5 to avoid rate limits
        try:
            # Try NSE suffix for Indian stocks
            nse_symbol = f"{symbol}.NSE"
            quote = av.get_stock_quote(nse_symbol)
            if quote and quote.get('price'):
                stock_data[symbol] = quote
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
    return stock_data


def get_market_sentiment() -> str:
    """Get current market sentiment from news."""
    av = get_alpha_vantage()
    if not av:
        return "Market sentiment: Unable to fetch"

    try:
        news = av.get_news_sentiment(topics="financial_markets")
        if news:
            # Calculate average sentiment
            sentiments = [n.get('sentiment_score', 0) for n in news if n.get('sentiment_score')]
            if sentiments:
                avg_sentiment = sum(sentiments) / len(sentiments)
                if avg_sentiment > 0.15:
                    return "📈 **Market Sentiment: BULLISH** - Positive news flow in financial markets"
                elif avg_sentiment < -0.15:
                    return "📉 **Market Sentiment: BEARISH** - Negative news flow, consider defensive positions"
                else:
                    return "➡️ **Market Sentiment: NEUTRAL** - Mixed signals in the market"
        return "**Market Sentiment:** Data unavailable"
    except Exception:
        return "**Market Sentiment:** Unable to fetch"


def get_stock_recommendations(risk_tolerance: str) -> str:
    """Get specific stock recommendations based on risk profile with live market data."""

    # Get market sentiment
    sentiment = get_market_sentiment()

    # Define stock recommendations by risk profile
    if risk_tolerance == "conservative":
        stocks_list = ["HDFCBANK", "TCS", "HINDUNILVR", "ASIANPAINT", "NESTLEIND"]
        dividend_stocks = ["ITC", "COALINDIA", "POWERGRID", "ONGC"]

        return f"""**📊 Stock Recommendations for Conservative Investors**

{sentiment}

Based on your **conservative** risk profile, here are my top stock picks:

---

### 🏦 Large Cap Blue Chips (70% of equity allocation)

| Stock | Sector | Why Recommended | Current View |
|-------|--------|-----------------|--------------|
| **HDFC Bank** | Banking | India's largest private bank, consistent 15-18% RoE | Strong Buy |
| **TCS** | IT Services | Market leader, stable 4%+ dividend yield | Buy on dips |
| **Hindustan Unilever** | FMCG | Defensive play, 50+ brands, rural recovery | Hold |
| **Asian Paints** | Paints | 50%+ market share, pricing power | Accumulate |
| **Nestle India** | FMCG | Premium valuations but recession-proof | SIP recommended |

---

### 💰 High Dividend Yield Stocks (30% of equity allocation)

| Stock | Dividend Yield | Sector | Investment Rationale |
|-------|----------------|--------|---------------------|
| **ITC** | ~4.0% | FMCG/Hotels | Re-rating in progress, FMCG growth |
| **Coal India** | ~7-8% | Mining | High dividend, energy security play |
| **Power Grid** | ~5.0% | Power | Steady cash flows, government backing |
| **ONGC** | ~5.5% | Oil & Gas | Dividend aristocrat, crude hedge |

---

### 📋 Investment Strategy for You:

1. **Entry Strategy**: Start SIP in these stocks via direct equity or ETFs
2. **Allocation**: 70% in blue chips, 30% in dividend stocks
3. **Time Horizon**: Minimum 3-5 years
4. **Rebalancing**: Review quarterly, rebalance annually
5. **Risk Management**: Focus only on Nifty 50 companies, avoid mid/small caps

**Expected Returns**: 10-12% CAGR with lower volatility

---

⚠️ **Disclaimer**: These recommendations are based on current market analysis. Past performance doesn't guarantee future returns. Consult a SEBI-registered advisor."""

    elif risk_tolerance == "aggressive":
        return f"""**📊 Stock Recommendations for Aggressive Investors**

{sentiment}

Based on your **aggressive** risk profile, here are high-growth stock picks:

---

### 🚀 Growth Stocks (40% allocation)

| Stock | Sector | Growth Potential | Risk Level |
|-------|--------|------------------|------------|
| **Trent** | Retail | Zudio expansion, 40%+ revenue growth | Medium-High |
| **Zomato** | Food Tech | Market leader, path to profitability | High |
| **Dixon Tech** | Electronics | PLI benefits, Apple manufacturing | Medium |
| **Persistent Systems** | IT | Digital transformation, deal wins | Medium |
| **Polycab** | Cables | Infrastructure boom beneficiary | Medium |

---

### 💎 Mid Cap Gems (35% allocation)

| Stock | Sector | Investment Thesis | Upside Potential |
|-------|--------|-------------------|------------------|
| **KEI Industries** | Cables | Real estate revival, export growth | 25-30% |
| **Astral Ltd** | Pipes | Building materials leader, brand strength | 20-25% |
| **APL Apollo** | Steel Tubes | Infrastructure play, market leader | 25-30% |
| **KPIT Technologies** | Auto Tech | EV transition, T25 partnerships | 30-40% |
| **Cyient DLM** | Electronics | Defense + aerospace growth | 35-45% |

---

### ⚡ High Risk-High Reward (25% allocation)

| Stock | Sector | Risk Level | Potential Return |
|-------|--------|------------|------------------|
| **Zomato** | Food Delivery | High | 40-50% in 2 years |
| **PB Fintech (PolicyBazaar)** | Fintech | Very High | 50-60% if profitable |
| **Delhivery** | Logistics | High | 30-40% |
| **Paytm** | Fintech | Very High | Turnaround play |

---

### 📋 Investment Strategy for You:

1. **Entry Strategy**: Deploy 50% now, 50% on 5-10% corrections
2. **Position Sizing**: Max 5% in any single stock
3. **Stop Loss**: Set 15-20% stop loss on all positions
4. **Time Horizon**: 5-7 years minimum
5. **Review**: Monthly performance review

**Expected Returns**: 18-25% CAGR with high volatility

---

⚠️ **Warning**: These are high-risk recommendations. Only invest money you can afford to lose."""

    else:  # moderate
        return f"""**📊 Stock Recommendations for Moderate Risk Investors**

{sentiment}

Based on your **moderate** risk profile, here's a balanced portfolio:

---

### 🏢 Core Holdings - Large Caps (50% allocation)

| Stock | Sector | Investment Thesis | Current View |
|-------|--------|-------------------|--------------|
| **Reliance Industries** | Conglomerate | Jio + Retail growth, refinery cash cow | Strong Buy |
| **ICICI Bank** | Banking | Best-in-class asset quality, digital leader | Buy |
| **Infosys** | IT Services | Large deal wins, AI investments | Accumulate |
| **Bharti Airtel** | Telecom | 5G rollout, ARPU improvement | Buy |
| **L&T** | Infrastructure | ₹4L Cr order book, execution king | Buy on dips |

---

### 📈 Growth Allocation - Mid Caps (30% allocation)

| Stock | Sector | Growth Driver | Target Upside |
|-------|--------|---------------|---------------|
| **Tata Elxsi** | IT Services | Auto tech, media & broadcast | 20-25% |
| **Coforge** | IT Services | Strong deal pipeline, BFS focus | 15-20% |
| **Oberoi Realty** | Real Estate | Mumbai luxury segment leader | 25-30% |
| **Max Healthcare** | Healthcare | Hospital expansion, occupancy up | 20-25% |
| **Tube Investments** | Auto Ancillary | EV components, CG Power stake | 25-30% |

---

### 🎯 Tactical/Thematic Picks (20% allocation)

| Stock | Sector | Investment Thesis | Timeline |
|-------|--------|-------------------|----------|
| **Tata Motors** | Auto | EV leader in India, JLR turnaround | 2-3 years |
| **SBI** | Banking | Valuations attractive, NIM stable | 1-2 years |
| **NTPC** | Power | Green energy transition, RE capacity | 3-5 years |
| **HAL** | Defense | Order book visibility, indigenization | 2-3 years |

---

### 📋 Investment Strategy for You:

1. **Entry Strategy**: Start with 50% in large caps via SIP
2. **Mid Cap Addition**: Add mid caps over 6-month period
3. **Cash Reserve**: Keep 10% cash for buying opportunities
4. **Rebalancing**: Quarterly review, annual rebalancing
5. **Stop Loss**: 12-15% for mid caps, trailing for large caps

**Expected Returns**: 14-18% CAGR with moderate volatility

---

⚠️ **Disclaimer**: Invest based on your financial goals. Consult a SEBI-registered advisor for personalized advice."""


def get_mutual_fund_recommendations(risk_tolerance: str, monthly_investment: float = 10000) -> str:
    """Get specific mutual fund recommendations based on risk profile."""

    if risk_tolerance == "conservative":
        return f"""**📊 Mutual Fund Recommendations for Conservative Investors**

Based on your profile, here's a **Rs.{int(monthly_investment):,}/month SIP** portfolio:

---

### 💰 Debt Funds (60% - Rs.{int(monthly_investment * 0.6):,}/month)

| Fund Name | Category | 3Y Returns | Expense Ratio | Rating |
|-----------|----------|------------|---------------|--------|
| **HDFC Short Term Debt Fund** | Short Duration | 6.8% | 0.35% | ⭐⭐⭐⭐⭐ |
| **ICICI Pru Corporate Bond Fund** | Corporate Bond | 7.2% | 0.36% | ⭐⭐⭐⭐⭐ |
| **SBI Magnum Gilt Fund** | Gilt | 6.5% | 0.46% | ⭐⭐⭐⭐ |

---

### ⚖️ Balanced Advantage Funds (25% - Rs.{int(monthly_investment * 0.25):,}/month)

| Fund Name | Category | 3Y Returns | Equity:Debt | Why Recommended |
|-----------|----------|------------|-------------|-----------------|
| **ICICI Pru Balanced Advantage** | BAF | 11.2% | Dynamic | Auto rebalancing |
| **HDFC Balanced Advantage** | BAF | 12.8% | Dynamic | Consistent performer |

---

### 📈 Large Cap Equity (15% - Rs.{int(monthly_investment * 0.15):,}/month)

| Fund Name | Category | 3Y Returns | Risk | Best For |
|-----------|----------|------------|------|----------|
| **UTI Nifty 50 Index Fund** | Index | 12.5% | Low | Core holding |
| **HDFC Index Nifty 50** | Index | 12.3% | Low | Low cost |

---

### 📋 Investment Plan:

**Monthly Allocation:**
- Debt Funds: Rs.{int(monthly_investment * 0.6):,}
- BAF Funds: Rs.{int(monthly_investment * 0.25):,}
- Large Cap: Rs.{int(monthly_investment * 0.15):,}

**Expected Returns**: 8-10% p.a. | **Investment Horizon**: 3-5 years

⚠️ **Note**: Returns are not guaranteed. Check fund ratings on Value Research/Morningstar."""

    elif risk_tolerance == "aggressive":
        return f"""**📊 Mutual Fund Recommendations for Aggressive Investors**

Based on your profile, here's a **Rs.{int(monthly_investment):,}/month SIP** portfolio:

---

### 🚀 Small & Mid Cap Funds (40% - Rs.{int(monthly_investment * 0.4):,}/month)

| Fund Name | Category | 3Y Returns | Risk | Star Rating |
|-----------|----------|------------|------|-------------|
| **Quant Small Cap Fund** | Small Cap | 35.2% | Very High | ⭐⭐⭐⭐⭐ |
| **Nippon India Small Cap** | Small Cap | 32.1% | Very High | ⭐⭐⭐⭐⭐ |
| **Kotak Emerging Equity** | Mid Cap | 23.1% | High | ⭐⭐⭐⭐⭐ |

---

### 💎 Flexi/Multi Cap Funds (35% - Rs.{int(monthly_investment * 0.35):,}/month)

| Fund Name | Category | 3Y Returns | Style | Why Buy |
|-----------|----------|------------|-------|---------|
| **Parag Parikh Flexi Cap** | Flexi Cap | 19.8% | Value | International exposure |
| **Quant Active Fund** | Multi Cap | 28.4% | Momentum | High alpha generator |
| **HDFC Flexi Cap** | Flexi Cap | 18.5% | Blend | Proven track record |

---

### 🎯 Sectoral/Thematic Funds (25% - Rs.{int(monthly_investment * 0.25):,}/month)

| Fund Name | Theme | 3Y Returns | Risk | Rationale |
|-----------|-------|------------|------|-----------|
| **ICICI Pru Technology** | IT/Tech | 18.2% | High | Digital India play |
| **Nippon India Pharma** | Healthcare | 15.8% | Medium | Defensive + growth |
| **Invesco India PSU Equity** | PSU | 42.5% | High | Govt capex beneficiary |

---

### 📋 Investment Plan:

**Monthly Allocation:**
- Small/Mid Cap: Rs.{int(monthly_investment * 0.4):,}
- Flexi Cap: Rs.{int(monthly_investment * 0.35):,}
- Sectoral: Rs.{int(monthly_investment * 0.25):,}

**Expected Returns**: 15-20% p.a. | **Investment Horizon**: 7+ years

⚠️ **Warning**: High volatility expected. Don't panic during 20-30% corrections!"""

    else:  # moderate
        return f"""**📊 Mutual Fund Recommendations for Moderate Risk Investors**

Based on your profile, here's a **Rs.{int(monthly_investment):,}/month SIP** portfolio:

---

### 🏢 Large Cap Core (35% - Rs.{int(monthly_investment * 0.35):,}/month)

| Fund Name | Category | 3Y Returns | Expense | Rating |
|-----------|----------|------------|---------|--------|
| **Mirae Asset Large Cap** | Large Cap | 14.2% | 0.52% | ⭐⭐⭐⭐⭐ |
| **UTI Nifty 50 Index Fund** | Index | 12.5% | 0.18% | ⭐⭐⭐⭐⭐ |
| **Canara Robeco Bluechip** | Large Cap | 14.8% | 0.43% | ⭐⭐⭐⭐⭐ |

---

### 📈 Flexi Cap (30% - Rs.{int(monthly_investment * 0.3):,}/month)

| Fund Name | Category | 3Y Returns | Style | Key Strength |
|-----------|----------|------------|-------|--------------|
| **Parag Parikh Flexi Cap** | Flexi Cap | 19.8% | Value | International + Quality |
| **HDFC Flexi Cap Fund** | Flexi Cap | 18.5% | Blend | Large AUM, consistent |

---

### 🚀 Mid Cap Growth (20% - Rs.{int(monthly_investment * 0.2):,}/month)

| Fund Name | Category | 3Y Returns | Risk | Opportunity |
|-----------|----------|------------|------|-------------|
| **Kotak Emerging Equity** | Mid Cap | 23.1% | Moderate-High | Quality midcaps |
| **Axis Mid Cap Fund** | Mid Cap | 20.5% | Moderate-High | Growth focused |

---

### 💰 Debt Stability (15% - Rs.{int(monthly_investment * 0.15):,}/month)

| Fund Name | Category | 3Y Returns | Safety | Purpose |
|-----------|----------|------------|--------|---------|
| **HDFC Short Term Debt** | Short Duration | 6.8% | High | Stability anchor |
| **ICICI Pru Corporate Bond** | Corporate Bond | 7.2% | High | Better than FD |

---

### 📋 Investment Plan:

**Monthly Allocation:**
- Large Cap: Rs.{int(monthly_investment * 0.35):,}
- Flexi Cap: Rs.{int(monthly_investment * 0.3):,}
- Mid Cap: Rs.{int(monthly_investment * 0.2):,}
- Debt: Rs.{int(monthly_investment * 0.15):,}

**Expected Returns**: 12-14% p.a. | **Investment Horizon**: 5-7 years

💡 **Pro Tip**: Increase SIP by 10% every year for better wealth creation!"""


FINANCIAL_KNOWLEDGE_BASE = {
    "investment": """**Investment Basics:**

Based on your query about investments, here are key principles:

1. **Diversification**: Never put all eggs in one basket. Spread investments across:
   - Equity (stocks, mutual funds) - for growth
   - Debt (bonds, FDs) - for stability
   - Gold - for hedge against inflation

2. **Asset Allocation by Risk Profile**:
   - Conservative: 30% Equity, 60% Debt, 10% Gold
   - Moderate: 50% Equity, 40% Debt, 10% Gold
   - Aggressive: 70% Equity, 20% Debt, 10% Gold

3. **Investment Options in India**:
   - Mutual Funds (SIP recommended)
   - Stocks (direct equity)
   - Fixed Deposits
   - PPF/NPS for retirement
   - ELSS for tax saving""",

    "sip": """**Systematic Investment Plan (SIP):**

SIP is one of the best ways to invest in mutual funds:

1. **Benefits**:
   - Rupee cost averaging - buy more units when prices are low
   - Disciplined investing habit
   - Power of compounding over time
   - Start with as little as Rs.500/month

2. **How to Start**:
   - Choose funds based on your goals and risk profile
   - Set up auto-debit from your bank account
   - Stay invested for at least 5-7 years

3. **SIP vs Lumpsum**:
   - SIP is better for volatile markets
   - Reduces timing risk
   - Ideal for salaried individuals""",

    "mutual fund": """**Mutual Funds Guide:**

Types of Mutual Funds:

1. **By Asset Class**:
   - Equity Funds: High risk, high return potential
   - Debt Funds: Lower risk, stable returns
   - Hybrid Funds: Mix of equity and debt

2. **By Investment Strategy**:
   - Large Cap: Invest in top 100 companies
   - Mid Cap: Companies ranked 101-250
   - Small Cap: Higher growth potential, higher risk
   - Index Funds: Track market indices, low cost

3. **Key Metrics to Check**:
   - Expense Ratio (lower is better)
   - Past performance (3-5 year returns)
   - Fund manager track record
   - AUM (Assets Under Management)""",

    "retirement": """**Retirement Planning:**

Key Steps for Retirement Planning:

1. **Calculate Your Retirement Corpus**:
   - Estimate monthly expenses in retirement
   - Account for inflation (6-7% per year)
   - Plan for 25-30 years post-retirement

2. **Investment Options**:
   - NPS (National Pension System): Tax benefits up to Rs.2 lakh
   - PPF: 15-year lock-in, tax-free returns
   - EPF: If you're employed
   - Equity mutual funds for long-term growth

3. **Rule of Thumb**:
   - Start early to leverage compounding
   - Invest 15-20% of income for retirement
   - Gradually shift to debt as you age""",

    "tax": """**Tax Saving Strategies:**

Tax Saving Options under Section 80C (up to Rs.1.5 lakh):

1. **Investment Options**:
   - ELSS Mutual Funds: 3-year lock-in, equity exposure
   - PPF: 15-year lock-in, guaranteed returns
   - Life Insurance Premium
   - 5-year Tax Saving FD

2. **Additional Deductions**:
   - Section 80CCD(1B): Additional Rs.50,000 for NPS
   - Section 80D: Health Insurance Premium
   - Section 24: Home Loan Interest (up to Rs.2 lakh)

3. **Tax-Efficient Investing**:
   - Hold equity for >1 year for LTCG benefits
   - Use tax-loss harvesting
   - Invest in tax-free bonds""",

    "emergency fund": """**Emergency Fund Guide:**

An emergency fund is crucial financial safety net:

1. **How Much to Save**:
   - 3-6 months of monthly expenses
   - More if you have dependents or unstable income

2. **Where to Keep**:
   - Savings Account (instant access)
   - Liquid Mutual Funds (slightly better returns)
   - Fixed Deposits (for portion not needed immediately)

3. **Building Your Fund**:
   - Prioritize this before investing
   - Save 10-15% of income until target reached
   - Don't use for non-emergencies""",

    "budget": """**Budgeting Basics:**

The 50/30/20 Rule:

1. **50% - Needs**:
   - Rent/EMI
   - Groceries
   - Utilities
   - Insurance

2. **30% - Wants**:
   - Entertainment
   - Dining out
   - Shopping
   - Travel

3. **20% - Savings & Investments**:
   - Emergency fund
   - Retirement savings
   - Goal-based investments

**Tips**:
- Track every expense
- Review and adjust monthly
- Automate savings and investments""",

    "stock": """**Stock Market Investing:**

Getting Started with Stocks:

1. **Before You Invest**:
   - Build emergency fund first
   - Understand your risk tolerance
   - Only invest money you won't need for 5+ years

2. **Investment Approaches**:
   - Index Funds: Passive, low-cost diversification
   - Blue Chip Stocks: Large, stable companies
   - Growth Stocks: Higher risk, higher potential

3. **Key Metrics**:
   - P/E Ratio: Price to Earnings
   - P/B Ratio: Price to Book Value
   - Dividend Yield
   - Debt to Equity Ratio

4. **Risk Management**:
   - Never invest borrowed money
   - Diversify across sectors
   - Don't try to time the market""",

    "goal": """**Goal-Based Financial Planning:**

How to Plan for Financial Goals:

1. **Short-term Goals (< 3 years)**:
   - Vacation, gadgets, wedding
   - Use: FDs, Liquid Funds, Debt Funds

2. **Medium-term Goals (3-7 years)**:
   - Car, down payment, education
   - Use: Balanced/Hybrid Funds, Conservative Equity

3. **Long-term Goals (> 7 years)**:
   - Retirement, child's higher education
   - Use: Equity Funds, SIPs in diversified funds

**Goal Planning Steps**:
- Define specific amount needed
- Set target date
- Calculate monthly investment required
- Choose appropriate investment vehicle
- Review and adjust annually""",

    "hello": """Hello! I'm your AI Financial Advisor. I'm here to help you with:

- **Investment Planning**: Mutual funds, stocks, SIPs
- **Budgeting**: Track expenses, save more
- **Goal Planning**: Retirement, education, home purchase
- **Tax Saving**: Section 80C investments and more

What would you like to know about today?""",

    "hi": """Hi there! Welcome to your personal financial advisor. I can help you with:

- Investment recommendations based on your risk profile
- Budget planning and expense tracking
- Retirement and goal-based planning
- Tax-saving investment strategies

What's on your mind today?""",

    "help": """**How I Can Help You:**

I'm your AI Financial Advisor. Here are some things you can ask me:

**Investment Questions:**
- "How should I start investing?"
- "What is SIP and how does it work?"
- "Which mutual funds should I invest in?"

**Planning Questions:**
- "How much do I need for retirement?"
- "How should I plan for my child's education?"
- "What's the 50/30/20 budget rule?"

**Tax Questions:**
- "How can I save taxes under 80C?"
- "What is ELSS?"
- "What are tax-free investment options?"

Just type your question and I'll do my best to help!""",
}


def get_smart_response(message: str, user: User) -> str:
    """Generate a smart rule-based response when LLM is unavailable."""
    message_lower = message.lower()
    risk_tolerance = user.risk_tolerance or "moderate"
    monthly_investment = user.monthly_investment or 10000

    # PRIORITY 1: Check for stock recommendation requests (comprehensive matching)
    stock_keywords = [
        "stock", "stocks", "share", "shares", "equity", "equities",
        "nifty", "sensex", "bse", "nse", "bluechip", "blue chip",
        "large cap", "mid cap", "small cap", "largecap", "midcap", "smallcap"
    ]
    recommendation_triggers = [
        "recommend", "recommendation", "recommendations", "suggest", "suggestion", "suggestions",
        "give me", "tell me", "show me", "list", "which", "what", "best", "top",
        "should i buy", "to buy", "to invest", "for investment", "good"
    ]

    has_stock_keyword = any(kw in message_lower for kw in stock_keywords)
    has_recommendation_trigger = any(trigger in message_lower for trigger in recommendation_triggers)

    # If asking about stocks with any recommendation intent
    if has_stock_keyword and has_recommendation_trigger:
        return get_stock_recommendations(risk_tolerance)

    # PRIORITY 2: Check for mutual fund recommendation requests
    fund_keywords = [
        "mutual fund", "mutual funds", "mf", "sip", "funds",
        "index fund", "elss", "debt fund", "equity fund", "hybrid fund",
        "flexi cap", "large cap fund", "mid cap fund", "small cap fund"
    ]
    has_fund_keyword = any(kw in message_lower for kw in fund_keywords)

    if has_fund_keyword and has_recommendation_trigger:
        return get_mutual_fund_recommendations(risk_tolerance, monthly_investment)

    # PRIORITY 3: Generic investment recommendation - give both
    generic_investment_triggers = [
        "where should i invest", "how should i invest", "investment recommendation",
        "investment suggestions", "what to invest", "where to invest", "how to invest",
        "start investing", "begin investing", "investment options", "invest my money"
    ]
    if any(trigger in message_lower for trigger in generic_investment_triggers):
        return f"""Based on your **{risk_tolerance}** risk profile, here are my complete investment recommendations:

{get_stock_recommendations(risk_tolerance)}

---

{get_mutual_fund_recommendations(risk_tolerance, monthly_investment)}

---

**Investment Tip**: For beginners, start with mutual fund SIPs before moving to direct equity."""

    # PRIORITY 4: Standalone "stock" or "stocks" query (user just typed "stocks" or "give me stocks")
    stock_only_patterns = ["stock", "stocks", "share", "shares", "equity"]
    if any(message_lower.strip() == pattern or message_lower.strip().startswith(pattern + " ") or
           pattern + " recommendation" in message_lower or pattern + " suggest" in message_lower
           for pattern in stock_only_patterns):
        return get_stock_recommendations(risk_tolerance)

    # PRIORITY 5: Check for common question patterns before knowledge base
    if any(word in message_lower for word in ["how to", "how do i", "how can i", "how should"]):
        if "save" in message_lower:
            return FINANCIAL_KNOWLEDGE_BASE["budget"]
        elif "invest" in message_lower:
            return get_mutual_fund_recommendations(risk_tolerance, monthly_investment)
        elif "retire" in message_lower:
            return FINANCIAL_KNOWLEDGE_BASE["retirement"]
        elif any(s in message_lower for s in ["stock", "stocks", "share", "equity"]):
            return get_stock_recommendations(risk_tolerance)

    # PRIORITY 6: Check for keyword matches in knowledge base (EXCLUDING "stock" - handled above)
    for keyword, response in FINANCIAL_KNOWLEDGE_BASE.items():
        # Skip "stock" keyword - we handle it with specific recommendations above
        if keyword == "stock":
            continue
        if keyword in message_lower:
            # Personalize if we have user info
            personalized = response
            if user.risk_tolerance and keyword not in ["hello", "hi", "help"]:
                personalized += f"\n\n**Based on your {user.risk_tolerance} risk profile**, "
                if user.risk_tolerance == "conservative":
                    personalized += "I recommend focusing more on debt instruments and stable investments."
                elif user.risk_tolerance == "aggressive":
                    personalized += "you can consider higher equity allocation for better growth potential."
                else:
                    personalized += "a balanced approach with mix of equity and debt would suit you well."
            return personalized

    # Default helpful response
    risk_info = f"Risk Tolerance: {user.risk_tolerance.title()}" if user.risk_tolerance else "Complete your profile for personalized advice"
    horizon_info = f"Investment Horizon: {user.investment_horizon} years" if user.investment_horizon else ""

    return f"""I understand you're asking about: "{message}"

Here's how I can help you with financial planning:

**Topics I Can Assist With:**
- **Stock Recommendations** - Ask "Give me stock recommendations"
- **Mutual Fund Recommendations** - Ask "Recommend mutual funds for me"
- **Investment Planning** - SIPs, portfolio allocation
- **Goal Planning** - Retirement, education, home purchase
- **Tax Saving** - Section 80C investments

**Your Profile:**
- {risk_info}
{f'- {horizon_info}' if horizon_info else ''}

**Try asking:**
- "Give me stock recommendations"
- "Which mutual funds should I invest in?"
- "How should I plan for retirement?"
- "What are the best tax saving options?"

I'm here to help with all your financial questions!"""


# Pydantic models
class ChatMessageCreate(BaseModel):
    message: str
    include_market_data: bool = True


class ChatMessageResponse(BaseModel):
    response: str
    response_id: str
    disclaimer: str
    market_data_used: bool
    sources: Optional[List[str]] = None


class ChatHistoryResponse(BaseModel):
    id: int
    role: str
    content: str
    response_id: Optional[str]
    created_at: datetime


def build_user_profile(user: User) -> UserProfile:
    """Build UserProfile from database user."""
    goals = []
    for g in (user.goals or []):
        try:
            goals.append(UserGoal(g))
        except ValueError:
            goals.append(UserGoal.OTHER)

    return UserProfile(
        name=user.full_name,
        age=user.age or 30,
        annual_income=user.annual_income or 0,
        current_savings=user.current_savings or 0,
        monthly_investment=user.monthly_investment or 0,
        debt_amount=user.debt_amount or 0,
        risk_tolerance=RiskTolerance(user.risk_tolerance or "moderate"),
        investment_horizon=user.investment_horizon or 10,
        goals=goals if goals else [UserGoal.WEALTH_BUILDING],
        has_emergency_fund=user.has_emergency_fund or False,
        has_retirement_account=user.has_retirement_account or False
    )


@router.post("", response_model=ChatMessageResponse)
async def chat(
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Send a message to the AI advisor."""
    response_id = str(uuid.uuid4())
    response_text = ""
    disclaimer = "This is AI-generated financial guidance for educational purposes only. Please consult a SEBI-registered advisor for personalized advice."
    sources = []
    used_llm = False

    # Try to use the LLM-powered advisor first
    try:
        advisor = get_financial_advisor()
        if advisor and check_llm_available():
            # Get recent chat history
            recent_messages = db.query(ChatHistory).filter(
                ChatHistory.user_id == current_user.id
            ).order_by(ChatHistory.created_at.desc()).limit(10).all()

            # Build chat history for context
            chat_history = []
            for msg in reversed(recent_messages):
                chat_history.append({
                    "role": msg.role,
                    "content": msg.content
                })

            # Build user profile
            user_profile = build_user_profile(current_user)

            # Get response from advisor
            result = advisor.answer_question(
                question=message_data.message,
                user_profile=user_profile,
                chat_history=chat_history[-6:] if chat_history else None
            )

            response_text = result.get("response", "")
            disclaimer = result.get("disclaimer", disclaimer)
            sources = result.get("sources", [])
            used_llm = True

    except Exception as e:
        print(f"LLM advisor error: {e}")
        used_llm = False

    # If LLM failed or not available, use smart fallback
    if not response_text:
        response_text = get_smart_response(message_data.message, current_user)
        used_llm = False

    # Save user message to history
    try:
        user_message = ChatHistory(
            user_id=current_user.id,
            role="user",
            content=message_data.message
        )
        db.add(user_message)

        # Save assistant response to history
        assistant_message = ChatHistory(
            user_id=current_user.id,
            role="assistant",
            content=response_text,
            response_id=response_id
        )
        db.add(assistant_message)
        db.commit()
    except Exception as e:
        print(f"Error saving chat history: {e}")
        db.rollback()

    return ChatMessageResponse(
        response=response_text,
        response_id=response_id,
        disclaimer=disclaimer,
        market_data_used=message_data.include_market_data and used_llm,
        sources=sources
    )


@router.get("/history", response_model=List[ChatHistoryResponse])
async def get_chat_history(
    limit: int = 50,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get chat history for current user."""
    messages = db.query(ChatHistory).filter(
        ChatHistory.user_id == current_user.id
    ).order_by(ChatHistory.created_at.desc()).limit(limit).all()

    return [
        ChatHistoryResponse(
            id=m.id,
            role=m.role,
            content=m.content,
            response_id=m.response_id,
            created_at=m.created_at
        )
        for m in reversed(messages)
    ]


@router.delete("/history")
async def clear_chat_history(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Clear chat history for current user."""
    db.query(ChatHistory).filter(
        ChatHistory.user_id == current_user.id
    ).delete()
    db.commit()

    return {"message": "Chat history cleared"}


@router.post("/feedback/{response_id}")
async def submit_chat_feedback(
    response_id: str,
    helpful: bool,
    rating: Optional[int] = None,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Submit feedback for a chat response."""
    message = db.query(ChatHistory).filter(
        ChatHistory.response_id == response_id,
        ChatHistory.user_id == current_user.id
    ).first()

    if not message:
        raise HTTPException(status_code=404, detail="Response not found")

    message.feedback_helpful = helpful
    if rating:
        message.feedback_rating = min(5, max(1, rating))

    db.commit()

    return {"message": "Feedback submitted"}


@router.get("/suggestions")
async def get_chat_suggestions(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get suggested questions based on user profile."""
    suggestions = [
        "How should I allocate my investments based on my risk profile?",
        "What's the difference between mutual funds and ETFs?",
        "How much should I save for retirement?",
        "Should I pay off debt or invest first?",
        "What are the best tax-saving investment options?"
    ]

    # Add personalized suggestions based on user profile
    if not current_user.has_emergency_fund:
        suggestions.insert(0, "How do I build an emergency fund?")

    if current_user.risk_tolerance == "conservative":
        suggestions.append("What are safe investment options for conservative investors?")
    elif current_user.risk_tolerance == "aggressive":
        suggestions.append("What high-growth investment options should I consider?")

    if current_user.age and current_user.age < 35:
        suggestions.append("How should young investors approach wealth building?")
    elif current_user.age and current_user.age > 50:
        suggestions.append("How should I plan for retirement in the next 10-15 years?")

    return {"suggestions": suggestions[:8]}


@router.get("/quick-answers/{topic}")
async def get_quick_answer(
    topic: str,
    current_user: User = Depends(get_current_user_from_header)
):
    """Get quick answers for common financial topics."""
    quick_answers = {
        "sip": {
            "title": "Systematic Investment Plan (SIP)",
            "content": "SIP is a method of investing a fixed amount regularly in mutual funds. Benefits include rupee cost averaging, disciplined investing, and the power of compounding.",
            "tips": [
                "Start with as little as Rs.500 per month",
                "Choose funds based on your risk profile and goals",
                "Stay invested for the long term (5+ years)",
                "Increase SIP amount annually as income grows"
            ]
        },
        "mutual_funds": {
            "title": "Mutual Funds",
            "content": "Mutual funds pool money from multiple investors to invest in stocks, bonds, or other securities. They offer diversification and professional management.",
            "tips": [
                "Equity funds for long-term wealth creation",
                "Debt funds for stable returns",
                "Hybrid funds for balanced exposure",
                "Check expense ratio before investing"
            ]
        },
        "emergency_fund": {
            "title": "Emergency Fund",
            "content": "An emergency fund is money set aside for unexpected expenses. It should cover 3-6 months of living expenses.",
            "tips": [
                "Keep in liquid/savings account",
                "Build before making risky investments",
                "Replenish after using",
                "Separate from regular savings"
            ]
        },
        "tax_saving": {
            "title": "Tax Saving Investments",
            "content": "Under Section 80C, you can claim deductions up to Rs.1.5 lakh per year through various investment options.",
            "tips": [
                "ELSS - 3 year lock-in, equity exposure",
                "PPF - 15 year lock-in, guaranteed returns",
                "NPS - Additional Rs.50K under 80CCD(1B)",
                "Life Insurance - Term plan recommended"
            ]
        },
        "retirement": {
            "title": "Retirement Planning",
            "content": "Start early to leverage compound growth. Aim to replace 70-80% of pre-retirement income.",
            "tips": [
                "Start SIP in equity funds early",
                "Contribute to EPF/NPS",
                "Build a diverse retirement corpus",
                "Account for inflation and healthcare costs"
            ]
        }
    }

    topic_lower = topic.lower().replace("-", "_").replace(" ", "_")

    if topic_lower in quick_answers:
        return quick_answers[topic_lower]
    else:
        return {"error": "Topic not found", "available_topics": list(quick_answers.keys())}


@router.get("/status")
async def get_chat_status():
    """Get the current status of chat services."""
    llm_available = check_llm_available()
    return {
        "llm_available": llm_available,
        "fallback_mode": not llm_available,
        "message": "AI advisor is fully operational" if llm_available else "Using smart fallback responses (Ollama not available)"
    }
