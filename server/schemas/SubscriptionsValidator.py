from server.config import CONFIG
from server.schemas import JsonSchemaValidator
from jsonschema import validate, ValidationError


class SubscriptionsValidator(JsonSchemaValidator):
    def __init__(self, data) -> None:
        path = CONFIG.SUBSCRIPTION_SCHEMA
        super().__init__(path)
        self.input = data
        self._valid = self._validate()

    def _validate(self) -> bool:
        try:
            validate(instance=self.input, schema=self.schema)
            return True
        except ValidationError as e:
            self._error = e.message
            return False

    @property
    def valid(self) -> bool:
        return self._valid

    @property
    def error(self) -> str:
        return getattr(self, '_error', None)