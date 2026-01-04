"""
Investment recommendations API routes.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from sqlalchemy.orm import Session
from app.database import get_db, User, Holding, FinancialGoal
from app.routers.auth import get_current_user_from_header
from app.services.financial_advisor import FinancialAdvisor
from app.models.user_profile import UserProfile, RiskTolerance, UserGoal


router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

# Initialize financial advisor service
financial_advisor = None


def get_financial_advisor():
    global financial_advisor
    if financial_advisor is None:
        financial_advisor = FinancialAdvisor()
    return financial_advisor


# Pydantic models
class RecommendationResponse(BaseModel):
    id: str
    type: str  # asset_allocation, stock, mutual_fund, action
    title: str
    description: str
    priority: str  # high, medium, low
    category: str
    action_items: List[str]
    metrics: Optional[dict] = None
    created_at: datetime


class PortfolioRecommendation(BaseModel):
    risk_profile: str
    risk_score: int
    current_allocation: dict
    recommended_allocation: dict
    rebalancing_suggestions: List[dict]
    diversification_score: float


class GoalRecommendation(BaseModel):
    goal_id: int
    goal_name: str
    recommended_monthly_sip: float
    recommended_investment_type: str
    expected_return_rate: float
    risk_level: str
    specific_recommendations: List[str]


@router.get("", response_model=List[RecommendationResponse])
async def get_recommendations(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get personalized recommendations for user."""
    recommendations = []
    now = datetime.utcnow()

    # Get user's holdings and goals
    holdings = db.query(Holding).filter(Holding.user_id == current_user.id).all()
    goals = db.query(FinancialGoal).filter(FinancialGoal.user_id == current_user.id).all()

    # 1. Emergency Fund Recommendation
    if not current_user.has_emergency_fund:
        monthly_income = (current_user.annual_income or 0) / 12
        emergency_fund_target = monthly_income * 6

        recommendations.append(RecommendationResponse(
            id=f"rec-emergency-{current_user.id}",
            type="action",
            title="Build Emergency Fund",
            description=f"Build an emergency fund of Rs.{int(emergency_fund_target):,} (6 months of expenses) before making aggressive investments.",
            priority="high",
            category="Emergency Fund",
            action_items=[
                "Open a high-yield savings account",
                f"Set up automatic transfer of Rs.{int(emergency_fund_target / 12):,} monthly",
                "Keep 3-6 months of expenses in liquid form"
            ],
            metrics={"target_amount": emergency_fund_target, "timeline_months": 12},
            created_at=now
        ))

    # 2. Asset Allocation Recommendations
    risk_score = calculate_risk_score(current_user)
    recommended_allocation = get_recommended_allocation(risk_score)

    if holdings:
        current_allocation = calculate_current_allocation(holdings)
        rebalancing_needed = check_rebalancing_needed(current_allocation, recommended_allocation)

        if rebalancing_needed:
            recommendations.append(RecommendationResponse(
                id=f"rec-rebalance-{current_user.id}",
                type="asset_allocation",
                title="Portfolio Rebalancing Needed",
                description="Your current portfolio allocation differs from your target allocation based on your risk profile.",
                priority="medium",
                category="Portfolio",
                action_items=generate_rebalancing_actions(current_allocation, recommended_allocation),
                metrics={
                    "current": current_allocation,
                    "recommended": recommended_allocation
                },
                created_at=now
            ))

    # 3. Diversification Recommendations
    if holdings:
        asset_types = set(h.asset_type for h in holdings)
        if len(asset_types) < 3:
            recommendations.append(RecommendationResponse(
                id=f"rec-diversify-{current_user.id}",
                type="action",
                title="Diversify Your Portfolio",
                description="Your portfolio is concentrated in few asset classes. Consider diversifying across stocks, bonds, and other asset classes.",
                priority="medium",
                category="Portfolio",
                action_items=[
                    "Add index funds for broad market exposure",
                    "Consider debt funds for stability",
                    "Explore international funds for geographical diversification"
                ],
                metrics={"current_asset_types": len(asset_types), "recommended_minimum": 4},
                created_at=now
            ))

    # 4. SIP Recommendations based on Goals
    for goal in goals:
        if not goal.is_achieved:
            days_left = (goal.target_date - now).days
            remaining = goal.target_amount - goal.current_amount

            if days_left > 0 and remaining > 0:
                # Calculate required SIP
                months_left = max(1, days_left / 30)
                required_sip = remaining / months_left

                if required_sip > goal.monthly_contribution * 1.2:  # 20% buffer
                    recommendations.append(RecommendationResponse(
                        id=f"rec-goal-{goal.id}",
                        type="action",
                        title=f"Increase SIP for {goal.name}",
                        description=f"Your current contribution may not be sufficient to reach your {goal.name} goal on time.",
                        priority="high" if days_left < 365 else "medium",
                        category="Goals",
                        action_items=[
                            f"Increase monthly SIP from Rs.{int(goal.monthly_contribution):,} to Rs.{int(required_sip):,}",
                            f"Consider extending target date by {int((required_sip - goal.monthly_contribution) / required_sip * months_left)} months",
                            "Review and adjust target amount if needed"
                        ],
                        metrics={
                            "current_sip": goal.monthly_contribution,
                            "required_sip": required_sip,
                            "gap": required_sip - goal.monthly_contribution
                        },
                        created_at=now
                    ))

    # 5. Investment Type Recommendations based on Risk Profile
    if current_user.risk_tolerance == "conservative":
        recommendations.append(RecommendationResponse(
            id=f"rec-invest-conservative-{current_user.id}",
            type="mutual_fund",
            title="Conservative Investment Options",
            description="Based on your risk profile, consider these low-risk investment options.",
            priority="low",
            category="Investments",
            action_items=[
                "Debt Mutual Funds - For stable returns with low risk",
                "PPF - Tax-free returns with 15-year lock-in",
                "Bank Fixed Deposits - Guaranteed returns",
                "Corporate Bonds - Higher returns than FD with moderate risk"
            ],
            metrics={"expected_return": "6-8%", "risk_level": "Low"},
            created_at=now
        ))
    elif current_user.risk_tolerance == "aggressive":
        recommendations.append(RecommendationResponse(
            id=f"rec-invest-aggressive-{current_user.id}",
            type="stock",
            title="Growth Investment Options",
            description="Based on your risk profile, consider these high-growth investment options.",
            priority="low",
            category="Investments",
            action_items=[
                "Equity Mutual Funds - Diversified stock exposure",
                "Direct Stocks - Individual company investments",
                "Small Cap Funds - Higher risk, higher potential returns",
                "International Funds - Global market exposure"
            ],
            metrics={"expected_return": "12-15%", "risk_level": "High"},
            created_at=now
        ))
    else:
        recommendations.append(RecommendationResponse(
            id=f"rec-invest-balanced-{current_user.id}",
            type="mutual_fund",
            title="Balanced Investment Options",
            description="Based on your risk profile, consider these balanced investment options.",
            priority="low",
            category="Investments",
            action_items=[
                "Balanced Advantage Funds - Dynamic equity-debt allocation",
                "Large Cap Funds - Stable blue-chip companies",
                "Hybrid Funds - Mix of equity and debt",
                "Index Funds - Low-cost market tracking"
            ],
            metrics={"expected_return": "10-12%", "risk_level": "Moderate"},
            created_at=now
        ))

    # 6. Tax Saving Recommendations
    if current_user.annual_income and current_user.annual_income > 500000:
        recommendations.append(RecommendationResponse(
            id=f"rec-tax-{current_user.id}",
            type="action",
            title="Tax Saving Opportunities",
            description="Maximize your tax savings under Section 80C and other provisions.",
            priority="medium",
            category="Tax",
            action_items=[
                "ELSS Mutual Funds - Rs.1.5L limit with 3-year lock-in",
                "PPF - Rs.1.5L limit with 15-year lock-in",
                "NPS - Additional Rs.50K deduction under 80CCD(1B)",
                "Health Insurance - Rs.25K-50K deduction under 80D"
            ],
            metrics={"max_deduction": 200000, "potential_savings": int(current_user.annual_income * 0.3 * 0.1)},
            created_at=now
        ))

    return recommendations


@router.get("/portfolio", response_model=PortfolioRecommendation)
async def get_portfolio_recommendation(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get detailed portfolio recommendation."""
    holdings = db.query(Holding).filter(Holding.user_id == current_user.id).all()

    risk_score = calculate_risk_score(current_user)
    risk_profile = get_risk_profile_name(risk_score)
    recommended_allocation = get_recommended_allocation(risk_score)

    current_allocation = {}
    rebalancing_suggestions = []
    diversification_score = 0

    if holdings:
        current_allocation = calculate_current_allocation(holdings)

        # Calculate diversification score (0-100)
        asset_types = len(set(h.asset_type for h in holdings))
        unique_symbols = len(set(h.symbol for h in holdings))
        diversification_score = min(100, (asset_types * 15) + (unique_symbols * 5))

        # Generate rebalancing suggestions
        for asset_class, target_pct in recommended_allocation.items():
            current_pct = current_allocation.get(asset_class, 0)
            diff = target_pct - current_pct

            if abs(diff) > 5:  # 5% threshold
                action = "increase" if diff > 0 else "decrease"
                rebalancing_suggestions.append({
                    "asset_class": asset_class,
                    "current_percent": current_pct,
                    "target_percent": target_pct,
                    "action": action,
                    "adjustment_percent": abs(diff)
                })

    return PortfolioRecommendation(
        risk_profile=risk_profile,
        risk_score=risk_score,
        current_allocation=current_allocation,
        recommended_allocation=recommended_allocation,
        rebalancing_suggestions=rebalancing_suggestions,
        diversification_score=diversification_score
    )


@router.get("/goals/{goal_id}", response_model=GoalRecommendation)
async def get_goal_recommendation(
    goal_id: int,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get investment recommendation for a specific goal."""
    goal = db.query(FinancialGoal).filter(
        FinancialGoal.id == goal_id,
        FinancialGoal.user_id == current_user.id
    ).first()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    # Calculate time horizon
    days_left = max(1, (goal.target_date - datetime.utcnow()).days)
    years_left = days_left / 365

    # Determine investment type based on time horizon
    if years_left < 2:
        investment_type = "Debt Funds / FDs"
        expected_return = 6
        risk_level = "Low"
        specific_recommendations = [
            "Short Duration Debt Funds",
            "Bank Fixed Deposits",
            "Liquid Funds for emergency accessibility"
        ]
    elif years_left < 5:
        investment_type = "Balanced / Hybrid Funds"
        expected_return = 9
        risk_level = "Moderate"
        specific_recommendations = [
            "Balanced Advantage Funds",
            "Conservative Hybrid Funds",
            "Large Cap Equity Funds (partial allocation)"
        ]
    else:
        investment_type = "Equity Funds"
        expected_return = 12
        risk_level = "Moderate to High"
        specific_recommendations = [
            "Flexi Cap Equity Funds",
            "Large & Mid Cap Funds",
            "Index Funds for long-term wealth creation"
        ]

    # Calculate recommended monthly SIP
    remaining = goal.target_amount - goal.current_amount
    months_left = max(1, days_left / 30)
    monthly_rate = expected_return / 100 / 12

    # Using future value of annuity formula
    if monthly_rate > 0:
        recommended_sip = remaining * monthly_rate / ((1 + monthly_rate) ** months_left - 1)
    else:
        recommended_sip = remaining / months_left

    return GoalRecommendation(
        goal_id=goal.id,
        goal_name=goal.name,
        recommended_monthly_sip=round(recommended_sip, 2),
        recommended_investment_type=investment_type,
        expected_return_rate=expected_return,
        risk_level=risk_level,
        specific_recommendations=specific_recommendations
    )


@router.post("/ai-advice")
async def get_ai_advice(
    question: Optional[str] = None,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get AI-powered financial advice with fallback responses."""
    try:
        advisor = get_financial_advisor()

        if advisor:
            # Build user profile for the advisor
            user_profile = UserProfile(
                name=current_user.full_name,
                age=current_user.age or 30,
                annual_income=current_user.annual_income or 0,
                current_savings=current_user.current_savings or 0,
                monthly_investment=current_user.monthly_investment or 0,
                debt_amount=current_user.debt_amount or 0,
                risk_tolerance=RiskTolerance(current_user.risk_tolerance or "moderate"),
                investment_horizon=current_user.investment_horizon or 10,
                goals=[UserGoal(g) if g in [e.value for e in UserGoal] else UserGoal.OTHER for g in (current_user.goals or [])],
                has_emergency_fund=current_user.has_emergency_fund or False,
                has_retirement_account=current_user.has_retirement_account or False
            )

            if question:
                result = advisor.answer_question(question, user_profile)
            else:
                result = advisor.get_portfolio_recommendation(user_profile)

            return result
    except Exception as e:
        print(f"AI advice error: {e}")

    # Fallback response when LLM is unavailable
    risk_score = calculate_risk_score(current_user)
    recommended_allocation = get_recommended_allocation(risk_score)
    risk_profile = get_risk_profile_name(risk_score)

    return {
        "risk_score": risk_score,
        "allocation": recommended_allocation,
        "detailed_advice": generate_fallback_advice(current_user, risk_profile, recommended_allocation),
        "disclaimer": "This is automated financial guidance for educational purposes only. Please consult a SEBI-registered advisor for personalized advice."
    }


def generate_fallback_advice(user: User, risk_profile: str, allocation: dict) -> str:
    """Generate fallback advice when LLM is unavailable."""
    age_str = f"{user.age} years old" if user.age else "your age"
    income_str = f"Rs.{user.annual_income:,}" if user.annual_income else "your income"

    advice = f"""**Personalized Investment Recommendations**

Based on your profile analysis, here's your recommended financial strategy:

**Your Risk Profile: {risk_profile}**
- Risk Score: {calculate_risk_score(user)}/10
- Investment Horizon: {user.investment_horizon or 10} years

**Recommended Asset Allocation:**
"""

    for asset_class, pct in allocation.items():
        advice += f"- {asset_class}: {pct}%\n"

    advice += """
**Key Recommendations:**

1. **Emergency Fund First**"""

    if not user.has_emergency_fund:
        monthly = (user.annual_income or 600000) / 12
        advice += f"""
   - Build an emergency fund of Rs.{int(monthly * 6):,} (6 months of expenses)
   - Keep it in a savings account or liquid fund"""
    else:
        advice += """
   - Great! You already have an emergency fund
   - Review it annually to match your expenses"""

    advice += """

2. **Investment Strategy**"""

    if user.risk_tolerance == "conservative":
        advice += """
   - Focus on debt funds and fixed deposits
   - Consider PPF for tax-free, risk-free returns
   - Allocate 30% or less to equity via SIPs"""
    elif user.risk_tolerance == "aggressive":
        advice += """
   - Maximize equity allocation through diversified funds
   - Consider small and mid-cap funds for growth
   - Use market corrections to invest more"""
    else:
        advice += """
   - Maintain a balanced 50-50 equity-debt split
   - Use balanced advantage funds for auto-rebalancing
   - Invest through SIPs for rupee cost averaging"""

    advice += """

3. **Tax Optimization**
   - Utilize Rs.1.5 lakh under Section 80C
   - Consider ELSS funds for tax saving with equity exposure
   - NPS offers additional Rs.50,000 deduction under 80CCD(1B)

4. **Regular Review**
   - Review portfolio quarterly
   - Rebalance annually
   - Increase SIP by 10% yearly with income growth

**Specific Fund Suggestions:**
"""

    if user.risk_tolerance == "conservative":
        advice += """- HDFC Short Term Debt Fund - For stability
- SBI Magnum Gilt Fund - Government securities
- ICICI Prudential Balanced Advantage Fund - Conservative hybrid"""
    elif user.risk_tolerance == "aggressive":
        advice += """- Parag Parikh Flexi Cap Fund - Diversified equity
- Mirae Asset Large Cap Fund - Blue-chip exposure
- Kotak Small Cap Fund - High growth potential"""
    else:
        advice += """- UTI Nifty 50 Index Fund - Low-cost market tracking
- HDFC Balanced Advantage Fund - Dynamic allocation
- Axis Bluechip Fund - Quality large caps"""

    return advice


# Helper functions
def calculate_risk_score(user: User) -> int:
    """Calculate risk score from 1-10."""
    score = 5

    if user.age:
        if user.age < 30:
            score += 2
        elif user.age < 40:
            score += 1
        elif user.age > 55:
            score -= 2
        elif user.age > 45:
            score -= 1

    if user.risk_tolerance == "conservative":
        score -= 2
    elif user.risk_tolerance == "aggressive":
        score += 2

    if user.investment_horizon:
        if user.investment_horizon > 15:
            score += 1
        elif user.investment_horizon < 5:
            score -= 2

    if not user.has_emergency_fund:
        score -= 1

    if user.debt_amount and user.annual_income:
        debt_ratio = user.debt_amount / user.annual_income
        if debt_ratio > 0.5:
            score -= 2
        elif debt_ratio > 0.3:
            score -= 1

    return max(1, min(10, score))


def get_risk_profile_name(score: int) -> str:
    """Get risk profile name from score."""
    if score <= 3:
        return "Conservative"
    elif score <= 5:
        return "Moderate-Conservative"
    elif score <= 7:
        return "Moderate"
    elif score <= 8:
        return "Moderate-Aggressive"
    else:
        return "Aggressive"


def get_recommended_allocation(risk_score: int) -> dict:
    """Get recommended asset allocation based on risk score."""
    if risk_score <= 3:
        return {"Stocks": 30, "Bonds": 50, "Cash": 15, "Alternatives": 5}
    elif risk_score <= 5:
        return {"Stocks": 50, "Bonds": 35, "Cash": 10, "Alternatives": 5}
    elif risk_score <= 7:
        return {"Stocks": 65, "Bonds": 25, "Cash": 5, "Alternatives": 5}
    elif risk_score <= 8:
        return {"Stocks": 75, "Bonds": 15, "Cash": 5, "Alternatives": 5}
    else:
        return {"Stocks": 85, "Bonds": 10, "Cash": 0, "Alternatives": 5}


def calculate_current_allocation(holdings: List[Holding]) -> dict:
    """Calculate current portfolio allocation."""
    total_value = 0
    allocation = {}

    for h in holdings:
        current_price = h.current_price or h.purchase_price
        value = h.quantity * current_price
        total_value += value

        # Map asset types to allocation categories
        category = map_asset_type_to_category(h.asset_type)
        allocation[category] = allocation.get(category, 0) + value

    # Convert to percentages
    if total_value > 0:
        allocation = {k: round(v / total_value * 100, 1) for k, v in allocation.items()}

    return allocation


def map_asset_type_to_category(asset_type: str) -> str:
    """Map asset type to allocation category."""
    mapping = {
        "stock": "Stocks",
        "etf": "Stocks",
        "mutual_fund": "Stocks",
        "bond": "Bonds",
        "crypto": "Alternatives",
        "real_estate": "Alternatives",
        "gold": "Alternatives",
        "cash": "Cash"
    }
    return mapping.get(asset_type.lower(), "Alternatives")


def check_rebalancing_needed(current: dict, target: dict) -> bool:
    """Check if portfolio rebalancing is needed."""
    for asset_class, target_pct in target.items():
        current_pct = current.get(asset_class, 0)
        if abs(target_pct - current_pct) > 10:  # 10% threshold
            return True
    return False


def generate_rebalancing_actions(current: dict, target: dict) -> List[str]:
    """Generate rebalancing action items."""
    actions = []
    for asset_class, target_pct in target.items():
        current_pct = current.get(asset_class, 0)
        diff = target_pct - current_pct

        if diff > 5:
            actions.append(f"Increase {asset_class} allocation by {diff:.1f}%")
        elif diff < -5:
            actions.append(f"Decrease {asset_class} allocation by {abs(diff):.1f}%")

    return actions if actions else ["Portfolio is well balanced"]
