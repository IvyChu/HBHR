from datetime import datetime
from random import randrange

from flask import current_app
from hbhr import db, login_manager, bcrypt
from flask_login import UserMixin
from re import sub


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(60), nullable=False, default=f'default{randrange(10)}.jpg')
    password = db.Column(db.String(60), nullable=False)
    display_name = db.Column(db.String(50), unique=False, nullable=True)
    notes = db.Column(db.String(160), unique=False, nullable=True)
    location = db.Column(db.String(30), unique=False, nullable=True)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # things specifically belonging to this user:
    # posts = db.relationship('Post', backref='author', lazy=True)
    # imgs = db.relationship('Picture', backref='author', lazy=True)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def set_username(self, username):
        self.username = sub('[^A-Za-z0-9_-]+', '', username)

    # def get_reset_token(self, expires_sec=1800):
    #     s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    #     return s.dumps({'user_id': self.id}).decode('utf-8')         

    # @staticmethod
    # def verify_reset_token(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         user_id = s.loads(token)['user_id']
    #     except:
    #         return None
    #     return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.display_name}')"

