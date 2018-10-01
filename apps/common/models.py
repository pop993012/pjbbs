from  exts import db
from datetime import datetime

class LBT(db.Model):
    __tablename__='lbt'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    bannerName = db.Column(db.String(20), nullable=False)
    imglink = db.Column(db.String(200), nullable=False, unique=True)
    link = db.Column(db.String(200), nullable=False, unique=True)
    priority = db.Column(db.Integer, default=1)

class BK(db.Model):
    __tablename__='bk'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bkname=db.Column(db.String(20), nullable=False)
    bknum=db.Column(db.Integer,default=0)
    create_time=db.Column(db.DateTime,default=datetime.now)