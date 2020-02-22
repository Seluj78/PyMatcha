from functools import wraps

from flask import request
from werkzeug.exceptions import BadRequest

from PyMatcha.errors import BadRequestError


def validate_required_params(required):
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
            for item in required:
                # If a key is missing in the sent data
                if item not in data.keys():
                    missing.append(item)
            if missing:
                raise BadRequestError(
                    "Missing keys {} to create user.".format(missing), "Complete your json body and try again"
                )

            for item in data.keys():
                # If there's an unwanted key in the sent data
                if item not in required:
                    raise BadRequestError(
                        "You can't specify key '{}'.".format(item),
                        "You are only allowed to specify the fields {} " "when creating a user.".format(required),
                    )

            for key, value in data.items():
                if value is None or value == "":
                    raise BadRequestError(f"The item {key} cannot be None or empty", "Please try again.")
            return fn(*args, **kwargs)

        return wrapper

    return decorator
