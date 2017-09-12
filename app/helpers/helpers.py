import datetime
import uuid
from .. import app
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail
from flask_mail import Message
from app.models.models import User
from flask import request

app.config.update(dict(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='patra.manoj0@gmail.com',
    # app password
    MAIL_PASSWORD='sdqipjmldfpblbqy',
    MAIL_DEFAULT_SENDER='patra.manoj0@gmail.com'
))


mail = Mail(app)


class Helper(object):
    """ Helper Class """

    def create_user(self, email_id):
        """
        Creates a new user to commit to the database
        Args:
            email_id: User's email id
        Returns:
            A User instance
        """
        new_user = User(email_id=email_id,
                        verification_code=self.generate_verification_code(),
                        is_verified=False,
                        created_at=datetime.datetime.now()
                        )
        return new_user

    def encrypt_email(self, email_id):
        """
        Encrypt email id before sending a link to the user
        Args:
            email_id: User's email id
        Returns:
            Encrypted email
        """
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return serializer.dumps({'email': email_id})

    def decrypt_email(self, code):
        """
        Decrypts email id for verification
        Args:
            code: encrypted code
        Returns:
            email id of user
        """
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                request.args.get('email'),
                max_age=3600
            )
        except Exception:
            return False
        return email['email']

    def generate_verification_code(self):
        """
        Generate random verification code
        """
        return uuid.uuid4().hex

    def send_mail(self, subject, sender, recipients, html_body):
        """
        Sends message to user's email id
        Args:
            subject: Tile of the message
            sender: Sender of the message
            recipients: Recipients of the message
            html_body: Body of the message
        """
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.html = html_body
        mail.send(msg)


# Helper object
helper = Helper()
