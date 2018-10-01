from flask import Flask
import config
from apps.cms.urls import bp as cms_bp
from apps.front.urls import bp as front_bp
from exts import db,mail
from flask_mail import Message
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)

app.config.from_object(config)
CSRFProtect(app=app)
db.init_app(app)
mail.init_app(app)
# with app.app_context():
#     msg = Message("更新邮箱验证码", recipients=['940418440@qq.com'], body="验证码为" )
#     mail.send(msg)


if __name__ == '__main__':
    app.run()






