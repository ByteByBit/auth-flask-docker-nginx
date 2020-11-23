'''
Logged in page routes.
[/, profile, delete_profile, logout].
'''

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required, logout_user

from src.forms import ResignForm
from src.models import db


# Blueprint config
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@main_bp.route('/', methods=['GET'])
@login_required
def main():
    '''Logged in page.'''

    return render_template(
        'main.jinja2',
        title='Flask-Login Tutorial.',
        template='main-template',
        current_user=current_user
    )


@main_bp.route("/profile")
@login_required
def profile():
    '''User profile page.'''

    return render_template(
        'profile.jinja2',
        title='Flask-Login Tutorial.',
        template='profile-template',
        current_user=current_user,
        form=ResignForm()
    )


@main_bp.route("/delete_profile", methods=['POST'])
@login_required
def delete_profile():
    '''Delete user.'''

    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    return redirect(url_for('auth_bp.login'))


@main_bp.route("/logout")
@login_required
def logout():
    '''User log out.'''

    logout_user()
    return redirect(url_for('auth_bp.login'))
