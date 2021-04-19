from googleapiclient.discovery import build


def provide_service(func, creds):
    """
    Function decorator that provides a gmail service.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        service = build("gmail", "v1", credentials=creds)
        return func(*args, service=service, **kwargs)

    return wrapper
