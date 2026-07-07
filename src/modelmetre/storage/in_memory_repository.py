from modelmetre.core.models import InteractionRecord
from modelmetre.storage.repository import UsageRepository


class InMemoryUsageRepository(UsageRepository):
    def __init__(self) -> None:
        self._records: list[InteractionRecord] = []

    def save(self, record: InteractionRecord) -> None:
        self._records.append(record)

    def get_all(self) -> list[InteractionRecord]:
        return list(self._records)

    def get_summary(self) -> dict[str, float | int]:
        total_interactions = len(self._records)
        total_cost = sum(record.estimated_cost for record in self._records)
        total_tokens = sum(record.input_tokens + record.output_tokens for record in self._records)

        return {
            "total_interactions": total_interactions,
            "total_cost": round(total_cost, 4),
            "total_tokens": total_tokens,
        }
