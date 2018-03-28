from app_package import app

@app.route("/")
def hello():
    return "hello world !"