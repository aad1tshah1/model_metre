from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from modelmetre.core.models import InteractionRecord

if TYPE_CHECKING:
    from modelmetre.storage.sqlite_repository import SQLiteUsageRepository


class UsageRepository(ABC):
    @abstractmethod
    def save(self, record: InteractionRecord) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[InteractionRecord]:
        raise NotImplementedError

    @abstractmethod
    def get_summary(self) -> dict[str, float | int]:
        raise NotImplementedError


_DEFAULT_REPOSITORY: UsageRepository | None = None


def get_default_repository() -> UsageRepository:
    global _DEFAULT_REPOSITORY
    if _DEFAULT_REPOSITORY is None:
        from modelmetre.storage.sqlite_repository import SQLiteUsageRepository

        _DEFAULT_REPOSITORY = SQLiteUsageRepository()
    return _DEFAULT_REPOSITORY
