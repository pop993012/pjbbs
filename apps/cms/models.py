from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class Permission:
    USER_INFO = 1           # 00000001
    BANNER = 2              # 00000010
    POSTS = 4               # 00000100
    COMMON = 8              # 00001000
    PLATE  = 16             # 00010000
    FRONT_USER = 32         # 00100000
    CMS_USER = 64           # 01000000
    CMS_USER_GROUP = 128    # 10000000



class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    _password = db.Column(db.String(200),nullable=False) # 加密过的
    email = db.Column(db.String(30),unique=True,nullable=False)
    join_time = db.Column(db.DateTime,default=datetime.now)
    # 因为要特殊处理password
    def __init__(self,password,**kwargs):
        self.password = password
        kwargs.pop('password',None)
        super(User,self).__init__(**kwargs)

    @property
    def current_user_permission(self):
        num = 0
        for role in self.roles:
            num = num | role.permissions
        print("当前这个用户的权限" + str(num))
        return num

    # 校验用户是否拥有这个权限
    def checkpermission(self, permission):
        print(str(self.current_user_permission & permission != 0))
        return self.current_user_permission & permission != 0
    @property
    def password(self):
        return self._password
    @password.setter
    def password(self,frontpwd):
        # 1. 密码不希望外界访问 2.防止循环引用
        self._password = generate_password_hash(frontpwd)
    def checkPwd(self,frontpwd):
        #return self.password == generate_password_hash(frontpwd)
        return check_password_hash(self._password,frontpwd)
cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id',db.Integer,db.ForeignKey('roel.id'),primary_key=True),
    db.Column('cms_user_id',db.Integer,db.ForeignKey('user.id'),primary_key=True)
)

class Roel(db.Model):
    __tablename__='roel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roelname=db.Column(db.String(20),unique=True,nullable=False)
    desc = db.Column(db.String(200))
    permissions = db.Column(db.Integer, default=Permission.USER_INFO)
    users = db.relationship('User', secondary=cms_role_user, backref=db.backref("roles"))

