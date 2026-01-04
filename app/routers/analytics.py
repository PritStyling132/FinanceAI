"""
Analytics and feedback API routes.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db, User, AnalyticsEvent, Feedback, Holding, FinancialGoal, Expense
from app.routers.auth import get_current_user_from_header


router = APIRouter(prefix="/api", tags=["Analytics"])


# Pydantic models
class AnalyticsEventCreate(BaseModel):
    event_type: str
    event_category: Optional[str] = None
    event_data: Optional[dict] = {}
    page: Optional[str] = None


class FeedbackCreate(BaseModel):
    feedback_type: str
    related_id: Optional[str] = None
    rating: Optional[int] = None
    helpful: Optional[bool] = None
    comment: Optional[str] = None


class AnalyticsSummary(BaseModel):
    total_portfolio_value: float
    total_returns: float
    total_returns_percent: float
    goals_count: int
    goals_achieved: int
    monthly_expenses: float
    savings_rate: float
    risk_score: int
    recommended_allocation: dict


class PerformanceData(BaseModel):
    labels: List[str]
    invested: List[float]
    current: List[float]


@router.post("/analytics/track")
async def track_event(
    event_data: AnalyticsEventCreate,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Track an analytics event."""
    event = AnalyticsEvent(
        user_id=current_user.id,
        event_type=event_data.event_type,
        event_category=event_data.event_category,
        event_data=event_data.event_data,
        page=event_data.page
    )

    db.add(event)
    db.commit()

    return {"message": "Event tracked"}


@router.post("/feedback")
async def submit_feedback(
    feedback_data: FeedbackCreate,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Submit user feedback."""
    feedback = Feedback(
        user_id=current_user.id,
        feedback_type=feedback_data.feedback_type,
        related_id=feedback_data.related_id,
        rating=feedback_data.rating,
        helpful=feedback_data.helpful,
        comment=feedback_data.comment
    )

    db.add(feedback)
    db.commit()

    return {"message": "Feedback submitted"}


@router.get("/analytics/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get overall analytics summary for user."""
    # Portfolio summary
    holdings = db.query(Holding).filter(Holding.user_id == current_user.id).all()

    total_value = 0
    total_invested = 0
    for h in holdings:
        current_price = h.current_price or h.purchase_price
        total_value += h.quantity * current_price
        total_invested += h.quantity * h.purchase_price

    total_returns = total_value - total_invested
    total_returns_percent = (total_returns / total_invested * 100) if total_invested > 0 else 0

    # Goals summary
    goals = db.query(FinancialGoal).filter(FinancialGoal.user_id == current_user.id).all()
    goals_count = len(goals)
    goals_achieved = len([g for g in goals if g.is_achieved])

    # Monthly expenses
    current_month = datetime.utcnow().strftime("%Y-%m")
    monthly_expenses = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id,
        func.strftime('%Y-%m', Expense.date) == current_month
    ).scalar() or 0

    # Savings rate
    monthly_income = (current_user.annual_income or 0) / 12
    savings_rate = ((monthly_income - monthly_expenses) / monthly_income * 100) if monthly_income > 0 else 0

    # Risk score calculation
    risk_score = 5  # Default

    if current_user.age:
        if current_user.age < 30:
            risk_score += 2
        elif current_user.age < 40:
            risk_score += 1
        elif current_user.age > 55:
            risk_score -= 2
        elif current_user.age > 45:
            risk_score -= 1

    if current_user.risk_tolerance == "conservative":
        risk_score -= 2
    elif current_user.risk_tolerance == "aggressive":
        risk_score += 2

    if current_user.investment_horizon:
        if current_user.investment_horizon > 15:
            risk_score += 1
        elif current_user.investment_horizon < 5:
            risk_score -= 2

    risk_score = max(1, min(10, risk_score))

    # Recommended allocation based on risk score
    if risk_score <= 3:
        allocation = {"Stocks": 30, "Bonds": 50, "Cash": 15, "Alternatives": 5}
    elif risk_score <= 5:
        allocation = {"Stocks": 50, "Bonds": 35, "Cash": 10, "Alternatives": 5}
    elif risk_score <= 7:
        allocation = {"Stocks": 65, "Bonds": 25, "Cash": 5, "Alternatives": 5}
    elif risk_score <= 8:
        allocation = {"Stocks": 75, "Bonds": 15, "Cash": 5, "Alternatives": 5}
    else:
        allocation = {"Stocks": 85, "Bonds": 10, "Cash": 0, "Alternatives": 5}

    return AnalyticsSummary(
        total_portfolio_value=total_value,
        total_returns=total_returns,
        total_returns_percent=total_returns_percent,
        goals_count=goals_count,
        goals_achieved=goals_achieved,
        monthly_expenses=monthly_expenses,
        savings_rate=savings_rate,
        risk_score=risk_score,
        recommended_allocation=allocation
    )


@router.get("/analytics/performance", response_model=PerformanceData)
async def get_performance_data(
    months: int = 6,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get portfolio performance data for charts."""
    holdings = db.query(Holding).filter(Holding.user_id == current_user.id).all()

    labels = []
    invested = []
    current = []

    # Generate monthly data points
    now = datetime.utcnow()
    for i in range(months - 1, -1, -1):
        month_date = now - timedelta(days=i * 30)
        month_label = month_date.strftime("%b %Y")
        labels.append(month_label)

        # Calculate values for this month
        month_invested = 0
        month_current = 0

        for h in holdings:
            if h.purchase_date <= month_date:
                month_invested += h.quantity * h.purchase_price
                # Simulate growth (in reality, would need historical prices)
                current_price = h.current_price or h.purchase_price
                growth_factor = 1 + ((months - i) / months) * ((current_price / h.purchase_price) - 1)
                month_current += h.quantity * h.purchase_price * growth_factor

        invested.append(round(month_invested, 2))
        current.append(round(month_current, 2))

    return PerformanceData(
        labels=labels,
        invested=invested,
        current=current
    )


@router.get("/analytics/expense-trends")
async def get_expense_trends(
    months: int = 6,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get expense trends over time."""
    now = datetime.utcnow()
    trends = {}

    for i in range(months - 1, -1, -1):
        month_date = now - timedelta(days=i * 30)
        month_str = month_date.strftime("%Y-%m")
        month_label = month_date.strftime("%b %Y")

        # Get expenses for this month
        month_total = db.query(func.sum(Expense.amount)).filter(
            Expense.user_id == current_user.id,
            func.strftime('%Y-%m', Expense.date) == month_str
        ).scalar() or 0

        trends[month_label] = month_total

    return {"trends": trends}


@router.get("/analytics/category-breakdown")
async def get_category_breakdown(
    month: Optional[str] = None,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get expense breakdown by category."""
    if not month:
        month = datetime.utcnow().strftime("%Y-%m")

    expenses = db.query(Expense).filter(
        Expense.user_id == current_user.id,
        func.strftime('%Y-%m', Expense.date) == month
    ).all()

    breakdown = {}
    for expense in expenses:
        category = expense.category.title()
        breakdown[category] = breakdown.get(category, 0) + expense.amount

    return {"breakdown": breakdown, "total": sum(breakdown.values())}


@router.get("/analytics/goal-progress")
async def get_goal_progress(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get progress on all goals."""
    goals = db.query(FinancialGoal).filter(
        FinancialGoal.user_id == current_user.id
    ).order_by(FinancialGoal.priority.desc()).all()

    progress_data = []
    for goal in goals:
        progress_percent = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
        days_left = max(0, (goal.target_date - datetime.utcnow()).days)

        progress_data.append({
            "id": goal.id,
            "name": goal.name,
            "goal_type": goal.goal_type,
            "progress_percent": round(progress_percent, 1),
            "current_amount": goal.current_amount,
            "target_amount": goal.target_amount,
            "days_left": days_left,
            "is_achieved": goal.is_achieved,
            "on_track": progress_percent >= (100 - (days_left / 365 * 100)) if days_left > 0 else goal.is_achieved
        })

    return {"goals": progress_data}


@router.get("/analytics/insights")
async def get_insights(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get personalized financial insights."""
    insights = []

    # Portfolio insights
    holdings = db.query(Holding).filter(Holding.user_id == current_user.id).all()
    if not holdings:
        insights.append({
            "type": "portfolio",
            "severity": "warning",
            "title": "Start Investing",
            "message": "You haven't added any investments yet. Start building your portfolio today!"
        })
    else:
        total_invested = sum(h.quantity * h.purchase_price for h in holdings)
        total_value = sum(h.quantity * (h.current_price or h.purchase_price) for h in holdings)
        returns_percent = ((total_value - total_invested) / total_invested * 100) if total_invested > 0 else 0

        if returns_percent > 10:
            insights.append({
                "type": "portfolio",
                "severity": "success",
                "title": "Strong Portfolio Performance",
                "message": f"Your portfolio is up {returns_percent:.1f}%! Consider rebalancing if needed."
            })
        elif returns_percent < -5:
            insights.append({
                "type": "portfolio",
                "severity": "warning",
                "title": "Portfolio Down",
                "message": f"Your portfolio is down {abs(returns_percent):.1f}%. Stay calm and consider your long-term goals."
            })

    # Savings insights
    monthly_income = (current_user.annual_income or 0) / 12
    current_month = datetime.utcnow().strftime("%Y-%m")
    monthly_expenses = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id,
        func.strftime('%Y-%m', Expense.date) == current_month
    ).scalar() or 0

    if monthly_income > 0:
        savings_rate = ((monthly_income - monthly_expenses) / monthly_income * 100)
        if savings_rate < 20:
            insights.append({
                "type": "savings",
                "severity": "warning",
                "title": "Low Savings Rate",
                "message": f"Your savings rate is {savings_rate:.1f}%. Try to save at least 20% of your income."
            })
        elif savings_rate > 40:
            insights.append({
                "type": "savings",
                "severity": "success",
                "title": "Excellent Savings",
                "message": f"You're saving {savings_rate:.1f}% of your income. Great discipline!"
            })

    # Goal insights
    goals = db.query(FinancialGoal).filter(
        FinancialGoal.user_id == current_user.id,
        FinancialGoal.is_achieved == False
    ).all()

    for goal in goals:
        days_left = (goal.target_date - datetime.utcnow()).days
        progress = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0

        if days_left < 90 and progress < 80:
            insights.append({
                "type": "goal",
                "severity": "critical",
                "title": f"Goal at Risk: {goal.name}",
                "message": f"Only {days_left} days left and {progress:.1f}% progress. Consider increasing contributions."
            })

    # Emergency fund insight
    if not current_user.has_emergency_fund:
        insights.append({
            "type": "emergency",
            "severity": "warning",
            "title": "Build Emergency Fund",
            "message": "An emergency fund covering 3-6 months of expenses is essential for financial security."
        })

    return {"insights": insights[:10]}  # Limit to 10 insights
