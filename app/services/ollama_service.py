"""
Ollama integration service for local LLM inference.
Provides chat completions, streaming responses, and health checking.
"""

import json
import os
from typing import List, Dict, Any, Optional, Iterator
import httpx


class OllamaService:
    def __init__(
        self,
        base_url: Optional[str] = None,
        default_model: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")
        self.default_model = default_model or os.getenv("OLLAMA_MODEL", "qwen2.5-coder:3b")
        self.timeout = timeout or float(os.getenv("OLLAMA_TIMEOUT", "65.0"))
        self.num_threads = min(os.cpu_count() or 4, 8)
        # 0 runs cleanly on CPU/RAM, avoiding Vulkan VRAM out-of-memory crashes on long prompts
        self.num_gpu = int(os.getenv("OLLAMA_NUM_GPU", "0"))

    def is_available(self) -> bool:
        """Check if Ollama service is reachable."""
        try:
            with httpx.Client(timeout=3.0) as client:
                res = client.get(f"{self.base_url}/api/tags")
                return res.status_code == 200
        except Exception:
            return False

    def get_available_models(self) -> List[str]:
        """Fetch list of models available in local Ollama."""
        try:
            with httpx.Client(timeout=5.0) as client:
                res = client.get(f"{self.base_url}/api/tags")
                if res.status_code == 200:
                    models = res.json().get("models", [])
                    return [m.get("name") for m in models if m.get("name")]
        except Exception:
            pass
        return []

    def get_best_model(self) -> str:
        """Select configured model or best available model."""
        models = self.get_available_models()
        if self.default_model in models:
            return self.default_model
        # Look for common models
        for preferred in ["qwen2.5-coder:3b", "qwen2.5", "llama3", "mistral"]:
            for m in models:
                if preferred in m:
                    return m
        return models[0] if models else self.default_model

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 250,
    ) -> Optional[str]:
        """
        Send multi-turn chat request and return complete response text.
        Returns None if generation fails or times out so caller can invoke fallback.
        """
        chosen_model = model or self.get_best_model()
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": chosen_model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_thread": self.num_threads,
                "num_gpu": self.num_gpu,
                "num_predict": max_tokens,
                "num_ctx": 2048,
            },
        }

        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.post(url, json=payload)
                if res.status_code != 200:
                    print(f"Ollama HTTP error {res.status_code}: {res.text}")
                    return None

                data = res.json()
                if "error" in data:
                    print(f"Ollama internal error: {data['error']}")
                    return None

                content = data.get("message", {}).get("content", "").strip()
                return content if content else None
        except Exception as e:
            print(f"Ollama chat error/timeout: {e}")
            return None

    def stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 400,
    ) -> Iterator[str]:
        """
        Stream chat response token by token as Server-Sent Events / raw chunks.
        """
        chosen_model = model or self.get_best_model()
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": chosen_model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": temperature,
                "num_thread": self.num_threads,
                "num_gpu": self.num_gpu,
                "num_predict": max_tokens,
                "num_ctx": 2048,
            },
        }

        try:
            stream_timeout = max(self.timeout, 120.0)
            with httpx.Client(timeout=stream_timeout) as client:
                with client.stream("POST", url, json=payload) as response:
                    if response.status_code != 200:
                        yield f"\n[Error: Ollama status {response.status_code}]"
                        return

                    for line in response.iter_lines():
                        if line:
                            try:
                                chunk = json.loads(line)
                                if "error" in chunk:
                                    yield f"\n[Error: {chunk['error']}]"
                                    break
                                content = chunk.get("message", {}).get("content", "")
                                if content:
                                    yield content
                                if chunk.get("done", False):
                                    break
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            yield f"\n[Stream Error: {str(e)}]"


# Global Ollama service singleton
ollama_service = OllamaService()
