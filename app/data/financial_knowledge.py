"""
Financial Knowledge Base - Static content for RAG retrieval.
This provides foundational financial knowledge that the LLM can retrieve.
"""

FINANCIAL_KNOWLEDGE_BASE = [
    # Investment Basics
    {
        "id": "stocks_101",
        "category": "Investment Basics",
        "title": "Understanding Stocks",
        "content": """Stocks represent ownership shares in a company. When you buy stock, you become a partial owner
of that company. Stock prices fluctuate based on company performance, market conditions, and investor sentiment.
Key concepts: Market capitalization (company value), dividends (profit sharing), capital gains (price appreciation).
Stocks are generally considered higher risk but offer higher potential returns over the long term.
Suitable for: Investors with longer time horizons (5+ years) and higher risk tolerance."""
    },
    {
        "id": "bonds_101",
        "category": "Investment Basics",
        "title": "Understanding Bonds",
        "content": """Bonds are debt instruments where you lend money to governments or corporations in exchange
for periodic interest payments and return of principal at maturity. Bond prices move inversely to interest rates.
Key concepts: Coupon rate (interest rate), maturity date, credit rating, yield to maturity.
Bonds are generally lower risk than stocks but offer lower potential returns.
Suitable for: Conservative investors, those nearing retirement, or as portfolio diversification."""
    },
    {
        "id": "mutual_funds_101",
        "category": "Investment Basics",
        "title": "Understanding Mutual Funds",
        "content": """Mutual funds pool money from multiple investors to invest in diversified portfolios of stocks,
bonds, or other securities. They are managed by professional fund managers.
Key concepts: Expense ratio (annual fees), NAV (net asset value), actively managed vs index funds.
Advantages: Diversification, professional management, accessibility.
Disadvantages: Management fees, less control, potential for underperformance.
Suitable for: Investors seeking diversification without individual stock selection."""
    },
    {
        "id": "etfs_101",
        "category": "Investment Basics",
        "title": "Understanding ETFs (Exchange-Traded Funds)",
        "content": """ETFs are investment funds that trade on stock exchanges like individual stocks.
They typically track an index, sector, commodity, or other assets.
Key concepts: Expense ratio (usually lower than mutual funds), intraday trading, index tracking.
Advantages: Low costs, tax efficiency, flexibility, transparency.
Comparison to mutual funds: ETFs trade throughout the day, have lower expense ratios,
but may have trading commissions.
Suitable for: Cost-conscious investors seeking diversified, passive investment strategies."""
    },
    # Risk Management
    {
        "id": "risk_tolerance",
        "category": "Risk Management",
        "title": "Understanding Risk Tolerance",
        "content": """Risk tolerance is your ability and willingness to lose some or all of your investment
in exchange for greater potential returns.
Factors affecting risk tolerance: Age, income stability, financial goals, time horizon, emotional comfort.
Risk categories:
- Conservative: Focus on capital preservation, prefer bonds and stable investments
- Moderate: Balance between growth and stability, mixed portfolio
- Aggressive: Focus on growth, higher allocation to stocks and alternative investments
Your risk tolerance should align with your investment time horizon and financial goals."""
    },
    {
        "id": "diversification",
        "category": "Risk Management",
        "title": "Portfolio Diversification",
        "content": """Diversification is spreading investments across various assets to reduce risk.
The principle: Different assets often perform differently under the same market conditions.
Types of diversification:
- Asset class diversification: Stocks, bonds, real estate, commodities
- Geographic diversification: Domestic, international, emerging markets
- Sector diversification: Technology, healthcare, finance, consumer goods
- Time diversification: Dollar-cost averaging, spreading purchases over time
A well-diversified portfolio can reduce volatility without necessarily sacrificing returns."""
    },
    # Retirement Planning
    {
        "id": "retirement_401k",
        "category": "Retirement Planning",
        "title": "401(k) Retirement Plans",
        "content": """A 401(k) is an employer-sponsored retirement savings plan with tax advantages.
Key features:
- Pre-tax contributions reduce current taxable income
- Employer matching (free money - always contribute enough to get full match)
- 2024 contribution limit: $23,000 ($30,500 if 50+)
- Withdrawals before 59.5 typically incur 10% penalty plus taxes
- Required minimum distributions (RMDs) start at age 73
Investment strategy: Generally, allocate more to stocks when young, gradually shift to bonds as retirement approaches."""
    },
    {
        "id": "retirement_ira",
        "category": "Retirement Planning",
        "title": "Individual Retirement Accounts (IRAs)",
        "content": """IRAs are personal retirement accounts with tax advantages.
Traditional IRA: Pre-tax contributions, tax-deferred growth, taxed on withdrawal.
Roth IRA: After-tax contributions, tax-free growth, tax-free qualified withdrawals.
2024 contribution limit: $7,000 ($8,000 if 50+)
Roth IRA income limits apply for direct contributions.
Strategy considerations:
- Roth if you expect higher taxes in retirement
- Traditional if you expect lower taxes in retirement
- Both can be part of a tax-diversified retirement strategy."""
    },
    # Asset Allocation
    {
        "id": "asset_allocation_basics",
        "category": "Asset Allocation",
        "title": "Asset Allocation Strategies",
        "content": """Asset allocation is dividing investments among different asset categories.
Common allocation strategies:
- Age-based rule: 100 minus your age = stock percentage (e.g., 30 years old = 70% stocks)
- Modern approach: 110 or 120 minus age for longer life expectancy
- Target-date funds: Automatically adjust allocation as you approach retirement

Sample allocations by risk profile:
- Conservative (low risk): 30% stocks, 60% bonds, 10% cash
- Moderate (balanced): 60% stocks, 30% bonds, 10% alternatives
- Aggressive (high risk): 80% stocks, 15% bonds, 5% alternatives

Rebalancing: Periodically adjust portfolio back to target allocation (annually or when drifted 5%+)."""
    },
    {
        "id": "age_based_investing",
        "category": "Asset Allocation",
        "title": "Age-Based Investment Strategies",
        "content": """Investment strategy should evolve with life stage:

20s-30s (Accumulation phase):
- Maximize growth with higher stock allocation (80-90%)
- Take advantage of compound interest
- Focus on retirement account contributions
- Can afford to ride out market volatility

40s-50s (Peak earning years):
- Gradually reduce risk (60-70% stocks)
- Maximize retirement contributions
- Consider catch-up contributions
- Diversify income sources

60s+ (Pre-retirement/Retirement):
- Preserve capital (40-50% stocks)
- Create income streams
- Consider sequence of returns risk
- Plan for healthcare costs and longevity"""
    },
    # Financial Planning
    {
        "id": "emergency_fund",
        "category": "Financial Planning",
        "title": "Emergency Fund Guidelines",
        "content": """An emergency fund is readily accessible money for unexpected expenses.
Recommended amount: 3-6 months of essential expenses (some experts suggest up to 12 months).
Where to keep it: High-yield savings account, money market account - accessible but separate from checking.
What it covers: Job loss, medical emergencies, major repairs, unexpected travel.
Building strategy: Start with $1,000, then build to one month's expenses, then continue to 3-6 months.
Priority: Build emergency fund before aggressive investing (after 401k match)."""
    },
    {
        "id": "debt_management",
        "category": "Financial Planning",
        "title": "Debt Management Strategies",
        "content": """Managing debt is crucial for financial health and investment capacity.
Types of debt:
- Good debt: Low-interest, tax-deductible, builds wealth (mortgage, education loans)
- Bad debt: High-interest, no tax benefits, depreciating assets (credit cards, car loans)

Payoff strategies:
- Avalanche method: Pay highest interest rate first (mathematically optimal)
- Snowball method: Pay smallest balance first (psychologically motivating)

Priority order:
1. Minimum payments on all debts
2. 401k match (guaranteed return)
3. High-interest debt (>7%)
4. Emergency fund
5. Additional retirement savings
6. Low-interest debt vs investing decision"""
    },
    # Tax Efficiency
    {
        "id": "tax_efficient_investing",
        "category": "Tax Efficiency",
        "title": "Tax-Efficient Investment Strategies",
        "content": """Tax efficiency can significantly impact long-term returns.
Account placement strategy:
- Tax-advantaged accounts (401k, IRA): Hold bonds, REITs, high-turnover funds
- Taxable accounts: Hold stocks, index funds, municipal bonds

Tax-loss harvesting: Sell losing investments to offset gains (watch wash sale rules).
Long-term vs short-term gains: Hold investments 1+ year for lower capital gains rates.
Qualified dividends: Taxed at lower capital gains rates.
Municipal bonds: Interest often tax-free at federal and sometimes state level.

Roth conversion: Consider converting Traditional to Roth in low-income years."""
    },
    # Market Concepts
    {
        "id": "market_indicators",
        "category": "Market Analysis",
        "title": "Key Market Indicators",
        "content": """Understanding market indicators helps with investment decisions.
Technical indicators:
- RSI (Relative Strength Index): Momentum indicator, >70 overbought, <30 oversold
- Moving averages: SMA (simple), EMA (exponential) - trend identification
- MACD: Trend and momentum indicator

Fundamental indicators:
- P/E ratio: Price to earnings, valuation measure
- Market cap: Company size classification
- Dividend yield: Income potential

Economic indicators:
- GDP growth: Overall economic health
- Unemployment rate: Labor market strength
- Inflation (CPI): Purchasing power changes
- Interest rates: Cost of borrowing, affects all asset values"""
    },
    {
        "id": "market_cycles",
        "category": "Market Analysis",
        "title": "Understanding Market Cycles",
        "content": """Markets move in cycles that affect investment strategy.
Bull market: Sustained period of rising prices, optimism, economic growth.
Bear market: 20%+ decline from recent highs, pessimism, often recession.

Cycle phases:
1. Accumulation: Smart money buys after bear market
2. Mark-up: Prices rise, broader participation
3. Distribution: Smart money sells, volatility increases
4. Mark-down: Prices fall, pessimism dominates

Investment implications:
- Time in market beats timing the market
- Dollar-cost averaging smooths entry points
- Rebalancing forces buy low, sell high
- Stay invested through cycles for long-term growth"""
    },
    # Goal-Based Planning
    {
        "id": "goal_based_planning",
        "category": "Goal Planning",
        "title": "Goal-Based Financial Planning",
        "content": """Align investments with specific financial goals.
Short-term goals (0-3 years):
- Keep in savings, CDs, money market
- Prioritize capital preservation
- Examples: Emergency fund, vacation, car purchase

Medium-term goals (3-10 years):
- Moderate risk, balanced portfolio
- Consider bond-heavy allocation
- Examples: Home down payment, education funding

Long-term goals (10+ years):
- Higher risk tolerance, growth-focused
- Stock-heavy allocation appropriate
- Examples: Retirement, legacy planning

For each goal: Define amount needed, timeline, and appropriate investment vehicle."""
    },
    # Investment Wisdom
    {
        "id": "common_mistakes",
        "category": "Investment Wisdom",
        "title": "Common Investment Mistakes to Avoid",
        "content": """Avoiding common mistakes can significantly improve returns.
Behavioral mistakes:
- Panic selling during market downturns
- Chasing past performance
- Overconfidence in stock picking
- Emotional decision making

Strategy mistakes:
- Not diversifying adequately
- Ignoring fees and expenses
- Trying to time the market
- Neglecting rebalancing

Planning mistakes:
- Starting too late (missing compound growth)
- Not maximizing employer match
- Underestimating retirement needs
- Ignoring tax implications

Key principle: Have a plan, stick to it, adjust only for life changes not market movements."""
    },
]


def get_knowledge_documents() -> list[dict]:
    """Return knowledge base formatted for embedding and storage."""
    documents = []
    for item in FINANCIAL_KNOWLEDGE_BASE:
        documents.append({
            "id": item["id"],
            "content": f"{item['title']}\n\n{item['content']}",
            "metadata": {
                "category": item["category"],
                "title": item["title"],
            }
        })
    return documents
