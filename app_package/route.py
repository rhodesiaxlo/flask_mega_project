from app_package import app
from flask import render_template

@app.route("/")
@app.route("/index")
def hello():
    user = {"name": "lushixin"}
    return render_template("index.html",  user=user)
