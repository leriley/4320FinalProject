from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy
import os

#create a blueprint for the application
reservation_bp = Blueprint('tasks', __name__)

#Index page view/route
@reservation_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#Admin page view/route
@reservation_bp.route('/admin', methods=['GET'])
def index():
    return render_template('admin.html')

#Reservations page view/route
@reservation_bp.route('/reservations', methods=['GET'])
def index():
    return render_template('reserve.html')