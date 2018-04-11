from app_package import app

@app.cli.group()
def testcmd():
    """this is testcmd information."""
    pass