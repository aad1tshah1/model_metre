from datetime import datetime

from modelmetre.core.models import InteractionRecord, PromptRequest
from modelmetre.core.usage_tracker import UsageTracker
from modelmetre.providers.base import Provider
from modelmetre.providers.fake import FakeProvider


class PromptService:
    def __init__(
        self,
        provider: Provider | None = None,
        tracker: UsageTracker | None = None,
    ) -> None:
        self.provider = provider or FakeProvider()
        self.tracker = tracker or UsageTracker()

    def ask(self, request: PromptRequest) -> InteractionRecord:
        provider_response = self.provider.send_prompt(request)

        record = InteractionRecord(
            provider=provider_response.provider,
            model=provider_response.model,
            prompt=request.prompt,
            response=provider_response.text,
            input_tokens=provider_response.input_tokens,
            output_tokens=provider_response.output_tokens,
            latency_ms=provider_response.latency_ms,
            estimated_cost=0.0,
            estimated_energy=0.0,
            created_at=datetime.now(),
        )

        self.tracker.track(record)
        return record