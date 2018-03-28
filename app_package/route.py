from app_package import app
from flask import render_template

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
