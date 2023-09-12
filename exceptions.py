class RequiredParameterException(Exception):

    def __init__(self, value):
        if value:
            self.message = "{value} is required"
        else:
            self.message = "A required parameter is missing"

    def __str__(self) -> str:
        return self.message


class DuplicateException(Exception):

    def __init__(self, model_name):
        if model_name:
            self.message = f"{model_name} with these details already exist"
        else:
            self.message = "Data with these details already exist"

    def __str__(self) -> str:
        return self.message


class NotFoundException(Exception):

    def __init__(self, model_name):
        if model_name:
            self.message = f"{model_name} with these details not found"
        else:
            self.message = "Data with these details not found"

    def __str__(self) -> str:
        return self.message


class AuthorizationException(Exception):

    def __init__(self, action_to_perform):
        if action_to_perform:
            self.message = f"Sorry, you are not allowed to {action_to_perform}"
        else:
            self.message = "Sorry, you are not allowed to perform this action"

    def __str__(self) -> str:
        return self.message
