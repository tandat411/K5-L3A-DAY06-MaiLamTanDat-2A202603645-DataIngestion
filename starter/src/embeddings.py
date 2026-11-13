"""Real embedding provider adapter for OpenRouter and OpenAI-compatible endpoints."""
import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Protocol
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text, in the same order."""
        ...

    def embed_query(self, question: str) -> list[float]:
        """Return a query vector compatible with the stored document vectors."""
        ...


class MyEmbedder:
    """Real embedding provider adapter; does not fallback to mock vectors."""

    def __init__(
        self,
        model_name: str | None = None,
        api_key: str | None = None,
        batch_size: int = 16,
    ) -> None:
        self.model_name = model_name or os.getenv("EMBEDDING_MODEL") or "qwen/qwen3-embedding-8b"
        self.batch_size = max(1, batch_size)

        openrouter_key = api_key or os.getenv("OPENROUTER_API_KEY")
        openai_key = api_key or os.getenv("OPENAI_API_KEY")

        if openrouter_key:
            self.api_key = openrouter_key
            self.endpoint = "https://openrouter.ai/api/v1/embeddings"
            self.provider = "OpenRouter"
        elif openai_key:
            self.api_key = openai_key
            self.endpoint = "https://api.openai.com/v1/embeddings"
            self.provider = "OpenAI"
        else:
            raise ValueError(
                "No API key found. Set OPENROUTER_API_KEY or OPENAI_API_KEY in your .env file."
            )

        # Probe model to verify credentials and discover vector dimensions upfront
        probe_vector = self.embed_query("probe embedding dimensions")
        self.dimensions = len(probe_vector)
        if self.dimensions == 0:
            raise RuntimeError(f"Received empty embedding vector from model {self.model_name}")

    def _call_api(self, input_texts: list[str]) -> list[list[float]]:
        # Avoid empty strings causing API errors
        sanitized = [t if t.strip() else " " for t in input_texts]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "HTTP-Referer": "https://github.com/ai-action-lab",
            "X-Title": "AI Action Lab",
        }
        payload = json.dumps({"model": self.model_name, "input": sanitized}).encode("utf-8")
        req = urllib.request.Request(self.endpoint, data=payload, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"Embedding API error ({self.provider} - HTTP {e.code}): {err_body}"
            ) from e
        except Exception as e:
            raise RuntimeError(f"Embedding request failed: {e}") from e

        if "data" not in data:
            raise RuntimeError(f"Unexpected response format from embedding API: {data}")

        # Ensure order matches inputs
        sorted_items = sorted(data["data"], key=lambda x: x["index"])
        embeddings = [item["embedding"] for item in sorted_items]

        if len(embeddings) != len(input_texts):
            raise RuntimeError(
                f"Expected {len(input_texts)} embeddings, but received {len(embeddings)}"
            )

        return embeddings

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text, in the same order, using batching."""
        if not texts:
            return []

        results: list[list[float]] = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            batch_embeddings = self._call_api(batch)
            results.extend(batch_embeddings)

        return results

    def embed_query(self, question: str) -> list[float]:
        """Return a query vector compatible with the stored document vectors."""
        clean_q = question.strip() or " "
        embeddings = self._call_api([clean_q])
        return embeddings[0]
