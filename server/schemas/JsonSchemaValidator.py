import json 
from abc import ABC,abstractmethod
from jsonschema.validators import validator_for
from jsonschema.exceptions import SchemaError
from server.extensions import logger


class JsonSchemaValidator(ABC):
    def __init__(self, path) -> None:
        self._path = path
        self.schema = path 

    @property
    def schema(self) -> dict:
        return self._data

    @schema.setter
    def schema(self, path: str) -> None:
        try:
            with open(path, 'r') as f:
                data = json.load(f)

            validator = validator_for(data)
            validator.check_schema(data)

            self._data = data
            self._path = path  

        except FileNotFoundError:
            filename = path.split('/')[-1]
            directory = '/'.join(path.split('/')[:-1])
            logger.error(f'{filename} not found at {directory}')
        
        except json.JSONDecodeError:
            logger.error(f'{path} is not a valid JSON file')

        except SchemaError:
            logger.error(f'{path} is a valid JSON file but not a valid JSON Schema')

            raise SchemaError
        except Exception as e:
            logger.error(f"Unexpected error: {e}")


    @schema.deleter
    def schema(self):
        logger.info(f"Deleting schema loaded from {self._path}")
        self._data = None

    @abstractmethod
    def validate(self):
        pass

