import json
import re
import datetime
from flask import (Blueprint, render_template, request, make_response)
from app.models.models import User
from app.models.session import session
from app.helpers.helpers import helper

mod_auth = Blueprint('auth', __name__)

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


@mod_auth.route('/email_verification', methods=['GET', 'POST'])
def email_verification():
    """
    Sends email verification link to user
    if email is valid
    """
    if request.method == 'POST':
        email_id = request.form.get('email')
        # Checks if email is valid
        if not EMAIL_REGEX.match(email_id):
            response = make_response(json.dumps('Invalid email!'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            user = session.query(User).filter_by(email_id=email_id).first()
            # Create new user if user doesn't exist
            if user is None:
                new_user = helper.create_user(email_id)
                session.add(new_user)
                session.commit()
            # Send mail if user is not verified
            if user is not None and not user.is_verified:
                encrypted_email = helper.encrypt_email(email_id)
                v_link = 'http://localhost:8000/email_verification_link'
                code = user.verification_code
                helper.send_mail("Verification Link",
                                 'patra.manoj0@gmail.com',
                                 [email_id],
                                 "<p>Please verify your email address</p>"
                                 "<a href='{}?email={}&code={}'>".format(
                                     v_link,
                                     encrypted_email,
                                     code) +
                                 "Verification Link</a>"
                                 )
                response = make_response(json.dumps(
                    "Verification Email sent to your Mail Id"), 200)
                response.headers['Content-Type'] = 'application/json'
                return response
            # Check if user is verified
            elif user.is_verified:
                response = make_response(json.dumps(
                    'Email already verified'), 200)
                response.headers['Content-Type'] = 'application/json'
                return response
    else:
        return render_template("main.html")


@mod_auth.route('/email_verification_link', methods=['GET'])
def verify_user():
    """
    Verify user and update user data in database
    """
    email_id = helper.decrypt_email(request.args.get('email'))
    code = request.args.get('code')
    user = session.query(User).filter_by(email_id=email_id).first()
    if user is not None and not user.is_verified:
        # Check if user's verification code same as that in
        # verification link
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
    # Check if user is already verified
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
