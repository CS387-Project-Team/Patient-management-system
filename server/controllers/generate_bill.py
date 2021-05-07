import flask
from flask import flash, g, Response, jsonify, render_template, redirect, url_for
import application
from application import default, my_jsonify
from datetime import datetime
from pandas import DataFrame

def show_test():
	data = {}

	conn = application.connect()
	db = conn.cursor(cursor_factory=application.DictCursor)

	db.execute(''' select * from support_staff where staff_id = %s''', (g.user.get('id'),))
	if len(db.fetchall()) == 0:
		return flask.Response('This page is only for support staff', 200)

	db.execute('''select patient_id, person.id as pid, person.name as pname, username, 
						test_id, test.name as tname, charges, result_file, comments, dat, bill_no 
				from person, patient natural join takes natural join test where person.id = patient.id;''')
	rows = db.fetchall()
	data['tests'] = my_jsonify(rows)

	db.execute('''select * from bill''')
	rows = db.fetchall()
	data['bills'] = my_jsonify(rows)

	conn.close()
	return render_template('bill/test.html', data=data)


def handle_post_test(request):
	conn = application.connect()
	db = conn.cursor(cursor_factory=application.DictCursor)

	pid = request.get('patient_id')
	test_id = request.get('test_id')
	date = request.get('date')
	purpose = request.get('purpose')
	discount = request.get('discount')

	if int(discount) < 0 or int(discount) > 100:
		return flask.Response('Invalid input for discount, please retry with a number between 0 and 100', 200)
	if purpose not in ['OPD', 'Pharmacy', 'Admission', 'Diagnosis']:
		return flask.Response('Purpose has to be one of OPD, Pharmacy, Admission, or Diagnosis, please try again with one of these values ', 200)

	db.execute('''select * from takes where patient_id = %s and test_id = %s and dat = %s''', (pid, test_id, date))
	if len(db.fetchall()) == 0:
		return flask.Response(f'Patient with id {pid} has not taken test {test_id} on {date}, please try again with proper input', 200)

	db.execute('''select * from takes where patient_id = %s and test_id = %s and dat = %s and bill_no is null''', (pid, test_id, date))
	if len(db.fetchall()) == 0:
		return flask.Response('A bill is already linked to this (patient, test, date) tuple', 200)

	db.execute('''select max(bill_no) from bill''')
	bill_no = db.fetchall()[0][0] + 1

	try:
		db.execute('''insert into bill values (%s, null, %s, %s, null)''', (bill_no, purpose, discount))
		db.execute('''update takes set bill_no = %s where patient_id = %s and test_id = %s and dat = %s''', 
			(bill_no, pid, test_id, date))
	except Exception as e:
		print(e)
		conn.rollback()
		conn.close()
		return redirect(url_for(generate_bill_test))

	conn.commit()
	conn.close()

	return redirect(url_for('generate_bill_test')) 


def show_medicine():
	pass

def handle_post_medicine(request):
	pass

def show_appo():
	data = {}

	conn = application.connect()
	db = conn.cursor(cursor_factory=application.DictCursor)

	db.execute(''' select * from support_staff where staff_id = %s''', (g.user.get('id'),))
	if len(db.fetchall()) == 0:
		return flask.Response('This page is only for support staff', 200)

	db.execute('''select * from meet natural join appointment''')
	rows = db.fetchall()
	data['appos'] = my_jsonify(rows)

	db.execute('''select * from bill''')
	rows = db.fetchall()
	data['bills'] = my_jsonify(rows)

	conn.close()
	return render_template('bill/appointment.html', data=data)

def handle_post_appo(request):
	conn = application.connect()
	db = conn.cursor(cursor_factory=application.DictCursor)

	app_id = request.get('app_id')
	purpose = ''
	discount = request.get('discount')

	if int(discount) < 0 or int(discount) > 100:
		return flask.Response('Invalid input for discount, please retry with a number between 0 and 100', 200)
	
	db.execute('''select * from appointment where app_id = %s''', (app_id,))
	if len(db.fetchall()) == 0:
		return flask.Response(f'No appointment exists with id {app_id}, please try again with proper input', 200)

	db.execute('''select type from appointment where app_id = %s and bill_no is null ''', (app_id,))
	rows = db.fetchall()
	if len(rows) == 0:
		return flask.Response('A bill is already linked to this appointment', 200)
	else:
		purpose = rows[0][0]

	db.execute('''select max(bill_no) from bill''')
	bill_no = db.fetchall()[0][0] + 1

	try:
		db.execute('''insert into bill values (%s, null, %s, %s, null)''', (bill_no, purpose, discount))
		db.execute('''update appointment set bill_no = %s where app_id = %s''', (bill_no, app_id))
	except Exception as e:
		print(e)
		conn.rollback()
		conn.close()
		return redirect(url_for(generate_bill_appo))

	conn.commit()
	conn.close()

	return redirect(url_for('generate_bill_appo')) 