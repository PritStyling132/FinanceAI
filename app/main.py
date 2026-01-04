"""
AI Financial Advisor - Main FastAPI Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.models.user_profile import (
    UserProfile,
    ChatRequest,
    ChatResponse,
    MarketDataRequest,
    HealthResponse,
)
from app.services.financial_advisor import FinancialAdvisor
from app.services.rag_pipeline import RAGPipeline
from app.services.alpha_vantage import AlphaVantageService
from app.database import init_db

# Import routers
from app.routers import auth, portfolio, goals, budget, alerts, analytics, recommendations, chat


rag_pipeline: RAGPipeline = None
financial_advisor: FinancialAdvisor = None
alpha_vantage: AlphaVantageService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_pipeline, financial_advisor, alpha_vantage

    print("Initializing Financial Advisor services...")

    # Initialize database
    print("Initializing database...")
    init_db()
    print("Database initialized!")

    # Initialize AI services
    rag_pipeline = RAGPipeline()
    financial_advisor = FinancialAdvisor()
    alpha_vantage = AlphaVantageService()

    try:
        status = rag_pipeline.is_ready()
        if not status["vector_store_ready"]:
            print("Initializing knowledge base...")
            try:
                count = rag_pipeline.initialize_knowledge_base()
                print(f"Knowledge base initialized with {count} documents")
            except Exception as e:
                print(f"Warning: Could not initialize knowledge base: {e}")
                print("Make sure Qdrant is running: docker-compose up -d")

        if not status["llm_ready"]:
            print("Warning: Ollama LLM not available. Make sure Ollama is running with llama3.2:3b model")
    except Exception as e:
        print(f"Warning: Could not check system status: {e}")
        print("Some features may not work. Make sure Qdrant is running: docker-compose up -d")

    print("Financial Advisor ready!")
    yield

    print("Shutting down Financial Advisor...")


app = FastAPI(
    title="AI Financial Advisor",
    description="Personalized AI-powered financial advisory service using RAG and LLM",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(portfolio.router)
app.include_router(goals.router)
app.include_router(budget.router)
app.include_router(alerts.router)
app.include_router(analytics.router)
app.include_router(recommendations.router)
app.include_router(chat.router)


# Health check endpoint
@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Check system health and component status."""
    try:
        status = rag_pipeline.is_ready() if rag_pipeline else {
            "all_ready": False,
            "llm_ready": False,
            "vector_store_ready": False,
            "knowledge_base_documents": 0
        }
        return HealthResponse(
            status="healthy" if status["all_ready"] else "degraded",
            llm_ready=status["llm_ready"],
            vector_store_ready=status["vector_store_ready"],
            knowledge_base_documents=status["knowledge_base_documents"],
        )
    except Exception:
        return HealthResponse(
            status="degraded",
            llm_ready=False,
            vector_store_ready=False,
            knowledge_base_documents=0,
        )


# Legacy endpoints for backward compatibility
@app.post("/api/legacy/chat", response_model=ChatResponse)
async def legacy_chat(request: ChatRequest):
    """Legacy chat endpoint - Chat with the financial advisor."""
    try:
        chat_history = None
        if request.chat_history:
            chat_history = [{"role": m.role, "content": m.content} for m in request.chat_history]

        result = financial_advisor.answer_question(
            question=request.message,
            user_profile=request.user_profile,
            chat_history=chat_history,
        )

        return ChatResponse(
            response=result["response"],
            user_profile=request.user_profile,
            market_data_used=request.include_market_data,
            disclaimer=result["disclaimer"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/profile/analyze")
async def analyze_profile(profile: UserProfile):
    """Analyze user profile and get portfolio recommendation."""
    try:
        recommendation = financial_advisor.get_portfolio_recommendation(profile)
        return recommendation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/profile/goal-plan")
async def create_goal_plan(profile: UserProfile):
    """Create a goal-based financial plan."""
    try:
        plan = financial_advisor.get_goal_based_plan(profile)
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/market/{symbol}")
async def get_market_data(symbol: str):
    """Get market data for a stock symbol."""
    try:
        quote = alpha_vantage.get_stock_quote(symbol.upper())
        if not quote:
            raise HTTPException(status_code=404, detail=f"Could not fetch data for {symbol}")

        overview = alpha_vantage.get_company_overview(symbol.upper())
        news = alpha_vantage.get_news_sentiment(tickers=symbol.upper())

        return {
            "symbol": symbol.upper(),
            "quote": quote,
            "overview": overview,
            "news": news,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/market/analyze")
async def analyze_investment(request: MarketDataRequest, profile: UserProfile = None):
    """Analyze a stock for investment suitability."""
    try:
        analysis = financial_advisor.analyze_investment(
            symbol=request.symbol.upper(),
            user_profile=profile,
        )
        if "error" in analysis:
            raise HTTPException(status_code=404, detail=analysis["error"])
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/initialize")
async def initialize_knowledge_base():
    """Initialize or reset the knowledge base."""
    try:
        count = rag_pipeline.initialize_knowledge_base()
        return {"message": f"Knowledge base initialized with {count} documents"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
