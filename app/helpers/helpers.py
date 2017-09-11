import datetime
import uuid
from .. import app
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail
from flask_mail import Message
from app.models.models import User
from flask import request


app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='patra.manoj0@gmail.com',
    MAIL_PASSWORD='sdqipjmldfpblbqy',
    MAIL_DEFAULT_SENDER='patra.manoj0@gmail.com'
))

mail = Mail(app)


def create_user(email_id):
    new_user = User(email_id=email_id,
                    verification_code=generate_verification_code(),
                    is_verified=False,
                    created_at=datetime.datetime.now()
                    )
    return new_user


def encrypt_email(email_id):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps({'email': email_id})


def decrypt_email(code):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            request.args.get('email'),
            max_age=3600
        )
    except:
        return False
    return email['email']


def generate_verification_code():
    return uuid.uuid4().hex


def send_mail(subject, sender, recipients, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    mail.send(msg)