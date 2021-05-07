from flask import flash, g, Response, jsonify, render_template, redirect, url_for
import application
from application import default, my_jsonify
import datetime
from pandas import DataFrame

def show_all():
    if not g.is_doctor:
        return redirect(url_for('dashboard'))
    user_id = g.user['id']

    # the day of the week
    week_day=datetime.datetime.now().isocalendar()[2]

    # list of dates remaining in current week
    dates=[str((datetime.datetime.now() + datetime.timedelta(days=i)).date()) for i in range(1,8-week_day)]

    start_time=datetime.datetime.strptime("00:00","%H:%M")
    time_generated=[start_time+datetime.timedelta(minutes=i*30) for i in range(48)]

    data={}
    data['slots']={}

    for d in dates:
        data['slots'][d]={}
        for t in time_generated:
            data['slots'][d][t.strftime("%H:%M")]=0

    dates_list=""
    for i in range(len(dates)):
        dates_list+='\''+dates[i]+'\''
        if i!=len(dates)-1:
            dates_list+=","

    sql='''SELECT dat, start_time from doctor_room_slot as drs where
            dat in ('''+dates_list+''') and
            not exists 
                (select * from (meet natural inner join doctor_room_slot) as i
                    where i.dat=drs.dat and i.start_time=drs.start_time and i.doc_id=drs.doc_id) and
            drs.doc_id=%s;'''

    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)

    db.execute(sql,(user_id,))

    available_slots=db.fetchall()

    sql='''SELECT dat,start_time from meet where
            dat in ('''+dates_list+") and doc_id=%s;"

    db.execute(sql,(user_id,))
    booked_slots=db.fetchall()

    for free_slot in available_slots:
        data['slots'][str(free_slot[0])][free_slot[1].strftime("%H:%M")]=1

    for booked_slot in booked_slots:
        data['slots'][str(booked_slot[0])][booked_slot[1].strftime("%H:%M")]=2

    print(data)

    return render_template('/doc_slots/viewall.html',data=data)

def change(request):
    if not g.is_doctor:
        return redirect(url_for('dashboard'))
    date=request.get('date')
    time=request.get('time')
    status=int(request.get('status'))

    user_id = g.user['id']

    if status==0:
        sql='''INSERT into doctor_room_slot(doc_id,dat,start_time) 
                values(%s,%s,%s);'''
    else:
        sql='''DELETE from doctor_room_slot where doc_id=%s and dat=%s and start_time=%s;'''

    try:
        conn = application.connect()
        db = conn.cursor(cursor_factory=application.DictCursor)

        db.execute("INSERT INTO slot values(%s,%s) on conflict do nothing;",(date,time))
        db.execute(sql,(user_id,date,time))
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()

    return redirect(url_for('get_week_slots'))




    

