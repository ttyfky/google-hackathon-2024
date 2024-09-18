import os


def base_path():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def resource_path():
    return base_path() + "/resources"


def secret_path():
    return resource_path() + "/secrets"


def temp_path():
    return resource_path() + "/temp"


def local_username() -> str:
    """
    Get the username of the current user.
    """
    return os.environ["LOGNAME"] if "LOGNAME" in os.environ else os.environ["USERNAME"]


def is_local() -> bool:
    """
    Check if the code is running locally.
    """
    return os.environ.get("IS_LOCAL", "false").lower() == "true"


def pubsub_active() -> bool:
    """
    Skip PubSub operations.
    """
    return not is_local() or os.environ.get("PUBSUB_FORCE", "false").lower() == "true"
