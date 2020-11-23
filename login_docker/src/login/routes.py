''' 
Login routes.
[signup, login, reset, confirm, recover]
'''

from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import current_user, login_user, logout_user

from src.login.forms import LoginForm, SignupForm, ResetForm, RecoverForm
from src.models import db, User, CreateUser
from src.login.models import SocialLogin
from src import login_manager


# Blueprint config.
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='src/templates',
    static_folder='static'
)


@auth_bp.route(
    '/signup', methods=['GET', 'POST'])
def signup():
    '''
    User sign-up page.

    [GET] sign-up page.
    [POST] validate form & user creation.
    '''

    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        if User.exist(email=email):  # User exists.
            flash('User exists.')
        else:
            create_u = CreateUser(email=email)
            user = create_u.create(
                name=form.name.data,
                password=form.password.data,
                login_type="site"
            )
            create_u.commit_db()

            from src.mailer.mail import Mailer, ConfirmMail
            msg = ConfirmMail(user.email)
            mailer = Mailer(msg)

            # Send email with reset uri.
            mailer.send()
            flash('We just sent you an email to confirm your account.')

        # Login page.
        return render_template(
            'login.jinja2',
            form=form,
            title='Log in.',
            template='login-page'
        )

    # Signup page.
    return render_template(
        'signup.jinja2',
        title='Join  our community!',
        form=form,
        template='signup-page'
    )


@auth_bp.route(  # Site login.
    '/login/', methods=['GET', 'POST'])
@auth_bp.route(  # Social media login.
    '/login/<provider>', methods=['GET', 'POST'])
def login(provider=None):
    '''
    User login page.

    param:
    provider (str): Login provider [ site | google | fb ]

    [GET] Login page.
    [POST] Validate form & user login.
    '''

    # User already logged in.
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.main'))

    form = LoginForm()
    if provider:
        sl = SocialLogin(provider)
        response, result = sl.login(request)
        if result:
            if result.user:

                # Update data from provider.
                result.user.update()
                email = result.user.email

                if not User.exist(email=email):
                    # Create user.
                    create_u = CreateUser(email=email)
                    user = create_u.create(
                        name=result.user.name,
                        login_type=provider
                    )
                else:
                    user = User.get(email=email)

                # Login.
                login_user(user=user)

            next_page = request.args.get('next')
            return redirect(next_page or url_for('main_bp.main'))

        return response
    else:
        # Validate login attempt.
        if form.validate_on_submit():

            email = form.email.data

            if User.exist(email=email):
                user = User.get(email=email)
                if user and user.confirmed and user.check_password(form.password.data):

                    login_user(user)
                    # Logged in.
                    next_page = request.args.get('next')
                    return redirect(next_page or url_for('main_bp.main'))

                flash('User not registered.')

            # return redirect(url_for('auth_bp.login'))

    # Login page.
    return render_template(
        'login.jinja2',
        form=form,
        title='Log in.',
        template='login-page'
    )


@auth_bp.route(  # Forgot password.
    '/reset', methods=['GET', 'POST'])
def reset():
    '''
    Reset password page.

    [GET] Reset page.
    [POST] Validate form & send reset email.
    '''

    form = ResetForm()
    if form.validate_on_submit():
        email = form.email.data

        if User.exist(email=email):

            user = User.get(email=email)

            from src.mailer.mail import Mailer, ResetMail
            msg = ResetMail(user.email)

            mailer = Mailer(msg)
            # Send email with reset uri.
            mailer.send()
            flash('An email sent to you.')
        else:
            flash('The email address is not registered.')

    return render_template(
        'reset.jinja2',
        title='Password recovery.',
        form=form,
        template='login-page'
    )


@auth_bp.route(  # Confirm.
    '/confirm/<token>', methods=['GET', 'POST'])
def confirm(token=None):
    ''''''
    from src.login.models import UserToken
    email = UserToken.verify(token)

    if not email:
        flash('User not found.')
        return redirect(url_for('auth_bp.login'))

    user = User.query.filter_by(email=email).first()
    if user:
        user.confirmed = True
        db.session.commit()
        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('main_bp.main'))

    form = LoginForm()
    # Login page.
    return render_template(
        'login.jinja2',
        form=form,
        title='Log in.',
        template='login-page'
    )


@auth_bp.route(  # Recover form.
    '/recover/', methods=['GET', 'POST'])
@auth_bp.route(  # Recover.
    '/recover/<token>', methods=['GET', 'POST'])
def recover(token=None):
    '''
    User login page.

    param:
    token (str): JWT token.

    [GET] Change password page.
    [POST] Validate form & change password.
    '''

    if request.method == 'GET':
        from src.login.models import UserToken
        email = UserToken.verify(token)

        if not email:
            flash('User not found.')
            return redirect(url_for('auth_bp.login'))

    form = RecoverForm()
    if form.validate_on_submit():

        email = form.email.data
        if User.exist(email=email):
            user = User.get(email=email)
            # Change password and commit.
            user.set_password(form.password.data)
            db.session.commit()

            flash('Password changed.')
            return redirect(url_for('auth_bp.login'))

    # Change password page.
    return render_template(
        'recover.jinja2',
        title='Reset your password.',
        form=form,
        template='login-page'
    )


@login_manager.user_loader
def load_user(user_id):
    ''' Check if user is logged-in upon page load.  '''

    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    ''' Redirect unauthorized users to login page. '''

    flash('Log in to view this page.')
    return redirect(url_for('auth_bp.login'))
