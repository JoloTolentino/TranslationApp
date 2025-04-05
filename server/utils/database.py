from server.extensions import logging, db
from server.models import ATTEMPTS, SUBSCRIPTIONS, USER
from typing import Dict, Union
from flask_sqlalchemy.model import Model
from sqlalchemy.exc import IntegrityError
from pprint import pprint
import pdb


class Postgres:
    """
    Postgress Service to serve the entire flask project
    """

    @staticmethod
    def check_values(service: Model) -> dict:
        """
        Debugging purposes, shows row values of entry being inserted

        parameters:
            service - is a row about to be inserted

        """
        values = {}
        for col in service.__tablename__.columns:
            values[col.name] = getattr(service, col.name)

        pprint(values)

    @staticmethod
    def add_services(services: dict[str, Model]) -> dict:
        """

        All Tables are independent of each other, however all tables must be created the same time.

        parameters:
            services - must be independent tables

        """
        try:
            for name, service in services.items():
                print(f"Adding service: {name} → {service.as_dict()}")
                db.session.add(service)

            print("Attempting to commit all services...")
            db.session.commit()
            print("Commit successful.")

            return {"message": "Records committed successfully"}, 201
        except IntegrityError as e:
            db.session.rollback()
            print("FAILED service values:")
            for name, service in services.items():
                print(f"{name}: {service.as_dict()}")
            logging.error(f"[DB] IntegrityError: {e}")
            return {"error": "Database constraint violation"}, 409
        except Exception as e:
            db.session.rollback()
            logging.error(f"[DB] Unexpected error: {e}")
            return {"error": "Unexpected server error"}, 500

    @staticmethod
    def add_dependent_services(services: dict[str, dict[str, Model]]) -> dict:
        """

        Preserves atomicity of dependent tables

        parameters:
            services - has dependency heirarchy, primary and secondary

        """
        try:
            for name, service in services["primary"].items():
                print(f"Adding primary service: {name} → {service.as_dict()}")
                db.session.add(service)

            db.session.flush()

            for name, service in services["secondary"].items():
                print(f"Adding dependent service: {name} → {service.as_dict()}")
                db.session.add(service)

            print("Attempting to commit all services...")
            db.session.commit()
            print("Commit successful.")

            return {"message": "Records committed successfully"}, 201
        except IntegrityError as e:
            db.session.rollback()
            print("FAILED service values:")
            for name, service in services.items():
                print(f"{name}: {service.as_dict()}")
            logging.error(f"[DB] IntegrityError: {e}")
            return {"error": "Database constraint violation"}, 409
        except Exception as e:
            db.session.rollback()
            logging.error(f"[DB] Unexpected error: {e}")
            return {"error": "Unexpected server error"}, 500
