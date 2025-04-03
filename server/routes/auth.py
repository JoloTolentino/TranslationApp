from server.schemas.ModelSchemaValidator import (
    UsersSchemaValidator,
    SubscriptionsSchemaValidator,
    SignupSchemaValidator
)
from server.utils.santize import (
    clean_username,
    clean_email,
    clean_name
)
from server.models import USER,SUBSCRIPTIONS,ATTEMPTS
from server.config import BAN_INTERVAL
from server.extensions import logging
from server.utils.database import Postgres
from flask import Blueprint,request,jsonify
from flask_login import login_user,logout_user,login_required
from pprint import pprint
import uuid
import pdb


auth = Blueprint('auth', __name__)

def get_invalid_keys(validator):
    if not validator.valid:
        payload = {
            'invalid_keys': validator.invalid,
            'missing_keys': validator.missing
        }
        return jsonify(payload)
    return None


@auth.route('/login', methods= ['POST'])
def login():
    data =request.get_json()
    validator = UsersSchemaValidator(data)
    invalid_keys = get_invalid_keys(validator)
    
    if invalid_keys:  
        return invalid_keys,400   

    raw_password = data.pop('password')
    data['username'] = clean_username(data['username'])
    user_details = USER.query.filter_by(username = data['username']).first()
    user_uuid = user_details.uuid
    user_attemtps = ATTEMPTS.query.filter_by(uuid = user_uuid)

    if user_details and not user_details.check_password(raw_password):
        response = user_attemtps.increment_attempt()
        return jsonify({**response, 'error': 'invalid password'}),400

    if not user_attemtps.check_valid():
        return jsonify({'error':f'{data['username']} is locked out till {user_attemtps.lockout_until}'}),401

    user_attemtps.reset_attempts()
    login_user()
    return jsonify({'success': f'{data['username']} succesfully loggedin'})




@auth.route('/signup', methods = ['POST'] )
def signup():
    data = request.get_json()
    validator = SignupSchemaValidator(data) 
    invalid_keys = get_invalid_keys(validator)
    if invalid_keys:  
        return invalid_keys,400   

    #sanitize inputs 
    raw_password = data.pop('password')
    subscription = data.pop('subscription')
    
    #log everything except password and subscription tier
    logging.debug(f'User Data : {pprint(data)}')

    data['username'] = clean_username(data['username'])
    data['firstname'] = clean_name(data['firstname'])
    data['lastname'] = clean_name(data[''])
    data['email'] = clean_email(data['email'])
    data['uuid'] = str(uuid.uuid4()) 

    logging.info(f'Processing user :[{data['uuid']}]')

    #create entries in the db
    new_user = USER(**data)
    new_user.set_password(raw_password)
    new_user_attempts = ATTEMPTS(uuid=data['uuid'])
    new_user_subscription = SUBSCRIPTIONS(uuid=data['uuid'])
    subscription_status = new_user_subscription.subscribe_tier(subscription)
    services = {
        'USER': new_user,
        'ATTEMPTS':new_user_attempts,
        'SUBSCRIPTIONS':new_user_subscription
    }
    response,status_code = Postgres.add_services(services)
    response['subscription_status'] = subscription_status
    return response,status_code



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200