from flask import Blueprint,request,jsonify,make_response
from flask import render_template
from flask.views import MethodView
from apps.front.forms import *
from apps.common.baseResp import *
from dysms_python.demo_sms_send import  send_sms
import string,random,json
from apps.common.captcha.xtcaptcha import Captcha
from io import BytesIO
from apps.common.models import *
from apps.common.checkaa import *
from  apps.front.models import *

bp = Blueprint('front',__name__)

@bp.route("/")
def loginView():
    banners = LBT.query.order_by(LBT.priority.desc()).limit(4)
    bk=BK.query.all()
    context = {
        'banners': banners,
        'bks':bk
    }
    return render_template("front/index.html", **context)




class Sigup(MethodView):
    def get(self):
        return  render_template('front/singUp.html')
    def post(self):
        fm =checkall(formdata=request.form)
        if fm.validate():
            r=Froneuser(username=fm.username.data,password=fm.passwprd.data,
                        telephone=fm.telephone.data)
            db.session.add(r)
            db.session.commit()
            delete(fm.telephone.data)
            delete(fm.captchacode.data)
            return jsonify(respSuccess(msg='成功了'))
        else:
            return jsonify(respParamErr(msg=fm.err))
bp.add_url_rule('/sigup/',endpoint='signup',view_func=Sigup.as_view('signup'))

class SigIN(MethodView):
    def get(self):
        local=request.headers.get('Referer')
        if not local:
            local='/'
        context={
            'local':local
        }
        return render_template('front/singIN.html',**context)
    def post(self):
        fm=checkUsername(formdata=request.form)
        print(111)
        if fm.validate():
            user=Froneuser.query.filter(Froneuser.telephone==fm.telephone.data).first()
            user=user.checkpwd(fm.password.data)
            if user:
                 return jsonify(respSuccess(msg='成功'))
            else:
                return jsonify(respParamErr(msg='密码错误'))
        else:
            return jsonify(respParamErr(msg=fm.err))
bp.add_url_rule('/sigin/',endpoint='signin',view_func=SigIN.as_view('signin'))

class CZpassword(MethodView):
    def get(self):
        return render_template('front/regisr.html')
    def post(self):
       fm=CZ(formdata=request.form)
       if fm.validate():
           user=Froneuser.query.filter(Froneuser.telephone==fm.telephone.data).first()
           if user:
               user.password =fm.password.data
               db.session.commit()
               return jsonify(respSuccess(msg='成功'))
           else:
               return  jsonify(respParamErr(msg='失败'))
       else:
           return jsonify(respParamErr(msg=fm.err))


bp.add_url_rule('/regist/',endpoint='regist',view_func=CZpassword.as_view('regist'))

@bp.route('/code/',methods=['post'])
def  zhale():
    fm=Cphone(formdata=request.form)
    if fm.validate():
        r = string.digits
        r=''.join(random.sample(r,4))
        saveCode(fm.telephone.data,r)
        print(r)
        r = send_sms(phone_numbers=fm.telephone.data,smscode=r)
        print(r)
        if json.loads(r.decode("utf-8"))['Code'] == 'OK':
            return jsonify(respSuccess("短信验证码发送成功，请查收"))
        else:  # 发送失败
            return jsonify(respParamErr("请检查网络"))

    else:
         return jsonify(respParamErr(msg=fm.err))

@bp.route('/send_imgcode/')
def ima_code():
    text,img=Captcha.gene_code()
    out=BytesIO()
    img.save(out,'png')
    out.seek(0)
    saveCode(text,text)
    print(text)
    reso=make_response(out.read())
    reso.content_type = "image/png"
    return reso

