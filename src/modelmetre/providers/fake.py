from modelmetre.core.models import PromptRequest
from modelmetre.providers.base import Provider, ProviderResponse


class FakeProvider(Provider):
    def send_prompt(self, request: PromptRequest) -> ProviderResponse:
        return ProviderResponse(
            provider=request.provider or "fake",
            model=request.model or "fake-model",
            text=f"Fake AI response for: {request.prompt}",
            input_tokens=0,
            output_tokens=0,
            latency_ms=0,
        )