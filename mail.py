from flask import render_template
from flask_mail import Mail, Message


from config import app


mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'bkgallery611@gmail.com',
    "MAIL_PASSWORD": 'jkeufmsxqhqpctjt'
}

app.config.update(mail_settings)
mail = Mail(app)


class Mail:
    @classmethod
    def send_mail_confirmation_to_user(cls, email, confirm_url):
        with app.app_context():
            msg = Message(subject="Xác thực tài khoản Tranh Việt",
                            sender=app.config.get("MAIL_USERNAME"),
                            recipients=[email]
                            )
            msg.html = render_template(
                'email_confirmation.html',confirm_url=confirm_url)
            try:
                mail.send(msg)
            except:
                return False

    @classmethod
    def send_approval_mail_to_admin(cls, admin_email, email, confirm_url):
        with app.app_context():
            msg = Message(subject="Xác thực tạo tài khoản vendor",
                            sender=app.config.get("MAIL_USERNAME"),
                            recipients=[admin_email]
                            )
            msg.html = render_template(
                'create_vendor_approval.html',confirm_url=confirm_url)
            try:
                mail.send(msg)
            except:
                return False