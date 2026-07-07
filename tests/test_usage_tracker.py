from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from modelmetre.cli.commands.stats import show_stats
from modelmetre.core.models import InteractionRecord
from modelmetre.core.usage_tracker import UsageTracker
from modelmetre.storage.in_memory_repository import InMemoryUsageRepository
from modelmetre.storage.sqlite_repository import SQLiteUsageRepository


def make_record() -> InteractionRecord:
    return InteractionRecord(
        provider="anthropic",
        model="sonnet",
        prompt="Explain BFS",
        response="A response",
        input_tokens=10,
        output_tokens=5,
        latency_ms=120,
        estimated_cost=1.25,
        estimated_energy=0.5,
        created_at=datetime(2024, 1, 1, 12, 0, 0),
    )


def test_usage_tracker_saves_to_repository() -> None:
    repository = InMemoryUsageRepository()
    tracker = UsageTracker(repository=repository)

    tracker.track(make_record())

    assert len(repository.get_all()) == 1


def test_sqlite_repository_persists_and_summarizes(tmp_path: Path) -> None:
    repository = SQLiteUsageRepository(db_path=str(tmp_path / "usage.db"))
    repository.save(make_record())

    rows = repository.get_all()
    summary = repository.get_summary()

    assert len(rows) == 1
    assert summary["total_interactions"] == 1
    assert summary["total_cost"] == 1.25


def test_show_stats_prints_summary(capsys) -> None:
    repository = InMemoryUsageRepository()
    repository.save(make_record())

    show_stats(repository=repository)

    captured = capsys.readouterr()
    assert "Total interactions" in captured.out
    assert "1" in captured.out
