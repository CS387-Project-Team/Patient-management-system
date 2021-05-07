from flask import flash, g, Response, jsonify, render_template, redirect, url_for
import application
from application import default, my_jsonify
import datetime
from pandas import DataFrame

def show_slots():
    if not g.is_admin:
        return redirect(url_for('dashboard'))

    sql='''SELECT name, doc_id, room_no, dat, start_time from
            (doctor_room_slot natural inner join doctor), person where
            doc_id=id
            order by dat, start_time, room_no;'''

    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)

    db.execute(sql)
    data={}
    data['slots']=my_jsonify(db.fetchall())

    return render_template('/assign_room/all_slots.html',data=data)

def edit_slot(request):
    if not g.is_admin:
        return redirect(url_for('dashboard'))

    doc_id=int(request.get('doc_id'))
    date=request.get('date')
    start_time=request.get('start_time')
    room_no=int(request.get('room_no'))

    try:
        if datetime.datetime.strptime(date,"%Y-%m-%d")<datetime.datetime.now():
            flash("Please edit for an upcoming date",'danger')
            return redirect(url_for('assign_room'))

        sql='''SELECT count(*) from doctor_room_slot where
                start_time=%s and
                dat=%s and
                room_no=%s;'''

        conn = application.connect()
        db = conn.cursor(cursor_factory=application.DictCursor)

        db.execute(sql,(start_time,date,room_no,))

        if db.fetchone()[0]!=0:
            flash('Chosen room no is conflicting','danger')
            return redirect(url_for('assign_room'))

        sql='''UPDATE doctor_room_slot
                set room_no=%s where
                doc_id=%s and
                dat=%s and
                start_time=%s;'''
        db.execute(sql,(room_no,doc_id,date,start_time))

        flash('Room no changed successfully','success')

        conn.commit()
        conn.close()


    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
    return redirect(url_for('assign_room'))


