from flask import Flask,request,render_template,Blueprint,jsonify,redirect,url_for,session,g
from models import QuestionModel,AnswerModel,UserModel
from .forms import QuestionForm,AnswerForm,ReviseForm
from exts import db
from werkzeug.utils import secure_filename
import os
import requests
from decorators import login_required
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
bp=Blueprint("qa",__name__,url_prefix="/")
@bp.route("/revise",methods=["GET","POST"])
def revise():
    if request.method=="GET":
        id = session.get("user_id")
        user = UserModel.query.filter_by(id=id).first()
        return render_template("revise.html",user=user)
    else:
        mainform = request.form
        Rform = ReviseForm(request.form)
        if Rform.validate():
            id = session.get("user_id")
            user=UserModel.query.filter_by(id=id).first()
            # if mainform.get("username") != NULL and mainform.get("biography")!=NULL:
            if 'profile_picture' in request.files:
                file = request.files['profile_picture']
                if file.filename != '':
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join("static/images", filename))
            print(request.files['profile_picture'])
            user.username=mainform.get("username")
            user.myself=mainform.get("biography")
            user.image="static/images/{}".format(filename)
            db.session.commit()
            #重点，名字更改了但是session中的名字没有更改，需要更新session
            session["username"]=mainform.get("username")
            return redirect(url_for("qa.myself"))
        else:
            print(Rform.errors)
            return redirect(url_for("qa.revise"))
@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template("index.html",questions=questions)
@bp.route("/myself")
def myself():
    user_id = int(session.get("user_id"))
    user = UserModel.query.get(user_id)
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template("myself.html", questions=questions, user = user)
@bp.route("/qa/detail/<qa_id>",methods=["POST","GET"])
def qa_detail(qa_id):
    if request.method=="GET":
        question = QuestionModel.query.get(qa_id)
        return render_template("detail.html",question=question)
    else:
        if session.get("delete")=="success":
            return redirect("/")
        else:
            question = QuestionModel.query.get(qa_id)
            return render_template("detail.html",question=question)
@bp.route("/answer/public_answer",methods=["POST"])
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content,question_id=question_id,author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail",qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail",qa_id=request.form.get("question_id")))

@bp.route("/qa/delete",methods=["GET","POST"])
def delete_post():
    data = request.form['data']
    data=int(data)
    question = QuestionModel.query.get(data)
    session["delete"]="success"
    db.session.delete(question)
    db.session.commit()
    return "Delete successfully"

@bp.route("/search")
def search():
    q = request.args.get("q")
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template("index.html",questions=questions)
@bp.route("/public_question",methods=["GET","POST"])
@login_required
def public_question():
    if request.method == "GET":
        return render_template("public_question.html")
    else:
        print(request.form)
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title,content=content,author_id=session.get("user_id"))
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))