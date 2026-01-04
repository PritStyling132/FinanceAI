from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class RiskTolerance(str, Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


class UserGoal(str, Enum):
    RETIREMENT = "retirement"
    EMERGENCY_FUND = "emergency_fund"
    HOME_PURCHASE = "home_purchase"
    EDUCATION = "education"
    WEALTH_BUILDING = "wealth_building"
    DEBT_PAYOFF = "debt_payoff"
    TRAVEL = "travel"
    OTHER = "other"


class UserProfile(BaseModel):
    user_id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=18, le=120)
    annual_income: float = Field(..., ge=0)
    current_savings: float = Field(default=0, ge=0)
    monthly_investment: float = Field(default=0, ge=0)
    debt_amount: float = Field(default=0, ge=0)
    risk_tolerance: RiskTolerance = RiskTolerance.MODERATE
    investment_horizon: int = Field(default=10, ge=1, le=50, description="Investment horizon in years")
    goals: list[UserGoal] = Field(default=[UserGoal.WEALTH_BUILDING])
    has_emergency_fund: bool = False
    has_retirement_account: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def get_risk_score(self) -> int:
        """Calculate a risk score from 1-10 based on profile."""
        score = 5

        if self.age < 30:
            score += 2
        elif self.age < 40:
            score += 1
        elif self.age > 55:
            score -= 2
        elif self.age > 45:
            score -= 1

        if self.risk_tolerance == RiskTolerance.CONSERVATIVE:
            score -= 2
        elif self.risk_tolerance == RiskTolerance.AGGRESSIVE:
            score += 2

        if self.investment_horizon > 15:
            score += 1
        elif self.investment_horizon < 5:
            score -= 2

        if not self.has_emergency_fund:
            score -= 1

        debt_ratio = self.debt_amount / max(self.annual_income, 1)
        if debt_ratio > 0.5:
            score -= 2
        elif debt_ratio > 0.3:
            score -= 1

        return max(1, min(10, score))

    def get_recommended_allocation(self) -> dict:
        """Get recommended asset allocation based on profile."""
        risk_score = self.get_risk_score()

        if risk_score <= 3:
            return {
                "stocks": 30,
                "bonds": 50,
                "cash": 15,
                "alternatives": 5,
                "profile": "Conservative",
            }
        elif risk_score <= 5:
            return {
                "stocks": 50,
                "bonds": 35,
                "cash": 10,
                "alternatives": 5,
                "profile": "Moderate-Conservative",
            }
        elif risk_score <= 7:
            return {
                "stocks": 65,
                "bonds": 25,
                "cash": 5,
                "alternatives": 5,
                "profile": "Moderate",
            }
        elif risk_score <= 8:
            return {
                "stocks": 75,
                "bonds": 15,
                "cash": 5,
                "alternatives": 5,
                "profile": "Moderate-Aggressive",
            }
        else:
            return {
                "stocks": 85,
                "bonds": 10,
                "cash": 0,
                "alternatives": 5,
                "profile": "Aggressive",
            }


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str


class ChatRequest(BaseModel):
    message: str
    user_profile: Optional[UserProfile] = None
    chat_history: Optional[list[ChatMessage]] = None
    include_market_data: bool = True


class ChatResponse(BaseModel):
    response: str
    user_profile: Optional[UserProfile] = None
    market_data_used: bool = False
    disclaimer: str = "This is AI-generated financial guidance for educational purposes only. Always consult with a qualified financial advisor before making investment decisions."


class MarketDataRequest(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=10)


class HealthResponse(BaseModel):
    status: str
    llm_ready: bool
    vector_store_ready: bool
    knowledge_base_documents: int
