import flask
from flask import flash, g, Response, jsonify, render_template, redirect, url_for
import application
from application import default, my_jsonify
from datetime import datetime
from pandas import DataFrame

def render_add_bed():
	data = {}

	conn = application.connect()
	db = conn.cursor(cursor_factory=application.DictCursor)

	#rooms/ward
	sql = '''select room_no, type from room'''
	db.execute(sql)
	rows = db.fetchall()
	data['rooms'] = my_jsonify(rows)

	#num_beds
	sql = '''select bed_no, type, charges, room_no from bed'''
	db.execute(sql)
	rows = db.fetchall()
	data['beds'] = my_jsonify(rows)

	conn.close()

	return render_template('inventory/add_bed.html', data=data)

def handle_post(request):
	if request['action'] == 'Add':
		return add_bed(request)
	elif request['action'] == 'Delete':
		return remove_bed(request)

def add_bed(request):
	conn = application.connect()
	db = conn.cursor(cursor_factory=application.DictCursor)

	bed_no = request.get('bed_no')
	bed_type = request.get('bed_type') 
	charges = request.get('charges')
	room_no = request.get('room_no')

	db.execute(''' select * from room where room_no = %s ''', (room_no,))
	if len(db.fetchall()) == 0:
		return flask.Response('No room with the given number exists', 200)

	db.execute(''' select * from bed where bed_no = %s''', (bed_no, ))
	if len(db.fetchall()) != 0:
		return flask.Response('A bed with the given bed no already exists', 200)

	try:
		db.execute('''insert into bed values (%s,%s,%s,%s)''', 
					(bed_no, bed_type, charges, room_no));
	except Exception as e:
		print(e)
		conn.rollback()
		conn.close()
		redirect(url_for('add_bed'))
	
	conn.commit()
	conn.close()
	return redirect(url_for('add_bed'))	

def remove_bed(request):
	conn = application.connect()
	db = conn.cursor(cursor_factory=application.DictCursor)

	bed_no = request.get('bed_no')

	db.execute(''' select * from bed where bed_no = %s''', (bed_no, ))
	if len(db.fetchall()) == 0:
		return flask.Response('No bed with the given bed number exists', 200)

	try:
		db.execute('''delete from bed where bed_no = %s''',(bed_no,));
	except Exception as e:
		print(e)
		conn.rollback()
		conn.close()
		redirect(url_for('add_bed'))
	
	conn.commit()
	conn.close()
	return redirect(url_for('add_bed'))

