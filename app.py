from config import app, api, jwt
from marshml import ma


from resources.user import UserLogin, UserRegister, UserLogout, TokenRefresh, UserInfo, AutoLogin
from resources.confirmation import ResendEmailConfirmationToken, EmailConfirmation
from resources.picture import Picture
from resources.comment import Comment
from resources.reply import Reply

# add routes to API
api.add_resource(UserRegister, '/user/register')
api.add_resource(UserLogin, '/user/login')
api.add_resource(TokenRefresh, '/user/authenticate')
api.add_resource(UserLogout, '/user/logout')
api.add_resource(EmailConfirmation, '/user/register')
api.add_resource(AutoLogin, '/user/login/automation')
api.add_resource(UserInfo, '/info')


api.add_resource(ResendEmailConfirmationToken, '/resend/confirmation/email')


api.add_resource(Picture, '/pictures')
api.add_resource(Comment, '/comments')

api.add_resource(Reply,'/reply')

if __name__ == '__main__':
    ma.init_app(app)
    app.run(debug=True)
