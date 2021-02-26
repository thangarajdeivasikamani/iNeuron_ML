from app import app

from app import app

@app.route("/")
def index():
    return "Hello world"

@app.route("/about")
def about():
    #return "<h1 style='color: red;'>I'm a red H1 heading!</h1>"
    return """
     <h1 style='color: red;'>I'm a red H1 heading!</h1>
     <p>This is a lovely little paragraph</p>
     <code>Flask is <em>awesome</em></code>
     """