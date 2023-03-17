from datetime import datetime
from random import randrange

# from flask import current_app
from hbhr import db
from flask_security import UserMixin, RoleMixin
from re import sub
from hbhr.utils import slugify



class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(60), nullable=False, default=f'default{randrange(10)}.jpg')
    password = db.Column(db.String(60), nullable=False)
    display_name = db.Column(db.String(50), unique=False, nullable=True, default='Anonymous')
    notes = db.Column(db.String(160), unique=False, nullable=True)
    location = db.Column(db.String(30), unique=False, nullable=True)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('users', lazy='dynamic'))

    # things specifically belonging to this user:
    # posts = db.relationship('Post', backref='author', lazy=True)
    # images = db.relationship('Image', backref='user', lazy=True)
    # businesses = db.relationship('Business', back_populates='owner')


    def set_username(self, username):
        self.username = sub('[^A-Za-z0-9_-]+', '', username)

    def is_owner(self, business_id):
        business_user = BusinessUser.query.filter((BusinessUser.business_id == business_id) & (BusinessUser.user_id == self.id)).first()
        if business_user and business_user.role == Business.OWNER:
            return True
        return False


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.display_name}')"

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    permissions = db.Column(db.UnicodeText)

class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255))


service_business = db.Table('service_business',
                            db.Column('service_id', db.Integer,
                                      db.ForeignKey('service.id')),
                            db.Column('business_id', db.Integer,
                                      db.ForeignKey('business.id'))
                            )

class BusinessUser(db.Model):
    __tablename__ = 'business_user'
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role = db.Column(db.String(50))

class Business(db.Model):
    __tablename__ = 'business'
    id = db.Column(db.Integer(), primary_key=True)

    # business role constants
    OWNER = 'owner'
    EMPLOYEE = 'employee'
    PARTNER = 'partner'

    name = db.Column(db.String(255))

    description = db.Column(db.Text)
    email = db.Column(db.String(120), unique=True, nullable=False)
    webpage = db.Column(db.String(255))
    image_file = db.Column(db.String(60), nullable=False, default=f'default{randrange(10)}.jpg')

    url = db.Column(db.String(60), unique=True, nullable=False)

    # URL needs to be unique, but the user may want to 
    def set_url(self, value):
        # make it URL friendly
        value = slugify(value)
        url = value[0:60]

        # check if it already exists for another business
        business = Business.query.filter_by(url=url).first()
        while business and business.id != self.id:
            url = value[0:55] + "-" + str(randrange(1000))
            business = Business.query.filter_by(url=url).first()
        self.url = url


    # To be verified by an admin or mod... Maybe later?
    # verified = db.Column(db.Boolean(), default=False)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_edit = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Users who work for this business (employees, partners, owners)
    members = db.relationship('User', secondary='business_user', backref='businesses')
    business_users = db.relationship('BusinessUser', backref='business', overlaps="businesses,members")

    def add_member(self, user, role):
        business_user = BusinessUser(business_id=self.id, user_id=user.id, role=role)
        self.business_users.append(business_user)

    # One business could have multiple addresses or phones, so they go in their own tables
    addresses = db.relationship('Address', backref='business')
    phones = db.relationship('Phone', backref='business')

    # Services provided by this business
    services = db.relationship('Service', secondary=service_business,
        backref=db.backref('businesses', lazy='dynamic'))

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer(), primary_key=True)

    # fields for physical address
    address = db.Column(db.Text)
    city = db.Column(db.String(100), nullable=False, index=True)
    state = db.Column(db.String(30), nullable=False, index=True)
    zip = db.Column(db.String(20), nullable=False, index=True)
    
    # business at this address
    business_id = db.Column(db.Integer(), db.ForeignKey('business.id'))

class Phone(db.Model):
    __tablename__ = 'phone'
    id = db.Column(db.Integer(), primary_key=True)

    # fields for phone number
    country_code = db.Column(db.String(4))
    phone_number = db.Column(db.String(20))
    extension = db.Column(db.String(20))

    # phones for this business
    business_id = db.Column(db.Integer(), db.ForeignKey('business.id'))
