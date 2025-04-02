
from server.extensions import logging,db
from server.models import ATTEMPTS,SUBSCRIPTIONS,USER
from typing import Dict,Union
from flask_sqlalchemy.model import Model
from sqlalchemy.exc import IntegrityError

class Postgres:
    @staticmethod
    def add_services(self, services: Dict[str, Model]) -> dict:
        try:
            for service in services:
                db.session.add(service)
            db.session.commit()
            return {"message": "Records committed successfully"}, 201
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"[DB] IntegrityError: {e}")
            return {"error": "Unique constraint violation"}, 409
        except Exception as e:
            db.session.rollback()
            logging.error(f"[DB] Unexpected error: {e}")
            return {"error": "Unexpected server error"}, 500

