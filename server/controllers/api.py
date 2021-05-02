import flask
import application
from flask import request, make_response, render_template, url_for, redirect
from controllers.auth import login_required
import controllers.dashboard, controllers.appointments, controllers.analytics
import controllers.generic_info

@login_required
def hello():
    return flask.Response('hello', 200)

@login_required
def dashboard():
    return controllers.dashboard.get_dashboard()

@login_required
def profile():
    if request.method == 'GET':
        return controllers.dashboard.get_profile()
    else:
        data = request.form
        return controllers.dashboard.update_profile(data)

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

# @login_required
# def confirm_appointment_post():
#     data = request.form
#     doc_name = data.get('doctor_name')
#     doc_id = int(data.get('doctor_id'))
#     date = data.get('date')
#     time = data.get('time')
#     print(data)
#     return redirect(url_for('confirm_appointment_get', doctor_name=doc_name, doctor_id=doc_id, date=date, time=time))

# @login_required
# def confirm_appointment_get():
#     if request.args.get('doctor_id') is None:
#         return redirect(url_for('available_slots'))
#     data = {}
#     data['doctor_name'] = request.args.get('doctor_name')
#     data['doctor_id'] = int(request.args.get('doctor_id'))
#     data['date'] = request.args.get('date')
#     data['time'] = request.args.get('time')    
#     return controllers.appointments.confirm_booking(data)

@login_required
def book_appointment():
    if request.method == 'POST':
        request_data = request.form
        return controllers.appointments.book_appointment(request_data)
    elif request.method == 'GET':
        return redirect(url_for('available_slots'))

@login_required
def cancel_appointment():
    if request.method == 'POST':
        request_data = request.form
        return controllers.appointments.cancel_appointment(request_data)
    elif request.method == 'GET':
        return redirect(url_for('get_appointments'))

def view_info():
    return controllers.generic_info.get_info()

def get_analytics():
    return controllers.analytics.get_analytics()

def show_analytics():
    return render_template('analytics/daywise.html')

def get_disease_analytics(disease_id):
    return controllers.analytics.get_disease_analytics(disease_id)

def show_disease_analytics(disease_id):
    # disease_id = request.args.get('disease_id', None)
    # if disease_id is None:
    #     return render_template('analytics/disease-wise.html')
    return controllers.analytics.show_disease_analytics(disease_id)

def post_disease_for_analytics():
    disease_name = request.form.get('disease')
    return controllers.analytics.post_disease_for_analytics(disease_name)