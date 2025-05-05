from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
#Index page view/route
#'app' on these routes will need to be updated when the database is set up so the blueprints can be incorperated
#from @app.route to @[blueprint_name].bp.route

@app.route('/dashboard_redirect', methods=['POST'])
def dashboard_redirect():
    option = request.form.get('option')
    if not option:
        return redirect(url_for('index'))
        
    if option == 'admin':
        return redirect(url_for('admin'))
    elif option == 'reserve':
        return redirect(url_for('reserve'))
    return redirect(url_for('index'))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#Admin page view/route
@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')

#Reservations page view/route
@app.route('/reserve', methods=['GET'])
def reserve():
    return render_template('reserve.html')


if __name__ == '__main__':
    app.run(debug=True, port=5019)