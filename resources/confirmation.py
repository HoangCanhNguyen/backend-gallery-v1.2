from flask_restful import Resource, request
from flask import url_for, render_template, redirect, make_response
from threading import Thread

from confirmation_token import generate_confirmation_token
from models.user import UserModule
from models.confirmation import ConfirmationModule
from mail import Mail


class EmailConfirmation(Resource):
    def get(self):
        token = request.args.get('token')
        email = ConfirmationModule.confirm_email(token)
        # if email:
        #     auth_url = url_for('passwordconfirmation', token=token)
        #     return redirect(auth_url)

class ResendEmailConfirmationToken(Resource):
    def post(self):
        email = request.get_json()["email"]

        token = generate_confirmation_token(email)
        confirm_url = url_for('userregister', token=token, _external=True)

        sending_thread = Thread(target=Mail.send_mail_confirmation_to_user, args=(
            email, confirm_url,), daemon=True)
        sending_thread.start()

        return {"msg": "GỬI THÀNH CÔNG MÃ XÁC THỰC ĐẾN EMAIL CỦA BẠN"}, 200