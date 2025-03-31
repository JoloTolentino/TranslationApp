from flask_login import UserMixin
from datetime import datetime
from server.extensions import db
from server.config import DATE_FMT
from werkzeug.security import generate_password_hash,check_password_hash



class USER(UserMixin,db.Model):

    __tablename__= 'users'
    uuid  = db.Column(db.String(50), primary_key = True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    is_online = db.Column(db.Boolean, nullable = False, default=False)
    last_login  = db.Column(db.String(20), default = None )

    def set_password(self,raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_last_login(self):
        self.last_login = datetime.now().isoformat()

    def __repr__(self):
        return f'User : {self.username}'        


class BANNED_USERS(db.Model):
    __tablename__ = 'banned_users'
    id = db.Column(db.Integer, primary_key= True)
    uuid = db.Column(db.String(50), db.ForeignKey('users.uuid'))
    reason = db.Column(db.String(250), nullable=True)
    banned_at = db.Column(db.String(50), 
                          default=datetime.strftime(datetime.today(),DATE_FMT))

    def __repr__(self):
        return f'Banned User: {self.uuid}'
