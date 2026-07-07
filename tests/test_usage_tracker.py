from modelmetre.core.usage_tracker import UsageTracker
from modelmetre.storage.in_memory_repository import InMemoryUsageRepository


def test_usage_tracker_saves_to_repository(make_record) -> None:
    repository = InMemoryUsageRepository()
    tracker = UsageTracker(repository=repository)

    tracker.track(make_record())

    assert len(repository.get_all()) == 1