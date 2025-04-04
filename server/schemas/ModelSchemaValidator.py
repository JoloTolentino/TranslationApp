from jsonschema import validate, ValidationError
from jsonschema import Draft7Validator
from server.schemas import JsonSchemaValidator
from server.config import CONFIG
from server.schemas.DataSchemaMixin import DataSchemaMixin

"""
    properties:
        valid - checks if the input data is valid
        missing - checks for missing keys provided a 
"""


class SignupSchemaValidator(DataSchemaMixin, JsonSchemaValidator):
    def __init__(self, data) -> None:
        path = CONFIG.SIGNUP_SCHEMA
        super().__init__(path)
        self._valid = self.validate(data)

    def validate(self, data) -> bool:
        validator = Draft7Validator(schema=self.schema)
        errors = list(validator.iter_errors(data))
        self._collect_errors(data, self.schema)
        return False if errors else True


class SubscriptionsSchemaValidator(DataSchemaMixin, JsonSchemaValidator):
    def __init__(self, data) -> None:
        path = CONFIG.SUBSCRIPTION_SCHEMA
        super().__init__(path)
        self._valid = self.validate(data)

    def validate(self, data) -> bool:
        validator = Draft7Validator(schema=self.schema)
        errors = list(validator.iter_errors(data))
        self._collect_errors(data, self.schema)
        return False if errors else True


class UsersSchemaValidator(DataSchemaMixin, JsonSchemaValidator):
    def __init__(self, data) -> None:
        path = CONFIG.USER_SCHEMA
        super().__init__(path)
        self._valid = self.validate(data)

    def validate(self, data) -> bool:
        validator = Draft7Validator(schema=self.schema)
        errors = list(validator.iter_errors(data))
        self._collect_errors(data, self.schema)
        return False if errors else True
