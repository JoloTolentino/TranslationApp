from server.schemas.ModelSchemaValidator import (
    UsersSchemaValidator,
    SubscriptionsSchemaValidator,
    SignupSchemaValidator,
)
from server.utils.santize import clean_username, clean_email, clean_name
from server.models import USER, SUBSCRIPTIONS, ATTEMPTS,Tiers
from server.config import BAN_INTERVAL
from server.extensions import logger
from server.utils.database import Postgres
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from pprint import pprint
import json
import uuid
import pdb


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    validator = UsersSchemaValidator(data)
    errors = validator.error
    if errors:
        return errors, 400

    raw_password = data.pop("password")
    data["username"] = clean_username(data["username"])
    user_details = USER.query.filter_by(username=data["username"]).first()
    user_uuid = user_details.uuid
    user_attemtps = ATTEMPTS.query.filter_by(uuid=user_uuid)

    if user_details and not user_details.check_password(raw_password):
        response = user_attemtps.increment_attempt()
        return jsonify({**response, "error": "invalid password"}), 400

    if not user_attemtps.check_valid():
        return (
            jsonify(
                {
                    "error": f"{data['username']} is locked out till {user_attemtps.lockout_until}"
                }
            ),
            401,
        )

    user_attemtps.reset_attempts()
    login_user()
    return jsonify({"success": f'{data["username"]} succesfully loggedin'})


@auth.route("/signup", methods=["POST"])
def signup():
    data = json.loads(request.get_json()["body"])

    #generate uuid  per user 
    data["uuid"] = str(uuid.uuid4())


    logger.info(f'Signup for :{data["uuid"]} in progress')
    subscription = data.pop("subscription")

    validator = SignupSchemaValidator(data)

    raw_password = data.pop("password")
    errors = validator.error
    if errors:
        logger.info(errors)
        return jsonify(errors), 400

    # sanitize inputs
    logger.info(f"User Data : {pprint(data)}")

    data["username"] = clean_username(data["username"])
    data["firstname"] = clean_name(data["firstname"])
    data["lastname"] = clean_name(data["lastname"])
    data["email"] = clean_email(data["email"])

    logger.info(f'Processing user :[{data["uuid"]}]')

    # create entries in the db
    new_user = USER(**data)
    new_user.set_password(raw_password)
    new_user_attempts = ATTEMPTS(uuid=data["uuid"])
    new_user_subscription = SUBSCRIPTIONS(uuid=data["uuid"])
    subscription_status = new_user_subscription.subscribe_tier(subscription)

    primary_service = {"USER": new_user}

    secondary_services = {
        "ATTEMPTS": new_user_attempts,
        "SUBSCRIPTIONS": new_user_subscription,
    }

    services = {"primary": primary_service, "secondary": secondary_services}

    response, status_code = Postgres.add_dependent_services(services)
    response["subscription_status"] = subscription_status

    pdb.set_trace()
    return jsonify(response), status_code


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200
