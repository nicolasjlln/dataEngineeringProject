# run.py
import jinja2
from flask import render_template

from App import create_app

app = create_app()


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/app')
def app_run():
    return "Hello, world !"


if __name__ == '__main__':
    app.run()
