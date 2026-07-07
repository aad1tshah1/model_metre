from datetime import datetime
from decimal import Decimal

from modelmetre.config.config_service import ConfigService
from modelmetre.core.cost_estimator import CostEstimator
from modelmetre.core.models import InteractionRecord, PromptRequest
from modelmetre.core.usage_tracker import UsageTracker
from modelmetre.providers.base import Provider
from modelmetre.providers.factory import ProviderFactory


class PromptService:
    def __init__(
        self,
        provider: Provider | None = None,
        tracker: UsageTracker | None = None,
    ) -> None:
        self.provider = provider
        self.tracker = tracker or UsageTracker()

    def ask(self, request: PromptRequest) -> InteractionRecord:
        config = ConfigService()
        request = config.apply_defaults(request)

        selected_provider = self.provider or ProviderFactory().create(request.provider)
        provider_response = selected_provider.send_prompt(request)

        estimated_cost = CostEstimator().estimate(
            provider=provider_response.provider,
            model=provider_response.model,
            input_tokens=provider_response.input_tokens,
            output_tokens=provider_response.output_tokens,
        )

        record = InteractionRecord(
            provider=provider_response.provider,
            model=provider_response.model,
            prompt=request.prompt,
            response=provider_response.text,
            input_tokens=provider_response.input_tokens,
            output_tokens=provider_response.output_tokens,
            latency_ms=provider_response.latency_ms,
            estimated_cost=estimated_cost,
            estimated_energy=Decimal("0.00"),
            created_at=datetime.now(),
        )

        self.tracker.track(record)
        return record