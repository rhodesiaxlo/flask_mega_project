from app_package import app,db
from flask import render_template,flash,redirect,request,url_for,request
from app_package.forms import LoginForm,RegisterForm,EditprofileForm,PostForm
from flask_login import current_user,login_user,logout_user,login_required
from app_package.models import User,Post
from werkzeug.urls import url_parse
from datetime import datetime
import json


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route("/")
@app.route("/index",methods=['GET','POST'])
@login_required
def hello():
    form = PostForm()
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        # 保存 post
        print('hello world')
        post = Post(body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        redirect(url_for('hello'))
    user = {"name": "lushixin"}
    posts = current_user.followed_posts().paginate(page, app.config['POST_PERPAGE'])
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    # return json.dumps(post)
    # post = [
    #     {
    #         'author':{'name':'john'},
    #         'body':'Beautiful day in poland'
    #     },
    #     {   'author':{'name':'Susan'},
    #         'body':'The Average movie is so cool !'
    #     }
    # ]
    return render_template("index.html",  user=user, posts=posts.items, form=form,next_url=next_url,prev_url=prev_url)

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


'''
    个人profile 页面，你
'''
@app.route("/user/<username>")
def user(username):
    page = request.args.get('page', 1, type=int)
    u = User.query.filter_by(username=username).first_or_404();
    # post = [
    #     'author':u,'body':'TEST POST # 1',
    #     'author':u,'body':'TEST POST # 2',
    # ]
    posts = [
        {'author': u, 'body': 'Test post #1'},
        {'author': u, 'body': 'Test post #2'}
    ]
    posts = Post.query.filter_by(user_id=u.id).paginate(page, app.config['POST_PERPAGE'], False)
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template("user.html", title="user", posts=posts.items, user=u, prev_url=prev_url, next_url=next_url)

@app.route("/editprofile/", methods=["GET","POST"])
@login_required
def edit_profile():
    form = EditprofileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.aboutme = form.aboutme.data
        db.session.commit()
        return redirect(url_for("edit_profile"))
    elif request.method=="GET":
        form.username.data = current_user.username
        form.aboutme.data = current_user.aboutme
        return render_template("edit_profile.html", title="edit profile", form=form)



@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/explore')
def explore():
    page = request.args.get('page', 2, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,app.config['POST_PERPAGE'],False)
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template("index.html",  user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)

