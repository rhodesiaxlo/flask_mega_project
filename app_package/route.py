from app_package import app

## 无法热修改
# 可以有格式

@app.route("/")
@app.route("/index")
def hello():
    user = {"name": "lushixin"}
    return '''
    <html>
        <head>
            <title>home page - my blog</title>
        </head>
        <body>
            <p> hello <strong>''' + user['name'] + '''</strong>
        </body>
    </html>'''
