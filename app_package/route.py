from app_package import app,db
from flask import render_template,flash,redirect,request,url_for,request
from app_package.forms import LoginForm,RegisterForm
from flask_login import current_user,login_user,logout_user,login_required
from app_package.models import User,Post
from werkzeug.urls import url_parse
import json

@app.route("/")
@app.route("/index")
@login_required
def hello():
    user = {"name": "lushixin"}
    post = [
        {
            'author':{'name':'john'},
            'body':'Beautiful day in poland'
        },
        {   'author':{'name':'Susan'},
            'body':'The Average movie is so cool !'
        }
    ]
    return render_template("index.html",  user=user, posts=post)

@app.route('/login', methods=['GET','POST'])
def login():
    #  controller-view connection
    #  request type
    #  pass parameters
    #  read parameters
    #  redirect
    # if user logined redirect to index
    next_page = request.args.get('next')
    
    if current_user.is_authenticated:
        redirect(url_for("hello"))

    form = LoginForm()
    # post request 
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        next_page = request.form.get('next_page')

        if not user or not user.check_password(form.password.data):
            flash("invalid username or password")
            # 登陆失败，如果有跳转页面，需要继续追加到 url 后面
            if next_page:
                return redirect(url_for("login",next_page=next_page))
            else:
                return redirect(url_for("login"))

        # 登陆2成功
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("hello"))
       # flash('Login requested for user {}, password {} remember_me={}'.format(
       #     form1.username.data, form1.password.data, form1.remember_me.data))
       # return redirect(url_for("hello"))
    return render_template("login.html", title="Sign in", form=form, next_page=next_page)

@app.route('/welcome')
@login_required
def welcome():
    name = request.args.get('name')
    return render_template("welcome.html", title="welcome", name=name)

@app.route("/logout")
def logout():
    logout_user();
    return redirect(url_for("hello"))

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 注册，设置密码
        u = User(username=form.username.data, email=form.email.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()

        # 跳转到用户列表
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template("register.html", title="register", form=form)
