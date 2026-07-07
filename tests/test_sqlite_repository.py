from pathlib import Path

from modelmetre.storage.sqlite_repository import SQLiteUsageRepository


def test_sqlite_repository_uses_temp_db_path(tmp_path: Path, make_record) -> None:
    db_path = tmp_path / "usage.db"
    repository = SQLiteUsageRepository(db_path=str(db_path))

    repository.save(make_record(estimated_cost=0.75, input_tokens=4, output_tokens=6))

    rows = repository.get_all()
    summary = repository.get_summary()

    assert db_path.exists()
    assert len(rows) == 1
    assert summary["total_interactions"] == 1
    assert summary["total_cost"] == 0.75
    assert summary["total_tokens"] == 10