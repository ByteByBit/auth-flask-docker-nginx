from threading import Thread

from flask_mail import Message, Mail
from flask import render_template, url_for

from server import app
from src.login.models import UserToken


class MailBody(Message):
    '''Email body.'''

    def __init__(self):
        
        app.config.from_object('src.config.MailerConfig')
        super(MailBody, self).__init__(sender=app.config['SENDER'])
        self.set_message()

    def set_message(self):
        '''Set up email message.'''

        self.subject = self.SUBJECT
        self.recipients = [self.email]
        self.token = UserToken.create(email=self.email)

        # Construct url for email purpose (confirm, change passw.)
        self.route_url = url_for(
            self.ROUTE_ID, token=self.token, _external=True
        )
        self.html = self.get_html()

        # Attach the logo to the mail.
        self.attach(
            'logo.png',
            'image/png',
            open('src/static/dist/img/logo.png', 'rb').read(),
            'inline',
            headers=[['Content-ID', '<logo>'], ]
        )

    def get_html(self):
        '''Render html for mail body.'''

        return render_template(
            'mail_layout.jinja2',
            text=self.MAIL_TXT,
            uri=self.route_url,
            action_text=self.ACTION_TXT
        )


class ResetMail(MailBody):
    '''Reset password mail.'''

    SUBJECT = 'Reset your password!'
    MAIL_TXT = 'reset your password'
    ROUTE_ID = 'auth_bp.recover'
    ACTION_TXT = 'Reset'

    def __init__(self, email: str):

        self.email = email
        super(ResetMail, self).__init__()


class ConfirmMail(MailBody):
    '''Account confirm mail.'''

    SUBJECT = 'Confirm your account!'
    MAIL_TXT = 'confrim your account'
    ROUTE_ID = 'auth_bp.confirm'
    ACTION_TXT = 'Confirm'

    def __init__(self, email: str):

        self.email = email
        super(ConfirmMail, self).__init__()


class Mailer:
    """Mail sender."""

    def __init__(self, msg: Message):

        self.mailer = Mail(app=app)
        self.mailer.init_app(app)
        self.msg = msg

    def send_async(self):

        with app.app_context():
            self.mailer.send(self.msg)

    def send(self):

        # Start a thread for mail sending,
        # do not block the main thread with it.
        Thread(target=self.send_async).start()
