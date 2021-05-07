import flask
from flask import flash, g, Response, jsonify, render_template, redirect, url_for
import application
from application import default, my_jsonify
from datetime import datetime
from pandas import DataFrame

def show_appos():
	data = {}

	conn = application.connect()
	db = conn.cursor(cursor_factory=application.DictCursor)

	db.execute(''' select * from doctor where doc_id = %s''', (g.user.get('id'),))
	if len(db.fetchall()) == 0:
		return flask.Response('This page is only for doctors', 200)

	#num_beds
	sql = '''select app_id, patient_id, id, name, username, dat, start_time, patient_complaint 
			from person natural join patient natural join meet
			where doc_id = %s'''
	db.execute(sql, (g.user.get('id'),))
	rows = db.fetchall()
	data['appos'] = my_jsonify(rows)

	db.execute('''select * from symptom''')
	rows = db.fetchall()
	data['symptoms'] = my_jsonify(rows)

	db.execute('''select * from disease''')
	rows = db.fetchall()
	data['diseases'] = my_jsonify(rows)

	db.execute('''select * from medicine''')
	rows = db.fetchall()
	data['medicines'] = my_jsonify(rows)

	db.execute('''select * from test''')
	rows = db.fetchall()
	data['tests'] = my_jsonify(rows)

	conn.close()
	return render_template('appo_feedback/appo_feedback.html', data=data)

def handle_post(request):
	conn = application.connect()
	db = conn.cursor(cursor_factory=application.DictCursor)

	app_id = request.get('appo_id')
	symptoms = request.get('symptoms')
	diseases = request.get('diseases')
	meds = request.get('meds')
	tests = request.get('tests')
	desc = request.get('desc')


	# is the input valid?
	symptoms, diseases, meds, tests = symptoms.split(','), diseases.split(','), meds.split(';'), tests.split(',')
	try:
		if symptoms == ['']: symptoms = []
		print(symptoms)
		
		if diseases == ['']: diseases = [] 
		print(diseases)
		
		if meds == ['']: meds = []
		else:
			meds = [x.replace('(','').replace(')','') for x in meds]
			meds = [x.split(',') for x in meds]
		print(meds)
		
		if tests == ['']: tests = [] 
		print(tests)
	except Exception as e:
		print(e)
		conn.close()
		return flask.Response('The input is ill-formed, please try again with proepr input', 200)

	for x in meds:
		if len(x) != 3:
			return flask.Response('The medicines input in ill-formed, please try again with proper input', 200)


	db.execute('''select * from meet where app_id = %s and doc_id = %s''', (app_id, g.user.get('id')))
	if len(db.fetchall()) == 0:
		return flask.Response(f'There is no appointment with id {app_id} in your list, please try again with proper input', 200)

	for x in symptoms:
		db.execute('''select * from symptom where symp_id = %s''', (x, ))
		if len(db.fetchall()) == 0:
			return flask.Response(f'There is no symptom with id {x}, please try again with proper input', 200)
	
	for x in diseases:
		db.execute('''select * from disease where disease_id = %s''', (x, ))
		if len(db.fetchall()) == 0:
			return flask.Response(f'There is no disease with id {x}, please try again with proper input', 200)

	for x in meds:
		db.execute('''select * from medicine where med_id = %s''', (x[0], ))
		if len(db.fetchall()) == 0:
			return flask.Response(f'There is no medicine with id {x[0]}, please try again with proper input', 200)

	for x in tests:
		db.execute('''select * from test where test_id = %s''', (x, ))
		if len(db.fetchall()) == 0:
			return flask.Response(f'There is no test with id {x}, please try again with proper input', 200)

	db.execute('''select patient_id from meet where app_id = %s''', (app_id,))
	patient_id = db.fetchall()[0][0]

	try:
		for x in symptoms:
			db.execute('''insert into shows values (%s, %s)''', (app_id, x))

		for x in diseases:
			db.execute('''insert into suffers values (%s, %s)''', (patient_id, x))
		
		db.execute('''insert into prescription select max(presc_id)+1, %s from prescription''', (desc,))
		db.execute('''select max(presc_id) from prescription''')
		presc_id = db.fetchall()[0][0]

		db.execute('''update appointment set presc_id = %s where app_id = %s''', (presc_id, app_id))
		for x in meds:
			db.execute('''insert into meds values (%s, %s, %s, %s)''', (x[0], presc_id, x[1], x[2]))
		for x in tests:
			db.execute('''insert into should_take values (%s, %s) ''', (presc_id, x))

	except Exception as e:
		print(e)
		conn.rollback()
		conn.close()
		redirect(url_for('appo_feedback'))

	conn.commit()
	conn.close()

	return redirect(url_for('appo_feedback')) 
