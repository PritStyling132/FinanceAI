"""
Database configuration and models using SQLAlchemy.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum
import os

# Database URL - using SQLite for simplicity
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./financial_advisor.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Enums
class RiskToleranceEnum(str, enum.Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


class GoalTypeEnum(str, enum.Enum):
    RETIREMENT = "retirement"
    EDUCATION = "education"
    HOUSE = "house"
    CAR = "car"
    VACATION = "vacation"
    EMERGENCY_FUND = "emergency_fund"
    WEDDING = "wedding"
    OTHER = "other"


class AssetTypeEnum(str, enum.Enum):
    STOCK = "stock"
    MUTUAL_FUND = "mutual_fund"
    ETF = "etf"
    BOND = "bond"
    CRYPTO = "crypto"
    REAL_ESTATE = "real_estate"
    GOLD = "gold"
    CASH = "cash"
    OTHER = "other"


class AlertSeverityEnum(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


# Models
class User(Base):
    """User model for authentication and profile."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Profile fields
    age = Column(Integer, nullable=True)
    annual_income = Column(Float, default=0)
    current_savings = Column(Float, default=0)
    monthly_investment = Column(Float, default=0)
    debt_amount = Column(Float, default=0)
    risk_tolerance = Column(String(20), default="moderate")
    investment_horizon = Column(Integer, default=10)
    goals = Column(JSON, default=list)
    has_emergency_fund = Column(Boolean, default=False)
    has_retirement_account = Column(Boolean, default=False)

    # Relationships
    holdings = relationship("Holding", back_populates="user", cascade="all, delete-orphan")
    financial_goals = relationship("FinancialGoal", back_populates="user", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")
    chat_history = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")
    analytics_events = relationship("AnalyticsEvent", back_populates="user", cascade="all, delete-orphan")


class Holding(Base):
    """Portfolio holdings model."""
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String(20), nullable=False)
    name = Column(String(200), nullable=False)
    asset_type = Column(String(20), default="stock")
    quantity = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=True)
    purchase_date = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="holdings")

    @property
    def current_value(self):
        price = self.current_price or self.purchase_price
        return self.quantity * price

    @property
    def invested_value(self):
        return self.quantity * self.purchase_price

    @property
    def returns(self):
        return self.current_value - self.invested_value

    @property
    def returns_percent(self):
        if self.invested_value == 0:
            return 0
        return (self.returns / self.invested_value) * 100


class FinancialGoal(Base):
    """Financial goals model."""
    __tablename__ = "financial_goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200), nullable=False)
    goal_type = Column(String(30), default="other")
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0)
    monthly_contribution = Column(Float, default=0)
    target_date = Column(DateTime, nullable=False)
    priority = Column(Integer, default=3)  # 1-5
    is_achieved = Column(Boolean, default=False)
    achieved_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="financial_goals")

    @property
    def progress_percent(self):
        if self.target_amount == 0:
            return 0
        return (self.current_amount / self.target_amount) * 100

    @property
    def remaining_amount(self):
        return max(0, self.target_amount - self.current_amount)


class Budget(Base):
    """Monthly budget model."""
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    month = Column(String(7), nullable=False)  # YYYY-MM format
    income = Column(Float, default=0)
    total_budget = Column(Float, default=0)
    category_budgets = Column(JSON, default=dict)  # {"food": 10000, "transport": 5000, ...}
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="budgets")


class Expense(Base):
    """Expense tracking model."""
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(String(500), nullable=True)
    date = Column(DateTime, nullable=False)
    payment_method = Column(String(50), nullable=True)
    is_recurring = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="expenses")


class Alert(Base):
    """User alerts and notifications model."""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(20), default="info")  # info, warning, critical
    alert_type = Column(String(50), nullable=True)  # market, goal, budget, etc.
    is_read = Column(Boolean, default=False)
    action_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="alerts")


class ChatHistory(Base):
    """Chat history for AI advisor."""
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    response_id = Column(String(50), nullable=True)
    feedback_helpful = Column(Boolean, nullable=True)
    feedback_rating = Column(Integer, nullable=True)  # 1-5
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="chat_history")


class AnalyticsEvent(Base):
    """Analytics event tracking."""
    __tablename__ = "analytics_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_type = Column(String(100), nullable=False)
    event_category = Column(String(50), nullable=True)
    event_data = Column(JSON, default=dict)
    page = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="analytics_events")


class Feedback(Base):
    """User feedback model."""
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    feedback_type = Column(String(50), nullable=False)  # chat_response, recommendation, general
    related_id = Column(String(50), nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5
    helpful = Column(Boolean, nullable=True)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create all tables
def init_db():
    Base.metadata.create_all(bind=engine)
