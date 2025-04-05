from flask import jsonify
from jsonschema import Draft7Validator, ValidationError, FormatChecker
import pdb


class DataSchemaMixin:
    @property
    def valid(self) -> bool:
        return getattr(self, "_valid", False)

    @property
    def error(self):
        return getattr(self, "_error") if self._error['invalid_keys'] and self.error['missing_keys'] else None

    @property
    def missing(self) -> list[str] | list[None]:
        return getattr(self, "_missing", []) 

    @property
    def invalid(self) -> list[str] | dict[None]:
        return getattr(self, "_invalid",{}) 

    @valid.setter
    def valid(self, val: bool) -> None:
        self._valid = val

    @error.setter
    def error(self, val: dict[str, list]) -> None:
        self._error = val

    def get_invalid_keys(self):
        if not self.valid:
            payload = {"invalid_keys": self.invalid, "missing_keys": self.missing}
            return jsonify(payload)
        return None

    def _collect_errors(self, data: dict, schema: dict):
        validator = Draft7Validator(schema, format_checker=FormatChecker())
        errors = list(validator.iter_errors(data))

        self._missing = []
        self._invalid = {}

        _path_delim = "/"

        for error in errors:
            if error.validator in ("type", "format"):
                self._invalid["Invalid Format"] = self._invalid.get(
                    "Invalid Format", []
                )
                full_path = _path_delim.join(str(p) for p in error.path)
                self._invalid["Invalid Format"].append({full_path: error.message})

            elif error.validator == "required":
                for missing_key in error.message.split("'")[1::2]:
                    full_path = ".".join([*map(str, error.path), missing_key])
                    self._missing.append(full_path)

            elif error.validator == "additionalProperties":
                full_path = "/".join(str(p) for p in error.path)
                additional_key = error.message.split("'")[1]  # fallback if no .params
                key = f"{full_path}/{additional_key}" if full_path else additional_key
                self._invalid["Additional Keys"] = self._invalid.get(
                    "Additional Keys", []
                )
                self._invalid["Additional Keys"].append({key: additional_key})

        self.error = self.get_invalid_keys().get_json()

