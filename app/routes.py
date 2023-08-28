from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Katy'}
    recipes = [
        {
            'author': {'username': 'John'},
            'name': 'Apple pie'
        },
        {
            'author': {'username': 'Susan'},
            'name': 'Pumpkin soup'
        },
        {
            'author': {'username': 'Dora'},
            'name': 'Pumpkin cinnamon buns'
        }
    ]
    return render_template('index.html', title='Home', user=user, recipes=recipes)