
from flask import Blueprint,request,jsonify
from flask_login import login_user,logout_user,login_required
from server.models import USER,SUBSCRIPTIONS,ATTEMPTS
from server.config import BAN_INTERVAL
from server.schemas import UsersValidator
import uuid
import pdb




auth = Blueprint('auth', __name__)

def check_missing_credentials(credentials: list[str]) -> bool:
    return not all(credentials)

@auth.route('/login', methods= ['POST'])
def login():
    if request.method != 'POST':
        return jsonify({'error': 'Method Not Allowed. Use POST instead.'}), 405

    data =request.get_json()
    validator = UsersValidator(data)









    user = data.get('username')
    raw_password = data.get('password')
    credentials = [user,raw_password]

    if check_missing_credentials(credentials):
        return jsonify({'error': 'Incomplete credentials'}),400
    
    user_details = USER.query.filter_by(username = user).first()

    if not user_details:
        return jsonify({'error': 'Invalid username and password'}),400
    
    user_uuid = user_details.uuid
    user_attemtps = ATTEMPTS.query.filter_by(uuid = user_uuid)

    if user_details and not user_details.check_password(raw_password):
        response = user_attemtps.increment_attempt()
        return jsonify({**response, 'error': 'invalid password'}),400

    user_attemtps.reset_attempts()


    return jsonify({'success': f'{user} succesfully loggedin'})



@auth.route('/test', methods = ['GET'])
def test():
    return 'test'




@auth.route('/signup', methods = ['POST'] )
def signup():
    data = request.get_json()
    validator = UsersValidator(data)

    pdb.set_trace()


    uuid = str(uuid.uuid4()) 








    


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200