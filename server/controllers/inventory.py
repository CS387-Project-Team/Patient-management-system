import flask
from flask import flash, g, Response, jsonify, render_template, redirect, url_for
import application
from application import default, my_jsonify
from datetime import datetime
from pandas import DataFrame

def get_inventory():
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

	return render_template('inventory/get_inventory.html',data=data)

def add_medicine(request):
	conn = application.connect()
	db = conn.cursor(cursor_factory=application.DictCursor)

	sql = '''select * from medicine where name=%s'''
	db.execute(sql,(request.get('name'),))
	row = db.fetchall()
	if(len(row)):
		return flask.Response('Medicine already exists',200)

	try:
		sql = '''select 1+max(med_id) from medicine'''
		db.execute(sql)
		new_id = db.fetchone()[0]
		# print(new_id)
		sql = '''insert into medicine values (%s,%s,%s,%s,%s)'''
		db.execute(sql,(new_id,request.get('name'),request.get('descr'),request.get('manufc'),request.get('price'),))
		conn.commit()
	except Exception as e:
		print(e)
		conn.rollback()

	conn.close()
	return redirect(url_for('get_inventory'))

def add_test(request):
	conn = application.connect()
	db = conn.cursor(cursor_factory=application.DictCursor)

	sql = '''select * from test where name=%s'''
	db.execute(sql,(request.get('name'),))
	row = db.fetchall()
	if(len(row)):
		return flask.Response('Test already exists',200)
	
	try:
		sql = '''select 1+max(test_id) from test'''
		db.execute(sql)
		new_id = db.fetchone()[0]
		sql = '''insert into test values (%s,%s,%s)'''
		db.execute(sql,(new_id,request.get('name'),request.get('charges'),))
		conn.commit()
	except Exception as e:
		print(e)
		conn.rollback()

	conn.close()
	return redirect(url_for('get_inventory'))

def add_eqp(request):
	conn = application.connect()
	db = conn.cursor(cursor_factory=application.DictCursor)
	
	try:
		sql = '''select 1+max(eqp_id) from equipment'''
		db.execute(sql)
		new_id = db.fetchone()[0]
		sql = '''insert into equipment values (%s,%s,%s,NULL)'''
		db.execute(sql,(new_id,request.get('type'),request.get('room_no'),))
		conn.commit()
		print("here4")
	except Exception as e:
		print(e)
		conn.rollback()

	conn.close()
	return redirect(url_for('get_inventory'))

def add_room(request):
	conn = application.connect()
	db = conn.cursor(cursor_factory=application.DictCursor)
	try:
		sql = '''select 1+max(room_no) from room'''
		db.execute(sql)
		new_id = db.fetchone()[0]
		sql = '''insert into room values (%s,%s)'''
		db.execute(sql,(new_id,request.get('type'),))
		conn.commit()
	except Exception as e:
		print(e)
		conn.rollback()

	conn.close()
	return redirect(url_for('get_inventory'))

def add_bed(request):
	conn = application.connect()
	db = conn.cursor(cursor_factory=application.DictCursor)

	sql = '''select 1+max(bed_no) from bed'''
	db.execute(sql)
	bed_no = db.fetchone()[0]

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
		return redirect(url_for('get_inventory'))
	
	conn.commit()
	conn.close()
	return redirect(url_for('get_inventory'))	

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
		redirect(url_for('get_inventory'))
	
	conn.commit()
	conn.close()
	return redirect(url_for('get_inventory'))

