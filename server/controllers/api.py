import flask
import application
from flask import request, make_response, render_template, url_for, redirect
from controllers.auth import login_required
import controllers.dashboard, controllers.appointments, controllers.analytics
import controllers.tests, controllers.administer_test, controllers.dis_symp
import controllers.doc_slots
import controllers.assign_room
import controllers.generic_info
import controllers.dashboard, controllers.appointments, controllers.analytics, controllers.tests, controllers.administer_test
import controllers.generic_info, controllers.beds, controllers.inventory, controllers.appo_feedback, controllers.generate_bill

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
def view_history():
	return controllers.dashboard.view_history()

@login_required
def add_history():
	if request.method == 'GET':
		return controllers.dashboard.get_history_for_edit()
	else:
		data = request.form
		print(data)
		return controllers.dashboard.add_history(data)

@login_required
def delete_history():
	data = request.form
	return controllers.dashboard.delete_history(data)

@login_required
def update_history():
	data = request.form
	return controllers.dashboard.update_history(data)

@login_required
def get_appointments():
	return controllers.appointments.get_appointments()

@login_required
def update_date_free_slots():
	date = request.form.get('date', None)
	return redirect(url_for('available_slots', date=date))

@login_required
def update_date_free_slots_followup():
	date = request.form.get('date', None)
	doc_id = request.form.get('doc_id', None)
	patient_id = request.form.get('patient_id', None)
	return redirect(url_for('available_slots_followup', doc_id=doc_id, patient_id=patient_id, date=date))

@login_required
def available_slots():
	date = request.args.get("date")
	return controllers.appointments.get_available_slots(date)

@login_required
def available_slots_followup():
	date = request.args.get("date")
	doc_id = request.args.get("doc_id")
	patient_id = request.args.get("patient_id")
	return controllers.appointments.get_available_slots_followup(patient_id, doc_id, date)
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
def get_inventory():
	return controllers.inventory.get_inventory()

@login_required
def add_bed():
	request_data = request.form
	return controllers.inventory.add_bed(request_data)

@login_required
def remove_bed():
	request_data = request.form
	return controllers.inventory.remove_bed(request_data)

@login_required
def add_room():
	request_data = request.form
	return controllers.inventory.add_room(request_data)

@login_required
def add_test():
	request_data = request.form
	return controllers.inventory.add_test(request_data)

@login_required
def add_medicine():
	request_data = request.form
	return controllers.inventory.add_medicine(request_data)

@login_required
def add_eqp():
	request_data = request.form
	return controllers.inventory.add_eqp(request_data)

@login_required
def pay_bill():
	request_data = request.form
	return controllers.dashboard.pay_bill(request_data)

@login_required
def view_resp():
	return controllers.dashboard.get_staff_resp()

@login_required
def assg_room_resp():
	request_data = request.form
	return controllers.dashboard.assg_staff_room(request_data)

@login_required
def assg_eqp_resp():
	# print("jere")
	request_data = request.form
	return controllers.dashboard.assg_staff_eqp(request_data)

@login_required
def evict_resp():
	request_data = request.form
	return controllers.dashboard.evict_staff_resp(request_data)

@login_required
def add_admin():
    if request.method == 'GET':
        return controllers.dashboard.get_admin_dashboard()
    elif request.method == 'POST':
        request_data = request.form
        return controllers.dashboard.add_admin(request_data)

@login_required
def remove_staff():
    request_data = request.form
    return controllers.dashboard.remove_staff(request_data)

@login_required
def add_doctor():
    request_data = request.form
    return controllers.dashboard.add_doctor(request_data)

@login_required
def add_staff():
    request_data = request.form
    return controllers.dashboard.add_staff(request_data)

@login_required
def add_remove_staff():
    return controllers.dashboard.get_staff()

@login_required
def upd_doctor():
    request_data = request.form
    return controllers.dashboard.upd_doctor(request_data)

@login_required
def upd_staff():
    request_data = request.form
    return controllers.dashboard.upd_staff(request_data)

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

@login_required
def update_complaint():
	data = request.form
	return controllers.appointments.update_complaint(data)
## tests
@login_required
def get_tests():
	return controllers.tests.get_tests()

@login_required
def book_test():
	if request.method == 'POST':
		request_data = request.form
		return controllers.tests.book_test(request_data)
	elif request.method == 'GET':
		return redirect(url_for('available_tests'))

@login_required
def available_tests():
	return controllers.tests.get_available_tests()

@login_required
def cancel_test():
	if request.method == 'POST':
		request_data = request.form
		return controllers.tests.cancel_test(request_data)
	elif request.method == 'GET':
		return redirect(url_for('get_appointments'))

@login_required
def administer_test():
	if request.method=='POST':
		request_data=request.form
		return controllers.administer_test.edit_test(request_data)
	elif request.method=='GET':
		return controllers.administer_test.show_tests()


@login_required
def view_dis_symp():
    return controllers.dis_symp.show_dis_symp()

@login_required
def add_dis():
    request_data=request.form
    return controllers.dis_symp.add_disease(request_data)

@login_required
def add_symp():
    request_data=request.form
    return controllers.dis_symp.add_symptom(request_data)

@login_required
def assign_room():
    if request.method=='GET':
        return controllers.assign_room.show_slots()
    else:
        request_data=request.form
        return controllers.assign_room.edit_slot(request_data)

@login_required
def get_week_slots():
	if request.method=='GET':
		return controllers.doc_slots.show_all()
	else:
		request_data=request.form
		return controllers.doc_slots.change(request_data)

def view_info():
	return controllers.generic_info.get_info()

def get_analytics():
	return controllers.analytics.get_analytics()

def show_analytics():
	data = controllers.analytics.get_analytics(json_=False)
	return render_template('analytics/daywise.html', data=data)

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

@login_required
def allot_beds():
	if request.method == 'GET':
		return controllers.beds.show_stuff()
	elif request.method == 'POST':
		return redirect(url_for('allot_beds2'))

@login_required
def allot_beds2():
	if request.method == 'GET':
		return render_template('beds/allot_beds2.html')
	elif request.method == 'POST':
		return controllers.beds.allot_beds(request.form)

# @login_required
# def add_bed():
# 	if request.method == 'GET':
# 		return controllers.inventory.render_add_bed()
# 	elif request.method == 'POST':
# 		return controllers.inventory.handle_post(request.form)

@login_required
def appo_feedback():
	if request.method == 'GET':
		return controllers.appo_feedback.show_appos()
	elif request.method == 'POST':
		return controllers.appo_feedback.handle_post(request.form)

@login_required
def generate_bill_test():
	if request.method == 'GET':
		return controllers.generate_bill.show_test()
	elif request.method == 'POST':
		return controllers.generate_bill.handle_post_test(request.form)

@login_required
def generate_bill_medicine():
	if request.method == 'GET':
		return controllers.generate_bill.show_medicine()
	elif request.method == 'POST':
		return controllers.generate_bill.handle_post_medicine(request.form)

@login_required
def generate_bill_appo():
	if request.method == 'GET':
		return controllers.generate_bill.show_appo()
	elif request.method == 'POST':
		return controllers.generate_bill.handle_post_appo(request.form)
