from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Document:
    id: UUID
    obligation_id: UUID
    filename: str
    mock_url: str
    created_at: datetime | None = None
