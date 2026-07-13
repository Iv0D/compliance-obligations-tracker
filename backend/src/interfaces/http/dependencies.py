from collections.abc import Iterator

from sqlalchemy.orm import Session

from src.infrastructure.database.session import get_session_factory


def get_session() -> Iterator[Session]:
    session = get_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
