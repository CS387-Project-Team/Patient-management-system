import flask
import application
from flask import request, make_response, render_template, url_for, redirect
from controllers.auth import login_required
import controllers.dashboard, controllers.appointments

@login_required
def hello():
    return flask.Response('hello', 200)

@login_required
def dashboard():
    return controllers.dashboard.get_dashboard()

@login_required
def get_appointments():
    return controllers.appointments.get_appointments()

@login_required
def update_date_free_slots():
    date = request.form.get('date', None)
    return redirect(url_for('available_slots', date=date))

@login_required
def available_slots():
    date = request.args.get("date")
    return controllers.appointments.get_available_slots(date)

@login_required
def book_appointment():
    if request.method == 'POST':
        request_data = request.form
        return controllers.appointments.book_appointment(request_data)
    elif request.method == 'GET':
        return render_template('appointments/book_slots.html')

@login_required
def cancel_appointment():
    if request.method == 'POST':
        request_data = request.form
        return controllers.appointments.cancel_appointment(request_data)
    elif request.method == 'GET':
        return render_template('appointments/cancel_appo.html')