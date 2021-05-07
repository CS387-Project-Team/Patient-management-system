from flask import flash, g, Response, jsonify, render_template, redirect, url_for
import application
from application import default, my_jsonify
import datetime
from pandas import DataFrame

def get_tests():
    data = {}
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    # appointments and prescription
    sql = '''WITH pt(patient_id) as
                (select patient_id
                from patient
                where patient.id = %s)
            select test_id, name as test, result_file , comments, dat, patient_id
            from (takes natural join pt natural join test) as foo'''
    db.execute(sql, (g.user.get('id'),))
    rows = db.fetchall()
    data['tests'] = my_jsonify(rows)
    conn.close()
    print(data)
    return render_template('tests/tests.html', data=data)

def get_available_tests():
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    sql='''SELECT test_id, name, charges from test'''
    db.execute(sql)
    rows = db.fetchall()
    if rows == []:
        return jsonify({'msg':'No data found'})

    data={}
    data['available_tests']=[]
    for r in rows:
        data['available_tests'].append({"id":r[0], "name":r[1],"charge":float(r[2])})
    print(data)
    return render_template('tests/available_tests.html', data=data)

def confirm_booking(request):
    data = {}
    data['doctor_name'] = request.get('doctor_name')
    data['doctor_id'] = int(request.get('doctor_id'))
    data['date'] = request.get('date')
    data['time'] = request.get('time')
    return render_template('appointments/confirm_booking.html', data=data)

def book_test(request):
    print(request)
    test_id = int(request.get('test_id'))
    date = request.get('date')
    print(request)
    user_id = g.user['id']
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    try:
        if datetime.datetime.strptime(date,"%Y-%m-%d")<datetime.datetime.now():
            flash("Please select an upcoming date",'danger')
            return redirect(url_for('get_tests'))
        sql = '''SELECT 1+max(patient_id) as new_id
                        from patient'''
        db.execute(sql)
        row = db.fetchone()
        patient_id = row['new_id']
        sql = '''INSERT into patient(id, patient_id)
                values (%s, %s);'''
        db.execute(sql, (user_id, patient_id,))

        sql='''INSERT into takes(patient_id, test_id, dat)
                values(%s,%s,%s);'''
        db.execute(sql,(patient_id, test_id,date))

        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
        return jsonify({'status':'Failed to book a new test', 'code':401})    
    flash('Diagnostic test booked successfully!', 'success')
    return redirect(url_for('get_tests'))


def cancel_test(request):
    test_id = int(request.get('test_id'))
    date=request.get('date')
    patient_id=int(request.get('pat_id'))
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    try:
        
        sql = '''DELETE from takes where
                    test_id=%s and
                    dat=%s and 
                    patient_id = %s;'''
        db.execute(sql, (test_id,date,patient_id))
        # deleted_test = db.fetchone() 
        if db.rowcount==0:
            raise Exception('no appointment deleted')
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
        return jsonify({'status':'Failed to cancel appointment', 'code':401})    
    flash('Apoointment cancelled successfully!', 'danger')
    return redirect(url_for('get_tests'))

    