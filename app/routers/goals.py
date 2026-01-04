"""
Financial goals API routes.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
import math

from sqlalchemy.orm import Session
from app.database import get_db, User, FinancialGoal
from app.routers.auth import get_current_user_from_header


router = APIRouter(prefix="/api/goals", tags=["Goals"])


# Pydantic models
class GoalCreate(BaseModel):
    name: str
    goal_type: str = "other"
    target_amount: float
    current_amount: float = 0
    monthly_contribution: float = 0
    target_date: datetime
    priority: int = 3
    notes: Optional[str] = None


class GoalUpdate(BaseModel):
    name: Optional[str] = None
    goal_type: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    monthly_contribution: Optional[float] = None
    target_date: Optional[datetime] = None
    priority: Optional[int] = None
    notes: Optional[str] = None


class GoalResponse(BaseModel):
    id: int
    name: str
    goal_type: str
    target_amount: float
    current_amount: float
    monthly_contribution: float
    target_date: datetime
    priority: int
    is_achieved: bool
    progress_percent: float
    remaining_amount: float
    notes: Optional[str]
    created_at: datetime


class GoalProjection(BaseModel):
    goal_id: int
    projected_completion_date: str
    monthly_required: float
    probability_of_success: float
    shortfall: float
    recommended_adjustments: List[str]
    timeline_data: List[dict]


def calculate_goal_projection(goal: FinancialGoal, assumed_return_rate: float = 0.08) -> GoalProjection:
    """Calculate projection for a goal."""
    now = datetime.utcnow()
    target_date = goal.target_date

    # Months until target
    months_left = max(1, (target_date.year - now.year) * 12 + (target_date.month - now.month))

    # Calculate required monthly contribution
    remaining = goal.target_amount - goal.current_amount
    if remaining <= 0:
        monthly_required = 0
        probability = 100
        shortfall = 0
    else:
        # Simple future value calculation
        monthly_rate = assumed_return_rate / 12
        if monthly_rate > 0:
            # PMT formula for future value
            monthly_required = remaining * monthly_rate / ((1 + monthly_rate) ** months_left - 1)
        else:
            monthly_required = remaining / months_left

        # Calculate probability based on current contribution vs required
        if goal.monthly_contribution >= monthly_required:
            probability = 100
        else:
            probability = min(99, (goal.monthly_contribution / monthly_required) * 100) if monthly_required > 0 else 100

        shortfall = max(0, monthly_required - goal.monthly_contribution) * months_left

    # Calculate projected completion date
    if goal.monthly_contribution > 0 and remaining > 0:
        months_to_complete = math.ceil(remaining / goal.monthly_contribution)
        projected_date = now + timedelta(days=months_to_complete * 30)
    else:
        projected_date = target_date

    # Generate recommendations
    recommendations = []
    if probability < 80:
        recommendations.append(f"Increase monthly contribution by Rs.{int((monthly_required - goal.monthly_contribution)):,} to stay on track")
    if goal.monthly_contribution < goal.target_amount * 0.01:
        recommendations.append("Consider setting up automatic SIP investments for consistent progress")
    if months_left < 24 and probability < 70:
        recommendations.append("Consider extending your target date or reducing the target amount")
    if goal.current_amount < goal.target_amount * 0.1 and months_left < 12:
        recommendations.append("You may need a lump sum investment to reach your goal on time")
    if not recommendations:
        recommendations.append("You're on track to meet your goal! Keep up the good work.")

    # Generate timeline data
    timeline_data = []
    current_value = goal.current_amount
    monthly_rate = assumed_return_rate / 12

    for month in range(min(months_left + 1, 60)):  # Max 5 years projection
        date = now + timedelta(days=month * 30)
        projected_value = current_value + (goal.monthly_contribution * month)
        # Add compound growth
        projected_value *= (1 + monthly_rate) ** month

        timeline_data.append({
            "date": date.strftime("%Y-%m"),
            "projected_value": round(projected_value, 2),
            "target": goal.target_amount
        })

    return GoalProjection(
        goal_id=goal.id,
        projected_completion_date=projected_date.strftime("%Y-%m-%d"),
        monthly_required=round(monthly_required, 2),
        probability_of_success=round(probability, 1),
        shortfall=round(shortfall, 2),
        recommended_adjustments=recommendations,
        timeline_data=timeline_data
    )


@router.get("", response_model=List[GoalResponse])
async def get_goals(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get all goals for current user."""
    goals = db.query(FinancialGoal).filter(
        FinancialGoal.user_id == current_user.id
    ).order_by(FinancialGoal.priority.desc(), FinancialGoal.target_date).all()

    return [
        GoalResponse(
            id=g.id,
            name=g.name,
            goal_type=g.goal_type,
            target_amount=g.target_amount,
            current_amount=g.current_amount,
            monthly_contribution=g.monthly_contribution,
            target_date=g.target_date,
            priority=g.priority,
            is_achieved=g.is_achieved,
            progress_percent=round((g.current_amount / g.target_amount * 100) if g.target_amount > 0 else 0, 1),
            remaining_amount=max(0, g.target_amount - g.current_amount),
            notes=g.notes,
            created_at=g.created_at
        )
        for g in goals
    ]


@router.post("", response_model=GoalResponse)
async def create_goal(
    goal_data: GoalCreate,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Create a new goal."""
    goal = FinancialGoal(
        user_id=current_user.id,
        name=goal_data.name,
        goal_type=goal_data.goal_type,
        target_amount=goal_data.target_amount,
        current_amount=goal_data.current_amount,
        monthly_contribution=goal_data.monthly_contribution,
        target_date=goal_data.target_date,
        priority=goal_data.priority,
        notes=goal_data.notes
    )

    # Check if already achieved
    if goal.current_amount >= goal.target_amount:
        goal.is_achieved = True
        goal.achieved_date = datetime.utcnow()

    db.add(goal)
    db.commit()
    db.refresh(goal)

    return GoalResponse(
        id=goal.id,
        name=goal.name,
        goal_type=goal.goal_type,
        target_amount=goal.target_amount,
        current_amount=goal.current_amount,
        monthly_contribution=goal.monthly_contribution,
        target_date=goal.target_date,
        priority=goal.priority,
        is_achieved=goal.is_achieved,
        progress_percent=round((goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0, 1),
        remaining_amount=max(0, goal.target_amount - goal.current_amount),
        notes=goal.notes,
        created_at=goal.created_at
    )


@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(
    goal_id: int,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get a specific goal."""
    goal = db.query(FinancialGoal).filter(
        FinancialGoal.id == goal_id,
        FinancialGoal.user_id == current_user.id
    ).first()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    return GoalResponse(
        id=goal.id,
        name=goal.name,
        goal_type=goal.goal_type,
        target_amount=goal.target_amount,
        current_amount=goal.current_amount,
        monthly_contribution=goal.monthly_contribution,
        target_date=goal.target_date,
        priority=goal.priority,
        is_achieved=goal.is_achieved,
        progress_percent=round((goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0, 1),
        remaining_amount=max(0, goal.target_amount - goal.current_amount),
        notes=goal.notes,
        created_at=goal.created_at
    )


@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: int,
    goal_data: GoalUpdate,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Update a goal."""
    goal = db.query(FinancialGoal).filter(
        FinancialGoal.id == goal_id,
        FinancialGoal.user_id == current_user.id
    ).first()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    update_data = goal_data.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(goal, key, value)

    # Check if achieved
    if goal.current_amount >= goal.target_amount and not goal.is_achieved:
        goal.is_achieved = True
        goal.achieved_date = datetime.utcnow()

    goal.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(goal)

    return GoalResponse(
        id=goal.id,
        name=goal.name,
        goal_type=goal.goal_type,
        target_amount=goal.target_amount,
        current_amount=goal.current_amount,
        monthly_contribution=goal.monthly_contribution,
        target_date=goal.target_date,
        priority=goal.priority,
        is_achieved=goal.is_achieved,
        progress_percent=round((goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0, 1),
        remaining_amount=max(0, goal.target_amount - goal.current_amount),
        notes=goal.notes,
        created_at=goal.created_at
    )


@router.put("/{goal_id}/progress")
async def update_goal_progress(
    goal_id: int,
    amount: float,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Add contribution to a goal."""
    goal = db.query(FinancialGoal).filter(
        FinancialGoal.id == goal_id,
        FinancialGoal.user_id == current_user.id
    ).first()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    goal.current_amount += amount

    # Check if achieved
    if goal.current_amount >= goal.target_amount and not goal.is_achieved:
        goal.is_achieved = True
        goal.achieved_date = datetime.utcnow()

    goal.updated_at = datetime.utcnow()
    db.commit()

    return {
        "message": "Progress updated",
        "new_amount": goal.current_amount,
        "is_achieved": goal.is_achieved
    }


@router.delete("/{goal_id}")
async def delete_goal(
    goal_id: int,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Delete a goal."""
    goal = db.query(FinancialGoal).filter(
        FinancialGoal.id == goal_id,
        FinancialGoal.user_id == current_user.id
    ).first()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    db.delete(goal)
    db.commit()

    return {"message": "Goal deleted successfully"}


@router.get("/{goal_id}/projection", response_model=GoalProjection)
async def get_goal_projection(
    goal_id: int,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get projection for a goal."""
    goal = db.query(FinancialGoal).filter(
        FinancialGoal.id == goal_id,
        FinancialGoal.user_id == current_user.id
    ).first()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    return calculate_goal_projection(goal)
