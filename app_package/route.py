from app_package import app
from flask import render_template,flash,redirect,request
from app_package.forms import LoginForm

@app.route("/")
@app.route("/index")
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
    form1 = LoginForm()

    # post request 
    if form1.validate_on_submit():
       flash('Login requested for user {}, password {} remember_me={}'.format(
           form1.username.data, form1.password.data, form1.remember_me.data))
       return redirect('/index')
    return render_template("login.html", title="Sign in", form=form1)

@app.route('/welcome')
def welcome():
    name = request.args.get('name')
    return render_template("welcome.html", title="welcome", name=name)
