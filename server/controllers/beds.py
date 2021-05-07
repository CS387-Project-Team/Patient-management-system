import flask
from flask import flash, g, Response, jsonify, render_template, redirect, url_for
import application
from application import default, my_jsonify
from datetime import datetime
from pandas import DataFrame

def show_stuff():
	data = {}

	conn = application.connect()
	db = conn.cursor(cursor_factory=application.DictCursor)

	#doctors
	sql = '''select patient_id, id as person_id, name, username
		  from person natural join patient
		  order by patient_id'''
	db.execute(sql)
	rows = db.fetchall()
	data['patients'] = my_jsonify(rows)

	#occupies
	sql = '''select * from occupies'''
	db.execute(sql)
	rows = db.fetchall()
	data['occupies'] = my_jsonify(rows)

	#rooms/ward
	sql = '''select distinct(type) from room'''
	db.execute(sql)
	rows = db.fetchall()
	data['rooms'] = my_jsonify(rows)

	#num_beds
	sql = '''select type, count(bed_no) as cnt from bed group by type'''
	db.execute(sql)
	rows = db.fetchall()
	data['beds'] = my_jsonify(rows)

	conn.close()
	return render_template('beds/allot_beds.html', data=data)

def allot_beds(request):
	conn = application.connect()
	db = conn.cursor(cursor_factory=application.DictCursor)
	
	pid = request.get('patient_id')
	room_type = request.get('room_type')
	bed_type = request.get('bed_type') 

	db.execute(''' select * from patient where patient_id = %s ''', (pid,))
	if len(db.fetchall()) == 0:
		return flask.Response('No patient with the given id exists', 200) 

	db.execute(''' select * from room where type = %s ''', (room_type,))
	if len(db.fetchall()) == 0:
		return flask.Response('No room with the given type exists', 200)  

	db.execute(''' select * from bed where type = %s ''', (bed_type,))
	if len(db.fetchall()) == 0:
		return flask.Response('No bed with the given type exists', 200) 

	sql = '''(select bed_no from room, bed 
				where bed.type = %s and room.type = %s)
			except 
			(select bed_no from room, bed natural join occupies 
				where bed.type = %s and room.type = %s and end_dt is null)'''
	db.execute(sql, (bed_type, room_type, bed_type, room_type))
	if len(db.fetchall()) == 0:
		return flask.Response('Sorry, there are no free beds with the requested requirements, please try other alternatives', 200) 

	try:
		dt = datetime.now()
		start_dt = f'{dt.year}-{dt.month}-{dt.day}'
		sql = '''with free_beds(bed_no) as 
					((select bed_no from room, bed 
						where bed.type = %s and room.type = %s) 
					except 
					(select bed_no from room, bed natural join occupies 
						where bed.type = %s and room.type = %s and end_dt is null)) 
				insert into occupies select %s, min(bed_no), %s from free_beds;
				'''
		db.execute(sql, (bed_type, room_type, bed_type, room_type, pid, start_dt))
	except Exception as e:
		print(e)
		conn.rollback()
		conn.close()
		redirect(url_for('allot_beds'))
	
	conn.commit()
	conn.close()
	return redirect(url_for('allot_beds'))



