import sqlite3
from datetime import datetime
from pathlib import Path

from modelmetre.core.models import InteractionRecord
from modelmetre.storage.repository import UsageRepository


class SQLiteUsageRepository(UsageRepository):
    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path or str(Path.home() / ".modelmetre" / "usage.db")
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _initialize(self) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS usage_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    provider TEXT NOT NULL,
                    model TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    response TEXT NOT NULL,
                    input_tokens INTEGER NOT NULL,
                    output_tokens INTEGER NOT NULL,
                    latency_ms INTEGER NOT NULL,
                    estimated_cost REAL NOT NULL,
                    estimated_energy REAL NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.commit()

    def save(self, record: InteractionRecord) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO usage_events (
                    provider, model, prompt, response, input_tokens, output_tokens,
                    latency_ms, estimated_cost, estimated_energy, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.provider,
                    record.model,
                    record.prompt,
                    record.response,
                    record.input_tokens,
                    record.output_tokens,
                    record.latency_ms,
                    record.estimated_cost,
                    record.estimated_energy,
                    record.created_at.isoformat(),
                ),
            )
            connection.commit()

    def get_all(self) -> list[InteractionRecord]:
        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute(
                "SELECT provider, model, prompt, response, input_tokens, output_tokens, latency_ms, estimated_cost, estimated_energy, created_at FROM usage_events ORDER BY id"
            ).fetchall()

        return [
            InteractionRecord(
                provider=row[0],
                model=row[1],
                prompt=row[2],
                response=row[3],
                input_tokens=row[4],
                output_tokens=row[5],
                latency_ms=row[6],
                estimated_cost=row[7],
                estimated_energy=row[8],
                created_at=datetime.fromisoformat(row[9]),
            )
            for row in rows
        ]

    def get_summary(self) -> dict[str, float | int]:
        with sqlite3.connect(self.db_path) as connection:
            row = connection.execute(
                """
                SELECT
                    COUNT(*) AS total_interactions,
                    COALESCE(SUM(estimated_cost), 0) AS total_cost,
                    COALESCE(SUM(input_tokens + output_tokens), 0) AS total_tokens
                FROM usage_events
                """
            ).fetchone()

        return {
            "total_interactions": int(row[0]),
            "total_cost": round(float(row[1]), 4),
            "total_tokens": int(row[2]),
        }
