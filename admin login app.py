from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/reservations.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

# === MODELS ===

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    row = db.Column(db.Integer, nullable=False)
    column = db.Column(db.Integer, nullable=False)
    reservation_code = db.Column(db.String, nullable=False)

# === COST MATRIX ===

def get_cost_matrix():
    return [[100, 75, 50, 100] for _ in range(12)]

# === ROUTES ===

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.password == password:  # ⚠️ Replace with hashed check in production
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')


@app.route('/admin-dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    reservations = Reservation.query.all()
    cost_matrix = get_cost_matrix()

    total_sales = 0
    for r in reservations:
        total_sales += cost_matrix[r.row][r.column]

    return render_template('admin_dashboard.html',
                           reservations=reservations,
                           total_sales=total_sales)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))
