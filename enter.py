from app_package import app,db
from app_package.models import User,Post
from app_package import cli

@app.shell_context_processor
def test():
    return {"db":db, "User":User, "Post":Post}