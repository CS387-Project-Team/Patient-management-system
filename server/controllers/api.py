import flask
import application
from flask import request, make_response, render_template
from controllers.auth import login_required
import controllers.dashboard, controllers.appointments

@login_required
def hello():
    return flask.Response('hello', 200)

@login_required
def dashboard():
    return controllers.dashboard.get_dashboard()

@login_required
def available_slots():
    if request.method == 'POST':
        date = request.form.get('date')
        return controllers.appointments.get_available_slots(date)
    elif request.method == 'GET':
        return render_template('appointments/available_slots.html')

@login_required
def book_appointment():
    if request.method == 'POST':
        request_data = request.form
        return controllers.appointments.book_appointment(request_data)
    elif request.method == 'GET':
        return render_template('appointments/book_slots.html')