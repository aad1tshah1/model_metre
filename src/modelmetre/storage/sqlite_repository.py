import sqlite3
from datetime import datetime
from decimal import Decimal
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
                    estimated_cost TEXT NOT NULL,
                    estimated_energy TEXT NOT NULL,
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
                    str(record.estimated_cost),
                    str(record.estimated_energy),
                    record.created_at.isoformat(),
                ),
            )
            connection.commit()

    def get_all(self) -> list[InteractionRecord]:
        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute(
                """
                SELECT provider, model, prompt, response, input_tokens,
                       output_tokens, latency_ms, estimated_cost,
                       estimated_energy, created_at
                FROM usage_events
                ORDER BY id
                """
            ).fetchall()

        return [
            InteractionRecord(
                provider=row[0],
                model=row[1],
                prompt=row[2],
                response=row[3],
                input_tokens=int(row[4]),
                output_tokens=int(row[5]),
                latency_ms=int(row[6]),
                estimated_cost=Decimal(str(row[7])),
                estimated_energy=Decimal(str(row[8])),
                created_at=datetime.fromisoformat(row[9]),
            )
            for row in rows
        ]

    def get_summary(self) -> dict[str, Decimal | int]:
        records = self.get_all()

        total_cost = sum(
            (record.estimated_cost for record in records),
            Decimal("0.00"),
        )

        total_tokens = sum(
            record.input_tokens + record.output_tokens
            for record in records
        )

        return {
            "total_interactions": len(records),
            "total_cost": total_cost.quantize(Decimal("0.0001")),
            "total_tokens": total_tokens,
        }