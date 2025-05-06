from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservations.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

class Admin(db.Model):
    __tablename__ = 'admins'
    username = db.Column(db.String, nullable=False, unique=True, primary_key=True)
    password = db.Column(db.String, nullable=False)

class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    passengerName = db.Column(db.String, nullable=False)
    seatRow = db.Column(db.Integer, nullable=False)
    seatColumn = db.Column(db.Integer, nullable=False)
    eTicketNumber = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# cost matrix
def get_cost_matrix():
    return [[100, 75, 50, 100] for _ in range(12)]

def seating_chart():
    chart = [[ 0 for _ in range(4)] for _ in range(12)]
    for res in Reservation.query.all():
        chart[res.seatRow - 1][res.seatColumn - 1] = 'X'
    return chart

def createTicketNumber(firstName):
    firstName = list(firstName)
    info = "INFOTC4320"
    info = list(info)
    a = len(firstName)
    b = len(info)
    ticketList = []
    i = 0
    if a > b:
        runIndex = a 
    else:
        runIndex = b
    while i <= runIndex:
        try:
            ticketList.append(firstName[i])
        except:
            pass
        
        try:
            ticketList.append(info[i])
        except:
            pass
        i += 1
    return ticketList

#Index page view/route
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

    show_seating_chart = seating_chart()
    return render_template('admin.html', show_seating_chart=show_seating_chart)

#Reservations page view/route
@app.route('/reserve', methods=['GET'])
def reserve():

    show_seating_chart = seating_chart()
    return render_template('reserve.html', show_seating_chart=show_seating_chart)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")