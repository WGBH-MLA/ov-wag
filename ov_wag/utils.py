from os import environ as env


def environ_bool(name, default=False):
    """Get a boolean environment variable.

    Valid values are 'true', '1', or 'yes' (case-insensitive).
    """
    return env.get(name, str(default)).lower() in ('true', '1', 'yes')
