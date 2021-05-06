from flask import flash, g, Response, jsonify, render_template, redirect, url_for
import application
from application import default, my_jsonify
import datetime
from pandas import DataFrame

def show_tests():
    user_id = g.user['id']
    sql='''SELECT patient.patient_id as pid, person.name as pname, takes.test_id as tid, test.name as test, result_file, comments, dat from 
            handle, equipment, takes, test,person, patient  where
            handle.eqp_id=equipment.eqp_id and
            equipment.test_id=test.test_id and
            test.test_id=takes.test_id and
            handle.staff_id= %s and
            takes.patient_id=patient.patient_id and
            patient.id=person.id
            order by dat desc;'''

    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)

    db.execute(sql,(user_id,))
    compatible_tests=db.fetchall()
    data={}
    data["administer_test"]=my_jsonify(compatible_tests)
    return render_template('tests/administer_test.html',data=data)

def edit_test(request):
    print(request)
    pid=request.get('pat_id')
    tid=request.get('test_id')
    date=request.get('date')
    result_file=request.get('rfile')
    comments=request.get('comments')

    try:
        sql='''UPDATE takes
                set result_file=%s, comments=%s
                where
                patient_id=%s and
                test_id=%s and
                dat=%s;'''

        conn = application.connect()
        db = conn.cursor(cursor_factory=application.DictCursor)

        db.execute(sql,(result_file,comments,pid,tid,date))
        if db.rowcount!=1:
            raise Exception('rows changed: '+str(db.rowcount))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
        return jsonify({'status':'Failed to edit test', 'code':401})    
    flash('Test editted successfully!', 'success')
    return redirect(url_for('administer_test'))




