from modelmetre.core.models import InteractionRecord
from modelmetre.storage.repository import UsageRepository, get_default_repository


class UsageTracker:
    def __init__(self, repository: UsageRepository | None = None) -> None:
        self.repository = repository or get_default_repository()

    def track(self, record: InteractionRecord) -> None:
        self.repository.save(record)