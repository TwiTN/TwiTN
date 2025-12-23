import uuid

_sessions: dict[str, str] = {}


def create_session(user_id: str) -> str:
    session_id = str(uuid.uuid4())
    _sessions[session_id] = user_id
    return session_id


def get_user_from_session(session_id: str) -> str | None:
    return _sessions.get(session_id)


def delete_session(session_id: str) -> None:
    _sessions.pop(session_id, None)
