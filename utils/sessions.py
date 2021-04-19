import contextlib
from functools import wraps
from inspect import signature

from models.base import Session

# SqlAlchemy session helpers that can be used as a decorator

@contextlib.contextmanager
def create_session():
    """Contextmanager that will create and teardown a session."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def find_session_idx(func):
    """Find session index in function call parameter."""
    func_params = signature(func).parameters
    try:
        session_args_idx = tuple(func_params).index("session")
    except ValueError:
        raise ValueError(f"Function {func.__qualname__} has no `session` argument") from None

    return session_args_idx


def provide_session(func):
    """
    Function decorator that provides a session if it isn't provided.
    """
    session_args_idx = find_session_idx(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        if "session" in kwargs or session_args_idx < len(args):
            return func(*args, **kwargs)
        else:
            with create_session() as session:
                return func(*args, session=session, **kwargs)

    return wrapper
