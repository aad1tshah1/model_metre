import os
import time

import httpx

from modelmetre.core.models import PromptRequest
from modelmetre.providers.base import Provider, ProviderResponse


class AnthropicProvider(Provider):
    def __init__(
        self,
        api_key: str,
        default_model: str = "claude-sonnet-4-6",
    ) -> None:
        self.api_key = api_key
        self.default_model = default_model

    def send_prompt(self, request: PromptRequest) -> ProviderResponse:
        model = request.model or self.default_model

        started = time.perf_counter()

        api_version = os.environ.get("ANTHROPIC_API_VERSION", "2023-06-01")

        response = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": api_version,
                "content-type": "application/json",
                "accept": "application/json",
            },
            json={
                "model": model,
                "max_tokens": 512,
                "messages": [
                    {
                        "role": "user",
                        "content": request.prompt,
                    }
                ],
            },
            timeout=60,
        )

        latency_ms = int((time.perf_counter() - started) * 1000)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text
            raise RuntimeError(
                f"Anthropic request failed ({exc.response.status_code}): {detail}"
            ) from exc

        payload = response.json()

        text = "".join(
            block.get("text", "")
            for block in payload.get("content", [])
        )

        usage = payload.get("usage", {})

        return ProviderResponse(
            provider="anthropic",
            model=payload.get("model", model),
            text=text,
            input_tokens=int(usage.get("input_tokens", 0)),
            output_tokens=int(usage.get("output_tokens", 0)),
            latency_ms=latency_ms,
        )