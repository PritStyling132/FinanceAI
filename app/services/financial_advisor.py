from typing import Optional

from app.models.user_profile import UserProfile, RiskTolerance, UserGoal
from app.services.rag_pipeline import RAGPipeline
from app.services.alpha_vantage import AlphaVantageService
from app.utils.guardrails import Guardrails


class FinancialAdvisor:
    def __init__(self):
        self.rag_pipeline = RAGPipeline()
        self.alpha_vantage = AlphaVantageService()
        self.guardrails = Guardrails()

    def get_advice(
        self,
        query: str,
        user_profile: Optional[UserProfile] = None,
        chat_history: Optional[list[dict]] = None,
    ) -> dict:
        """Get personalized financial advice."""
        processed_query = self.guardrails.preprocess_query(query)

        response = self.rag_pipeline.generate_response(
            query=processed_query,
            user_profile=user_profile,
            chat_history=chat_history,
            include_market_data=True,
        )

        response = self.guardrails.postprocess_response(response)

        return {
            "response": response,
            "disclaimer": self.guardrails.get_disclaimer(),
        }

    def get_portfolio_recommendation(self, user_profile: UserProfile) -> dict:
        """Generate portfolio recommendation based on user profile."""
        allocation = user_profile.get_recommended_allocation()
        risk_score = user_profile.get_risk_score()

        recommendation_query = f"""Based on this user profile, provide specific investment recommendations:
- Age: {user_profile.age}
- Risk tolerance: {user_profile.risk_tolerance.value}
- Investment horizon: {user_profile.investment_horizon} years
- Monthly investment capacity: ${user_profile.monthly_investment}
- Goals: {', '.join(g.value for g in user_profile.goals)}
- Risk score calculated: {risk_score}/10
- Suggested allocation: {allocation['stocks']}% stocks, {allocation['bonds']}% bonds, {allocation['cash']}% cash

Provide specific ETF or fund suggestions for each asset class and explain why this allocation suits their profile."""

        advice = self.get_advice(recommendation_query, user_profile)

        return {
            "risk_score": risk_score,
            "allocation": allocation,
            "detailed_advice": advice["response"],
            "disclaimer": advice["disclaimer"],
        }

    def analyze_investment(self, symbol: str, user_profile: Optional[UserProfile] = None) -> dict:
        """Analyze a specific investment/stock."""
        quote = self.alpha_vantage.get_stock_quote(symbol)
        overview = self.alpha_vantage.get_company_overview(symbol)
        rsi = self.alpha_vantage.get_technical_indicator(symbol, "RSI")

        if not quote:
            return {
                "error": f"Could not fetch data for symbol: {symbol}",
                "symbol": symbol,
            }

        market_context = f"""Analyze {symbol} for investment:
Current Price: ${quote['price']:.2f}
Change: {quote['change_percent']}
"""
        if overview:
            market_context += f"""
Company: {overview.get('name', 'N/A')}
Sector: {overview.get('sector', 'N/A')}
P/E Ratio: {overview.get('pe_ratio', 'N/A')}
Market Cap: {overview.get('market_cap', 'N/A')}
"""
        if rsi and rsi.get("values"):
            market_context += f"\nRSI (14): {rsi['values'][0]['value']:.2f}"

        if user_profile:
            market_context += f"""

Consider this for a {user_profile.risk_tolerance.value} investor with {user_profile.investment_horizon} year horizon."""

        market_context += "\n\nProvide analysis of whether this stock suits the investor profile, potential risks, and recommendation."

        advice = self.get_advice(market_context, user_profile)

        return {
            "symbol": symbol,
            "quote": quote,
            "overview": overview,
            "technical": {"rsi": rsi},
            "analysis": advice["response"],
            "disclaimer": advice["disclaimer"],
        }

    def get_goal_based_plan(self, user_profile: UserProfile) -> dict:
        """Create a goal-based financial plan."""
        goals_text = ", ".join(g.value for g in user_profile.goals)

        plan_query = f"""Create a comprehensive financial plan for achieving these goals: {goals_text}

User Profile:
- Age: {user_profile.age}
- Annual Income: ${user_profile.annual_income:,}
- Current Savings: ${user_profile.current_savings:,}
- Monthly Investment: ${user_profile.monthly_investment:,}
- Debt: ${user_profile.debt_amount:,}
- Risk Tolerance: {user_profile.risk_tolerance.value}
- Has Emergency Fund: {user_profile.has_emergency_fund}
- Has Retirement Account: {user_profile.has_retirement_account}

Provide:
1. Priority order for goals
2. Timeline for each goal
3. Monthly savings targets
4. Recommended accounts/investment vehicles
5. Key milestones to track"""

        advice = self.get_advice(plan_query, user_profile)

        return {
            "goals": [g.value for g in user_profile.goals],
            "allocation": user_profile.get_recommended_allocation(),
            "plan": advice["response"],
            "disclaimer": advice["disclaimer"],
        }

    def answer_question(
        self,
        question: str,
        user_profile: Optional[UserProfile] = None,
        chat_history: Optional[list[dict]] = None,
    ) -> dict:
        """Answer a general financial question."""
        return self.get_advice(question, user_profile, chat_history)
