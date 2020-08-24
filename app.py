from config import app, api, jwt
from marshml import ma
from resources.user import UserLogin, UserRegister, UserLogout, TokenRefresh
from resources.confirmation import ResendEmailConfirmationToken, EmailConfirmation

# add routes to API
api.add_resource(UserRegister, '/user/register')
api.add_resource(UserLogin, '/user/login')
api.add_resource(TokenRefresh, '/user/authenticate')
api.add_resource(UserLogout, '/user/logout')
api.add_resource(EmailConfirmation, '/user/register')

api.add_resource(ResendEmailConfirmationToken, '/resend/confirmation/email')

if __name__ == '__main__':
    ma.init_app(app)
    app.run(debug=True)