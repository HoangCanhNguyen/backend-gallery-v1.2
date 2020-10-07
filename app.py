from config import app, api, jwt
from marshml import ma


from resources.user import (
    UserLogin,
    UserRegister,
    UserLogout,
    TokenRefresh,
    User,
    PasswordConfirmation,
    ConfirmPasswordAction,
    AvatarUpload
)
from resources.vendor import (
    VendorRegister,
    VendorLogin,
    VendorLogout,
    AccountInfo,
    PendingApproval,
    VendorInfo,
    VendorList
)
from resources.picture import (
    Picture,
    PictureAction,
    PictureByCreator,
    PictrueByArtist
)

from resources.comment import Comment, CommentCreation, Comment1
from resources.reply import Reply, ReplyCreation
from resources.confirmation import ResendEmailConfirmationToken, EmailConfirmation
from resources.notification import Notification, ReplyNotification


# add routes to API
api.add_resource(UserRegister, '/user/register')
api.add_resource(UserLogin, '/user/login')
api.add_resource(TokenRefresh, '/user/authenticate')
api.add_resource(UserLogout, '/user/logout')
api.add_resource(EmailConfirmation, '/user/register')
api.add_resource(AvatarUpload, '/user/avatar/upload')
api.add_resource(PasswordConfirmation, '/authenticate')
api.add_resource(ConfirmPasswordAction, '/user/confirm/<string:token>')
api.add_resource(User, '/user')

api.add_resource(VendorLogin, '/vendor/login')
api.add_resource(VendorLogout, '/vendor/logout')
api.add_resource(VendorRegister, '/vendor/register')
api.add_resource(VendorInfo, '/vendor/information')
api.add_resource(VendorList, '/vendor/list/<string:_id>')


api.add_resource(AccountInfo, '/admin/account/manager')
api.add_resource(PendingApproval, '/admin/account/pending')


api.add_resource(ResendEmailConfirmationToken, '/resend/confirmation/email')

api.add_resource(Picture, '/pictures')
api.add_resource(PictureAction, '/picture/method')
api.add_resource(PictureByCreator, '/vendor/pictures')
api.add_resource(PictrueByArtist, '/picture/<string:artist>')

api.add_resource(Comment, '/comments')
api.add_resource(Comment1, '/comments/<string:_id>')

api.add_resource(CommentCreation, '/comment/create')

api.add_resource(Notification, '/notification/comment/<string:_id>')
api.add_resource(ReplyNotification, '/notification/reply/<string:_id>')
api.add_resource(Reply, '/reply')
api.add_resource(ReplyCreation, '/reply/create')


if __name__ == '__main__':
    ma.init_app(app)
    app.run(debug=True)
