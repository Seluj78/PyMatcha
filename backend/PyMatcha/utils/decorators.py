import os
from functools import wraps
from typing import Optional

from flask import request
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.errors import UnauthorizedError
from werkzeug.exceptions import BadRequest


def validate_params(required: dict, optional: Optional[dict] = None):
    if optional is None:
        optional = {}

    def decorator(fn):
        """Decorator that checks for the required parameters"""

        @wraps(fn)
        def wrapper(*args, **kwargs):
            # If the json body is missing something (`,` for example), throw an error
            try:
                data = request.get_json()
            except BadRequest:
                raise BadRequestError("The Json Body is malformed", "Please check it and try again")

            # If the data dict is empty
            if not data:
                raise BadRequestError("Missing json body.", "Please fill your json body")

            missing = []
            for item in required.keys():
                # If a key is missing in the sent data
                if item not in data.keys():
                    missing.append(item)
            if missing:
                raise BadRequestError("Missing keys {}.".format(missing), "Complete your json body and try again")

            for item in data.keys():
                # If there's an unwanted key in the sent data
                if item not in required.keys() and item not in optional.keys():
                    raise BadRequestError(
                        "You can't specify key '{}'.".format(item),
                        "You are only allowed to specify the fields {}" ".".format(required.keys()),
                    )

            for key, value in data.items():
                if not value:
                    if required[key] == int:
                        pass
                    else:
                        raise BadRequestError(f"The item {key} cannot be None or empty", "Please try again.")

            wrong_types = [r for r in required.keys() if not isinstance(data[r], required[r])]
            wrong_types += [r for r in optional.keys() if r in data and not isinstance(data[r], optional[r])]

            if wrong_types:
                raise BadRequestError(
                    "{} is/are the wrong type.".format(wrong_types),
                    "It/They must be respectively {} and {}".format(required, optional),
                )

            return fn(*args, **kwargs)

        return wrapper

    return decorator


def debug_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("debug-auth-token", None)
        if token:
            if token != os.getenv("DEBUG_AUTH_TOKEN"):
                raise UnauthorizedError("Incorrect debug auth token.", "Try again")
        else:
            raise UnauthorizedError("Missing debug auth token.", "Try again")
        return f(*args, **kwargs)

    return decorated_function
