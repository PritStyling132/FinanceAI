import re
from typing import Optional


class Guardrails:
    DISCLAIMER = """
---
**Disclaimer**: This is AI-generated financial guidance for educational purposes only.
It does not constitute professional financial advice, investment recommendations, or
an offer to buy or sell any securities. Past performance does not guarantee future results.
All investments carry risk, including potential loss of principal.
Please consult with a qualified financial advisor before making any investment decisions.
"""

    BLOCKED_TOPICS = [
        "guaranteed returns",
        "get rich quick",
        "insider trading",
        "pump and dump",
        "ponzi",
        "pyramid scheme",
    ]

    SENSITIVE_PATTERNS = [
        r"guarantee.*return",
        r"100%.*safe",
        r"can't lose",
        r"risk.?free.*profit",
        r"double.*money.*fast",
    ]

    def __init__(self):
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.SENSITIVE_PATTERNS]

    def preprocess_query(self, query: str) -> str:
        """Preprocess and validate user query."""
        query = query.strip()

        for topic in self.BLOCKED_TOPICS:
            if topic.lower() in query.lower():
                return f"I cannot provide advice on topics related to '{topic}'. Please ask about legitimate investment strategies and financial planning."

        return query

    def postprocess_response(self, response: str) -> str:
        """Postprocess LLM response to add guardrails."""
        for pattern in self.compiled_patterns:
            if pattern.search(response):
                response = self._add_risk_warning(response)
                break

        if not self._has_disclaimer(response):
            response = response + "\n" + self.DISCLAIMER

        return response

    def _has_disclaimer(self, text: str) -> bool:
        """Check if response already contains a disclaimer."""
        disclaimer_keywords = ["disclaimer", "not financial advice", "consult", "professional advisor"]
        text_lower = text.lower()
        return any(kw in text_lower for kw in disclaimer_keywords)

    def _add_risk_warning(self, response: str) -> str:
        """Add risk warning to response."""
        warning = "\n\n**Important Risk Warning**: All investments carry inherent risks. The statements above should not be interpreted as guarantees of future performance.\n"
        return response + warning

    def get_disclaimer(self) -> str:
        """Get the standard disclaimer text."""
        return self.DISCLAIMER.strip()

    def validate_response(self, response: str) -> dict:
        """Validate response for compliance issues."""
        issues = []

        for pattern in self.compiled_patterns:
            if pattern.search(response):
                issues.append({
                    "type": "risky_language",
                    "pattern": pattern.pattern,
                    "severity": "warning",
                })

        for topic in self.BLOCKED_TOPICS:
            if topic.lower() in response.lower():
                issues.append({
                    "type": "blocked_topic",
                    "topic": topic,
                    "severity": "error",
                })

        return {
            "is_valid": len([i for i in issues if i["severity"] == "error"]) == 0,
            "issues": issues,
        }

    def sanitize_user_input(self, text: str) -> str:
        """Sanitize user input to prevent injection attacks."""
        text = re.sub(r'[<>]', '', text)

        text = text.replace('\x00', '')

        max_length = 5000
        if len(text) > max_length:
            text = text[:max_length]

        return text.strip()

    def format_financial_numbers(self, response: str) -> str:
        """Format large numbers in response for readability."""
        def format_number(match):
            num = float(match.group(1).replace(',', ''))
            if num >= 1_000_000_000:
                return f"${num/1_000_000_000:.2f}B"
            elif num >= 1_000_000:
                return f"${num/1_000_000:.2f}M"
            elif num >= 1_000:
                return f"${num/1_000:.2f}K"
            return match.group(0)

        pattern = r'\$([0-9,]+(?:\.[0-9]+)?)'
        return re.sub(pattern, format_number, response)
