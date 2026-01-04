"""
Portfolio management API routes.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from sqlalchemy.orm import Session
from app.database import get_db, User, Holding
from app.routers.auth import get_current_user_from_header
from app.services.alpha_vantage import AlphaVantageService


router = APIRouter(prefix="/api/portfolio", tags=["Portfolio"])

# Initialize Alpha Vantage service
alpha_vantage = AlphaVantageService()


# Pydantic models
class HoldingCreate(BaseModel):
    symbol: str
    name: str
    asset_type: str = "stock"
    quantity: float
    purchase_price: float
    purchase_date: datetime
    notes: Optional[str] = None


class HoldingUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[float] = None
    purchase_price: Optional[float] = None
    current_price: Optional[float] = None
    notes: Optional[str] = None


class HoldingResponse(BaseModel):
    id: int
    symbol: str
    name: str
    asset_type: str
    quantity: float
    purchase_price: float
    current_price: Optional[float]
    current_value: float
    invested_value: float
    returns: float
    returns_percent: float
    purchase_date: datetime


class PortfolioSummary(BaseModel):
    total_value: float
    total_invested: float
    total_returns: float
    total_returns_percent: float
    holdings_count: int
    asset_allocation: dict


@router.get("/holdings", response_model=List[HoldingResponse])
async def get_holdings(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get all holdings for current user."""
    holdings = db.query(Holding).filter(Holding.user_id == current_user.id).all()

    result = []
    for h in holdings:
        current_price = h.current_price or h.purchase_price
        current_value = h.quantity * current_price
        invested_value = h.quantity * h.purchase_price
        returns = current_value - invested_value
        returns_percent = (returns / invested_value * 100) if invested_value > 0 else 0

        result.append(HoldingResponse(
            id=h.id,
            symbol=h.symbol,
            name=h.name,
            asset_type=h.asset_type,
            quantity=h.quantity,
            purchase_price=h.purchase_price,
            current_price=current_price,
            current_value=current_value,
            invested_value=invested_value,
            returns=returns,
            returns_percent=returns_percent,
            purchase_date=h.purchase_date
        ))

    return result


@router.post("/holdings", response_model=HoldingResponse)
async def create_holding(
    holding_data: HoldingCreate,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Create a new holding."""
    # Try to get current price from Alpha Vantage
    current_price = None
    try:
        quote = alpha_vantage.get_stock_quote(holding_data.symbol)
        if quote and "price" in quote:
            current_price = float(quote["price"])
    except Exception:
        pass

    holding = Holding(
        user_id=current_user.id,
        symbol=holding_data.symbol.upper(),
        name=holding_data.name,
        asset_type=holding_data.asset_type,
        quantity=holding_data.quantity,
        purchase_price=holding_data.purchase_price,
        current_price=current_price,
        purchase_date=holding_data.purchase_date,
        notes=holding_data.notes
    )

    db.add(holding)
    db.commit()
    db.refresh(holding)

    current_price = holding.current_price or holding.purchase_price
    current_value = holding.quantity * current_price
    invested_value = holding.quantity * holding.purchase_price
    returns = current_value - invested_value
    returns_percent = (returns / invested_value * 100) if invested_value > 0 else 0

    return HoldingResponse(
        id=holding.id,
        symbol=holding.symbol,
        name=holding.name,
        asset_type=holding.asset_type,
        quantity=holding.quantity,
        purchase_price=holding.purchase_price,
        current_price=current_price,
        current_value=current_value,
        invested_value=invested_value,
        returns=returns,
        returns_percent=returns_percent,
        purchase_date=holding.purchase_date
    )


@router.put("/holdings/{holding_id}", response_model=HoldingResponse)
async def update_holding(
    holding_id: int,
    holding_data: HoldingUpdate,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Update a holding."""
    holding = db.query(Holding).filter(
        Holding.id == holding_id,
        Holding.user_id == current_user.id
    ).first()

    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")

    update_data = holding_data.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(holding, key, value)

    holding.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(holding)

    current_price = holding.current_price or holding.purchase_price
    current_value = holding.quantity * current_price
    invested_value = holding.quantity * holding.purchase_price
    returns = current_value - invested_value
    returns_percent = (returns / invested_value * 100) if invested_value > 0 else 0

    return HoldingResponse(
        id=holding.id,
        symbol=holding.symbol,
        name=holding.name,
        asset_type=holding.asset_type,
        quantity=holding.quantity,
        purchase_price=holding.purchase_price,
        current_price=current_price,
        current_value=current_value,
        invested_value=invested_value,
        returns=returns,
        returns_percent=returns_percent,
        purchase_date=holding.purchase_date
    )


@router.delete("/holdings/{holding_id}")
async def delete_holding(
    holding_id: int,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Delete a holding."""
    holding = db.query(Holding).filter(
        Holding.id == holding_id,
        Holding.user_id == current_user.id
    ).first()

    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")

    db.delete(holding)
    db.commit()

    return {"message": "Holding deleted successfully"}


@router.get("/summary", response_model=PortfolioSummary)
async def get_portfolio_summary(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get portfolio summary with asset allocation."""
    holdings = db.query(Holding).filter(Holding.user_id == current_user.id).all()

    total_value = 0
    total_invested = 0
    asset_allocation = {}

    for h in holdings:
        current_price = h.current_price or h.purchase_price
        current_value = h.quantity * current_price
        invested_value = h.quantity * h.purchase_price

        total_value += current_value
        total_invested += invested_value

        # Group by asset type
        asset_type = h.asset_type.replace("_", " ").title()
        asset_allocation[asset_type] = asset_allocation.get(asset_type, 0) + current_value

    total_returns = total_value - total_invested
    total_returns_percent = (total_returns / total_invested * 100) if total_invested > 0 else 0

    return PortfolioSummary(
        total_value=total_value,
        total_invested=total_invested,
        total_returns=total_returns,
        total_returns_percent=total_returns_percent,
        holdings_count=len(holdings),
        asset_allocation=asset_allocation
    )


@router.post("/refresh-prices")
async def refresh_prices(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Refresh current prices for all holdings."""
    holdings = db.query(Holding).filter(Holding.user_id == current_user.id).all()

    updated_count = 0
    for holding in holdings:
        if holding.asset_type in ["stock", "etf"]:
            try:
                quote = alpha_vantage.get_stock_quote(holding.symbol)
                if quote and "price" in quote:
                    holding.current_price = float(quote["price"])
                    holding.updated_at = datetime.utcnow()
                    updated_count += 1
            except Exception:
                continue

    db.commit()

    return {"message": f"Updated prices for {updated_count} holdings"}
