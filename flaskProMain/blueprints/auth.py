import string
import random
from flask import Flask,request,render_template,Blueprint,jsonify,redirect,url_for,session
from flask_mail import Message
from exts import mail,db
from models import EmailCaptchaModel,UserModel
from .forms import RegisterForm,LoginForm
#加密
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
bp=Blueprint("auth",__name__,url_prefix="/auth")
#登录
@bp.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        form=LoginForm(request.form)
        result=form.validate()
        if result:
            email = form.email.data
            password=form.password.data
            user=UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱不存在，请重新登录!")
                return redirect(url_for("auth.login"))
            else:
                if check_password_hash(user.password,password):
                    #发送给cookie
                    session["user_id"]=user.id
                    session["username"]=user.username
                    return redirect("/")
                    # return render_template('index.html')
                else:
                    print("密码错误")
                    return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            error="用户名或密码错误，请再试一次！"
            return render_template("login.html",error=error)
@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
#注册
@bp.route("/register",methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template("register.html",error=dict())
    else:
        form=RegisterForm(request.form)
        result=form.validate()
        if result:
            email=form.email.data
            username=form.username.data
            password=form.password.data
            user=UserModel(email=email,username=username,password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return render_template("register.html",error=form.errors,list_error=list(form.errors))
@bp.route("/mail/test")
def mail_test():
    message=Message(subject="[中国建设银行]银行卡封禁",recipients=["3049312375@qq.com"],body="您涉嫌在海外账户施行金额巨大的交易，先将你的银行卡封禁，请转100w给帅气的史哥哥来解封！")
    mail.send(message)
    return "邮件发送成功！"

@bp.route("/captcha/email")
def get_email_captha():
    email=request.args.get("email")
    source=string.digits*4    #'0123456789012345678901234567890123456789'
    #从source中选出4个数字
    captcha=random.sample(source,4)
    #将['3', '5', '1', '6']变为'3516'
    captcha="".join(captcha)
    message=Message(subject="博客验证码",recipients=[email],body=f"验证码是{captcha}")
    mail.send(message)
    email_captha=EmailCaptchaModel(email=email,captcha=captcha)
    db.session.add(email_captha)
    db.session.commit()
    return jsonify({"code": 200, "message": "", "data": captcha})
