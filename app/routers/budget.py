"""
Budget and expense management API routes.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db, User, Budget, Expense
from app.routers.auth import get_current_user_from_header


router = APIRouter(prefix="/api/budget", tags=["Budget"])


# Pydantic models
class BudgetCreate(BaseModel):
    month: str  # YYYY-MM format
    income: float = 0
    total_budget: float = 0
    category_budgets: Dict[str, float] = {}


class BudgetUpdate(BaseModel):
    income: Optional[float] = None
    total_budget: Optional[float] = None
    category_budgets: Optional[Dict[str, float]] = None


class BudgetResponse(BaseModel):
    id: int
    month: str
    income: float
    total_budget: float
    category_budgets: dict
    total_spent: float
    remaining: float
    savings: float
    savings_rate: float


class ExpenseCreate(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None
    date: datetime
    payment_method: Optional[str] = None
    is_recurring: bool = False


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    payment_method: Optional[str] = None
    is_recurring: Optional[bool] = None


class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category: str
    description: Optional[str]
    date: datetime
    payment_method: Optional[str]
    is_recurring: bool
    created_at: datetime


class BudgetSummary(BaseModel):
    month: str
    income: float
    total_budget: float
    total_spent: float
    remaining: float
    savings: float
    savings_rate: float
    category_breakdown: Dict[str, float]
    budget_vs_actual: Dict[str, dict]


# Default expense categories
DEFAULT_CATEGORIES = [
    "food",
    "transport",
    "utilities",
    "entertainment",
    "shopping",
    "healthcare",
    "education",
    "rent",
    "insurance",
    "investments",
    "other"
]


@router.get("", response_model=List[BudgetResponse])
async def get_budgets(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get all budgets for current user."""
    budgets = db.query(Budget).filter(Budget.user_id == current_user.id).order_by(Budget.month.desc()).all()

    result = []
    for b in budgets:
        # Calculate total spent for this month
        total_spent = db.query(func.sum(Expense.amount)).filter(
            Expense.user_id == current_user.id,
            func.strftime('%Y-%m', Expense.date) == b.month
        ).scalar() or 0

        remaining = b.total_budget - total_spent
        savings = b.income - total_spent
        savings_rate = (savings / b.income * 100) if b.income > 0 else 0

        result.append(BudgetResponse(
            id=b.id,
            month=b.month,
            income=b.income,
            total_budget=b.total_budget,
            category_budgets=b.category_budgets or {},
            total_spent=total_spent,
            remaining=remaining,
            savings=savings,
            savings_rate=savings_rate
        ))

    return result


@router.post("", response_model=BudgetResponse)
async def create_budget(
    budget_data: BudgetCreate,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Create a new budget."""
    # Check if budget for this month already exists
    existing = db.query(Budget).filter(
        Budget.user_id == current_user.id,
        Budget.month == budget_data.month
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Budget for this month already exists")

    budget = Budget(
        user_id=current_user.id,
        month=budget_data.month,
        income=budget_data.income,
        total_budget=budget_data.total_budget,
        category_budgets=budget_data.category_budgets
    )

    db.add(budget)
    db.commit()
    db.refresh(budget)

    return BudgetResponse(
        id=budget.id,
        month=budget.month,
        income=budget.income,
        total_budget=budget.total_budget,
        category_budgets=budget.category_budgets or {},
        total_spent=0,
        remaining=budget.total_budget,
        savings=budget.income,
        savings_rate=100 if budget.income > 0 else 0
    )


@router.get("/{month}", response_model=BudgetResponse)
async def get_budget_by_month(
    month: str,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get budget for a specific month."""
    budget = db.query(Budget).filter(
        Budget.user_id == current_user.id,
        Budget.month == month
    ).first()

    if not budget:
        # Create a default budget if none exists
        budget = Budget(
            user_id=current_user.id,
            month=month,
            income=0,
            total_budget=0,
            category_budgets={}
        )
        db.add(budget)
        db.commit()
        db.refresh(budget)

    # Calculate total spent
    total_spent = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id,
        func.strftime('%Y-%m', Expense.date) == month
    ).scalar() or 0

    remaining = budget.total_budget - total_spent
    savings = budget.income - total_spent
    savings_rate = (savings / budget.income * 100) if budget.income > 0 else 0

    return BudgetResponse(
        id=budget.id,
        month=budget.month,
        income=budget.income,
        total_budget=budget.total_budget,
        category_budgets=budget.category_budgets or {},
        total_spent=total_spent,
        remaining=remaining,
        savings=savings,
        savings_rate=savings_rate
    )


@router.put("/{month}", response_model=BudgetResponse)
async def update_budget(
    month: str,
    budget_data: BudgetUpdate,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Update budget for a specific month."""
    budget = db.query(Budget).filter(
        Budget.user_id == current_user.id,
        Budget.month == month
    ).first()

    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    update_data = budget_data.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(budget, key, value)

    budget.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(budget)

    # Calculate total spent
    total_spent = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id,
        func.strftime('%Y-%m', Expense.date) == month
    ).scalar() or 0

    remaining = budget.total_budget - total_spent
    savings = budget.income - total_spent
    savings_rate = (savings / budget.income * 100) if budget.income > 0 else 0

    return BudgetResponse(
        id=budget.id,
        month=budget.month,
        income=budget.income,
        total_budget=budget.total_budget,
        category_budgets=budget.category_budgets or {},
        total_spent=total_spent,
        remaining=remaining,
        savings=savings,
        savings_rate=savings_rate
    )


@router.get("/summary", response_model=BudgetSummary)
async def get_budget_summary(
    month: Optional[str] = None,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get budget summary with breakdown."""
    if not month:
        month = datetime.utcnow().strftime("%Y-%m")

    # Get or create budget
    budget = db.query(Budget).filter(
        Budget.user_id == current_user.id,
        Budget.month == month
    ).first()

    if not budget:
        budget = Budget(
            user_id=current_user.id,
            month=month,
            income=current_user.annual_income / 12 if current_user.annual_income else 0,
            total_budget=0,
            category_budgets={}
        )
        db.add(budget)
        db.commit()
        db.refresh(budget)

    # Get expenses by category
    expenses = db.query(Expense).filter(
        Expense.user_id == current_user.id,
        func.strftime('%Y-%m', Expense.date) == month
    ).all()

    category_breakdown = {}
    for expense in expenses:
        category = expense.category
        category_breakdown[category] = category_breakdown.get(category, 0) + expense.amount

    total_spent = sum(category_breakdown.values())
    remaining = budget.total_budget - total_spent
    savings = budget.income - total_spent
    savings_rate = (savings / budget.income * 100) if budget.income > 0 else 0

    # Budget vs Actual comparison
    budget_vs_actual = {}
    for category, budgeted in (budget.category_budgets or {}).items():
        actual = category_breakdown.get(category, 0)
        budget_vs_actual[category] = {
            "budgeted": budgeted,
            "actual": actual,
            "remaining": budgeted - actual,
            "percent_used": (actual / budgeted * 100) if budgeted > 0 else 0
        }

    return BudgetSummary(
        month=month,
        income=budget.income,
        total_budget=budget.total_budget,
        total_spent=total_spent,
        remaining=remaining,
        savings=savings,
        savings_rate=savings_rate,
        category_breakdown=category_breakdown,
        budget_vs_actual=budget_vs_actual
    )


# Expense endpoints
@router.get("/expenses/all", response_model=List[ExpenseResponse])
async def get_all_expenses(
    month: Optional[str] = None,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get all expenses with optional filters."""
    query = db.query(Expense).filter(Expense.user_id == current_user.id)

    if month:
        query = query.filter(func.strftime('%Y-%m', Expense.date) == month)

    if category:
        query = query.filter(Expense.category == category)

    expenses = query.order_by(Expense.date.desc()).all()

    return [
        ExpenseResponse(
            id=e.id,
            amount=e.amount,
            category=e.category,
            description=e.description,
            date=e.date,
            payment_method=e.payment_method,
            is_recurring=e.is_recurring,
            created_at=e.created_at
        )
        for e in expenses
    ]


@router.post("/expenses", response_model=ExpenseResponse)
async def create_expense(
    expense_data: ExpenseCreate,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Create a new expense."""
    expense = Expense(
        user_id=current_user.id,
        amount=expense_data.amount,
        category=expense_data.category,
        description=expense_data.description,
        date=expense_data.date,
        payment_method=expense_data.payment_method,
        is_recurring=expense_data.is_recurring
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return ExpenseResponse(
        id=expense.id,
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        date=expense.date,
        payment_method=expense.payment_method,
        is_recurring=expense.is_recurring,
        created_at=expense.created_at
    )


@router.put("/expenses/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Update an expense."""
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    update_data = expense_data.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(expense, key, value)

    db.commit()
    db.refresh(expense)

    return ExpenseResponse(
        id=expense.id,
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        date=expense.date,
        payment_method=expense.payment_method,
        is_recurring=expense.is_recurring,
        created_at=expense.created_at
    )


@router.delete("/expenses/{expense_id}")
async def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Delete an expense."""
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted successfully"}


@router.get("/categories")
async def get_expense_categories():
    """Get list of expense categories."""
    return DEFAULT_CATEGORIES
