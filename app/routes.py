from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, I am a recipe book!"