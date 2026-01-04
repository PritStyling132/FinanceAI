import httpx
from typing import Optional, Generator
import json

from app.config import get_settings


class LLMService:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.ollama_base_url
        self.model = self.settings.ollama_model

    def _make_request(self, endpoint: str, payload: dict, stream: bool = False) -> dict:
        """Make a request to Ollama API."""
        url = f"{self.base_url}{endpoint}"
        with httpx.Client(timeout=120.0) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            return response.json()

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Generate a response from the LLM."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        if system_prompt:
            payload["system"] = system_prompt

        response = self._make_request("/api/generate", payload)
        return response.get("response", "")

    def chat(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Chat completion with message history."""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        response = self._make_request("/api/chat", payload)
        return response.get("message", {}).get("content", "")

    def is_available(self) -> bool:
        """Check if Ollama is running and model is available."""
        try:
            url = f"{self.base_url}/api/tags"
            with httpx.Client(timeout=5.0) as client:
                response = client.get(url)
                response.raise_for_status()
                models = response.json().get("models", [])
                return any(m["name"] == self.model or m["name"].startswith(self.model.split(":")[0]) for m in models)
        except Exception:
            return False

    def list_models(self) -> list[str]:
        """List available models in Ollama."""
        try:
            url = f"{self.base_url}/api/tags"
            with httpx.Client(timeout=5.0) as client:
                response = client.get(url)
                response.raise_for_status()
                models = response.json().get("models", [])
                return [m["name"] for m in models]
        except Exception:
            return []
