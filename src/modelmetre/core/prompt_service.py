from datetime import datetime

from modelmetre.core.models import PromptRequest, InteractionRecord
from modelmetre.core.usage_tracker import UsageTracker
from modelmetre.storage.repository import get_default_repository


class PromptService:
    def __init__(self, tracker: UsageTracker | None = None) -> None:
        self.tracker = tracker or UsageTracker(repository=get_default_repository())

    def ask(self, request: PromptRequest) -> InteractionRecord:
        record = InteractionRecord(
            provider=request.provider or "anthropic",
            model=request.model or "sonnet",
            prompt=request.prompt,
            response=f"Fake AI response for: {request.prompt}",
            input_tokens=0,
            output_tokens=0,
            latency_ms=0,
            estimated_cost=0.0,
            estimated_energy=0.0,
            created_at=datetime.now(),
        )
        self.tracker.track(record)
        return record