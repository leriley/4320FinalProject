from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash, session
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
        chart[res.seatRow][res.seatColumn] = 'X'
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
    return ''.join(ticketList)

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
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('action') == 'logout':
            session.pop('admin_logged_in', None)
            return redirect(url_for('admin'))
        
        if request.form.get('action') == 'delete':
            ticket = request.form.get('ticket')
            reservation = Reservation.query.filter_by(eTicketNumber=ticket).first()
            if reservation:
                db.session.delete(reservation)
                db.session.commit()
                flash(f'Reservation {ticket} deleted successfully.')
            else:
                flash('Reservation not found.')
            return redirect(url_for('admin'))

        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.password == password:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('admin'))

    show_seating_chart = seating_chart()
    logged_in = session.get('admin_logged_in', False)
    reservations = Reservation.query.all()
    cost_matrix = get_cost_matrix()

    total_sales = 0
    for r in reservations:
        total_sales += cost_matrix[r.seatRow][r.seatColumn]

    return render_template('admin.html', show_seating_chart=show_seating_chart, logged_in=logged_in, reservations=reservations, total_sales=total_sales)

#Reservations page view/route
@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        name = request.form['name']
        seat_row = request.form['seat_row']
        seat_column = request.form['seat_column']

        if not name:
            flash('Name is required.', 'error')
            return redirect(url_for('reserve'))
        
        if not seat_row:
            flash('Row is required.', 'error')
            return redirect(url_for('reserve'))
        
        if not seat_column:
            flash('Seat is required.', 'error')
            return redirect(url_for('reserve'))
        
        ticket_number = createTicketNumber(name)

        chart = seating_chart()
        if chart[int(seat_row)][int(seat_column)] == 'X':
            flash('This seat has already been booked.', 'error')
            return redirect(url_for('reserve'))
        
        new_reservation = Reservation(passengerName=name, seatRow=seat_row, seatColumn=seat_column, eTicketNumber=ticket_number)
        db.session.add(new_reservation)
        db.session.commit()
        flash(f'You have successfully reserved Row #{seat_row}, Seat #{seat_column}. Your eTicket number is {ticket_number}. Thank you!')

    show_seating_chart = seating_chart()
    return render_template('reserve.html', show_seating_chart=show_seating_chart)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")