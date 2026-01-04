from typing import Optional
import re

from app.services.vector_store import VectorStoreService
from app.services.llm_service import LLMService
from app.services.alpha_vantage import AlphaVantageService
from app.models.user_profile import UserProfile


class RAGPipeline:
    SYSTEM_PROMPT = """You are an AI-powered Financial Advisor assistant. Your role is to provide
personalized, data-driven financial guidance based on the user's profile, goals, and current market conditions.

Guidelines:
1. Always consider the user's risk tolerance, age, income, and financial goals when giving advice
2. Use the provided market data and knowledge base to support your recommendations
3. Be specific and actionable in your advice
4. Explain the reasoning behind your recommendations
5. Include relevant disclaimers about investment risks
6. Never guarantee returns or make promises about market performance
7. If you don't have enough information, ask clarifying questions

Remember: You are an educational tool, not a licensed financial advisor. Always recommend
consulting with qualified professionals for major financial decisions."""

    def __init__(self):
        self.vector_store = VectorStoreService()
        self.llm = LLMService()
        self.alpha_vantage = AlphaVantageService()

    def _extract_stock_symbols(self, text: str) -> list[str]:
        """Extract potential stock symbols from text."""
        pattern = r'\b([A-Z]{1,5})\b'
        common_words = {'I', 'A', 'THE', 'AND', 'OR', 'FOR', 'TO', 'IN', 'OF', 'IS', 'IT', 'ON', 'AT', 'BY', 'AN', 'IF', 'SO', 'MY', 'UP', 'DO', 'GO', 'NO', 'BE', 'AS', 'WE', 'US', 'AM', 'PM', 'VS', 'ETF', 'IRA', 'USD', 'RSI', 'SMA', 'EMA'}
        matches = re.findall(pattern, text)
        symbols = [m for m in matches if m not in common_words and len(m) >= 2]
        return list(set(symbols))[:3]

    def _build_context(
        self,
        query: str,
        user_profile: Optional[UserProfile] = None,
        include_market_data: bool = True,
    ) -> str:
        """Build context for the prompt using RAG."""
        context_parts = []

        if user_profile:
            profile_context = f"""User Profile:
- Age: {user_profile.age}
- Annual Income: ${user_profile.annual_income:,}
- Risk Tolerance: {user_profile.risk_tolerance.value}
- Investment Horizon: {user_profile.investment_horizon} years
- Financial Goals: {', '.join(g.value for g in user_profile.goals)}
- Current Savings: ${user_profile.current_savings:,}
- Monthly Investment Capacity: ${user_profile.monthly_investment:,}"""
            context_parts.append(profile_context)

        retrieved_docs = self.vector_store.search(query, top_k=3, score_threshold=0.3)
        if retrieved_docs:
            knowledge_context = "Relevant Financial Knowledge:\n"
            for doc in retrieved_docs:
                knowledge_context += f"\n{doc['content']}\n"
            context_parts.append(knowledge_context)

        if include_market_data:
            symbols = self._extract_stock_symbols(query)
            for symbol in symbols:
                market_context = self.alpha_vantage.format_market_context(symbol)
                if market_context and "Unable to fetch" not in market_context:
                    context_parts.append(market_context)

        return "\n\n---\n\n".join(context_parts)

    def generate_response(
        self,
        query: str,
        user_profile: Optional[UserProfile] = None,
        chat_history: Optional[list[dict]] = None,
        include_market_data: bool = True,
    ) -> str:
        """Generate a response using RAG pipeline."""
        context = self._build_context(query, user_profile, include_market_data)

        if context:
            augmented_query = f"""Context Information:
{context}

---

User Question: {query}

Please provide a helpful, personalized response based on the context above."""
        else:
            augmented_query = query

        if chat_history:
            messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
            for msg in chat_history[-6:]:
                messages.append(msg)
            messages.append({"role": "user", "content": augmented_query})
            response = self.llm.chat(messages)
        else:
            response = self.llm.generate(
                prompt=augmented_query,
                system_prompt=self.SYSTEM_PROMPT,
            )

        return response

    def initialize_knowledge_base(self) -> int:
        """Initialize the vector store with financial knowledge."""
        return self.vector_store.initialize_knowledge_base()

    def is_ready(self) -> dict:
        """Check if all components are ready."""
        try:
            llm_ready = self.llm.is_available()
        except Exception:
            llm_ready = False

        try:
            vector_store_ready = self.vector_store.collection_exists()
            collection_info = self.vector_store.get_collection_info()
            knowledge_base_documents = collection_info.get("points_count", 0) if collection_info else 0
        except Exception:
            vector_store_ready = False
            knowledge_base_documents = 0

        return {
            "llm_ready": llm_ready,
            "vector_store_ready": vector_store_ready,
            "knowledge_base_documents": knowledge_base_documents,
            "all_ready": llm_ready and vector_store_ready,
        }
