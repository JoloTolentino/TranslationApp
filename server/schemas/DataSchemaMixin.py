from jsonschema import Draft7Validator

class DataSchemaMixin:
    @property
    def valid(self) -> bool:
        return getattr(self, '_valid', False)
    
    @property
    def error(self):
        return getattr(self, '_error')
    
    @property
    def missing(self) ->list[str] | list[None] :
        return getattr(self,'_missing',[])

    @property
    def invalid(self) -> list[str] | list[None]:
        return getattr(self,'_invalid',[])


    @valid.setter
    def valid(self, val: bool) -> None:
        self._valid = val


    def _collect_errors(self, data: dict, schema: dict):
        
        validator = Draft7Validator(schema)
        errors = list(validator.iter_errors(data))

        self._missing = []
        self._invalid = []

        for error in errors:
            if error.validator == "required":
                for missing_key in error.message.split("'")[1::2]:
                    full_path = ".".join([*error.path, missing_key])
                    self._missing.append(full_path)

            elif error.validator == "additionalProperties":
                full_path = ".".join(str(p) for p in error.path)
                additional_key = error.message.split("'")[1]
                self._invalid.append(f"{full_path}.{additional_key}" 
                                    if full_path else additional_key)
    

    
       