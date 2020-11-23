'''Signup & login forms.'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class SignupForm(FlaskForm):
    '''Signup form.'''

    name = StringField(
        'Name',
        validators=[DataRequired()]
    )

    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email.'),
            DataRequired()
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )

    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    '''Login form.'''

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Log In')


class ResignForm(FlaskForm):
    '''Resign form.'''

    submit = SubmitField('Delete')


class ResetForm(FlaskForm):
    '''Reset password form.'''

    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email.'),
            DataRequired()
        ]
    )

    submit = SubmitField('Reset')
