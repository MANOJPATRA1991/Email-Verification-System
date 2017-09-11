import json
import re
import datetime
from flask import (Blueprint, render_template, request, make_response)
from app.models.models import User
from app.models.session import session
from app.helpers.helpers import create_user, encrypt_email, send_mail, decrypt_email

mod_auth = Blueprint('auth', __name__)

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


@mod_auth.route('/email_verification', methods=['GET','POST'])
def email_verification():
    if request.method == 'POST':
        email_id = request.form.get('email')
        if not EMAIL_REGEX.match(email_id):
            response = make_response(json.dumps('Invalid email!'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            user = session.query(User).filter_by(email_id=email_id).first()
            if user is None:
                new_user = create_user(email_id)
                session.add(new_user)
                session.commit()
                print(new_user)
            if user is not None and not user.is_verified:
                encrypted_email = encrypt_email(email_id)
                verification_link = 'http://localhost:8000/email_verification_link'
                code = user.verification_code
                send_mail("Verification Link",
                          'patra.manoj0@gmail.com',
                          [email_id],
                          "<p>Please verify your email address</p>"\
                          "<a href='{}?email={}&code={}'>Verification Link</a>".format(verification_link,
                                                                         encrypted_email,
                                                                         code))
                response = make_response(json.dumps(
                    "Verification Email sent to your Mail Id"), 200)
                response.headers['Content-Type'] = 'application/json'
                return response
            elif user.is_verified:
                response = make_response(json.dumps(
                    'Email already verified'), 200)
                response.headers['Content-Type'] = 'application/json'
                return response
    else:
        return render_template("main.html")


@mod_auth.route('/email_verification_link', methods=['GET'])
def verify_user():
    email_id = decrypt_email(request.args.get('email'))
    code = request.args.get('code')
    user = session.query(User).filter_by(email_id=email_id).first()
    if user is not None and not user.is_verified:
        if user.verification_code == code:
            user.is_verified = True
            user.updated_at = datetime.datetime.now()
            session.add(user)
            session.commit()
            response = make_response(json.dumps(
                "Email verified."), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            response = make_response(json.dumps(
                "Email not Verified, Retry."), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
    elif user is not None and user.is_verified:
        response = make_response(json.dumps(
            "Email already Verified."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            "Email not Verified, Retry."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

