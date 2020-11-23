'''User & Database models.'''

import datetime
import string
import random

from flask import flash
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from src import db


class User(UserMixin, db.Model):
    '''User model.'''

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
    )
    created = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=db.func.now()
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    login_type = db.Column(
        db.String(10),
        nullable=False
    )
    confirmed = db.Column(
        db.Boolean,
        default=False
    )

    def set_password(self, password):
        '''Set hashed password.'''

        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        '''Validate password.'''

        return check_password_hash(self.password, password)

    def set_last_login(self,):
        '''Set last login to current time.'''

        self.last_login = datetime.datetime.now()

    def get_last_login(self):
        '''Get last login time.'''

        return self.last_login.strftime('%d %b %Y - %H:%M:%S')

    @staticmethod
    def exist(email: str):
        '''If user exists.'''

        if User.get(email=email):
            return True

        return False

    @staticmethod
    def get(email: str):
        '''Get user.'''

        return User.query.filter_by(email=email).first()

    def __repr__(self):

        return '<User {}>'.format(self.name)


class CreateUser:
    '''Create user.'''

    LOGIN_TYPES = ['fb', 'google']

    def __init__(self, email: str):
        self.email = email

    def create(self, name: str, login_type: str, password: str = ''):

        confirmed = False
        if login_type in self.LOGIN_TYPES:
            # For social signup, create a random password.
            password = self.get_random_password()
            confirmed = True

        # Create user.
        self.user = User(
            name=name,
            email=self.email,
            login_type=login_type,
            confirmed=confirmed
        )
        self.user.set_password(password=password)
        self.user.set_last_login()

        db.session.add(self.user)
        self.commit_db()
        return self.user

    def commit_db(self):
        '''Commit db.'''

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            flash('An error happened, please try again!')
            return False

        return True

    @staticmethod
    def get_random_password():
        ''' Create dummy password for social login. '''

        chars = string.ascii_uppercase + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(12))
