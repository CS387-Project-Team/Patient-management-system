from flask import g, Response, jsonify, render_template, redirect, url_for
import application
from application import default, my_jsonify
import datetime

def get_analytics():
    data = {}
    # data about bed occupancy vs date
    cur_date = datetime.datetime.strptime('2021-01-01', '%Y-%m-%d').date() # hardcoded for now
    print(cur_date)
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    sql = '''select start_dt, count(*) as admissions from occupies
            group by start_dt
            order by start_dt'''
    db.execute(sql)
    admissions = db.fetchall()
    sql = '''select end_dt, count(*) as discharges from occupies
            where end_dt is not null
            group by end_dt
            order by end_dt'''
    db.execute(sql)
    discharges = db.fetchall()

    sql = '''select dat, count(*) as appos from meet
            where dat is not null
            group by dat
            order by dat'''
    db.execute(sql)
    appos = db.fetchall()

    sql = '''select count(*) as beds from bed
            '''
    db.execute(sql)
    total_beds = db.fetchone()
    data['daywise'] = []
    data['total_beds'] = total_beds['beds']
    occupied = 0
    admit_iter = 0
    discharge_iter = 0
    appo_iter = 0
    while True:
        daywise = {}
        daywise['date'] = cur_date.isoformat()
        if admit_iter >= len(admissions) or cur_date < admissions[admit_iter]['start_dt']:
            daywise['admissions'] = 0
        else:
            daywise['admissions'] = admissions[admit_iter]['admissions']
            admit_iter += 1
        if discharge_iter >= len(discharges) or cur_date < discharges[discharge_iter]['end_dt']:
            daywise['discharges'] = 0
        else:
            daywise['discharges'] = discharges[discharge_iter]['discharges']
            discharge_iter += 1
        if appo_iter >= len(appos) or cur_date < appos[appo_iter]['dat']:
            daywise['appos'] = 0
        else:
            daywise['appos'] = appos[appo_iter]['appos']
            appo_iter += 1
        occupied = occupied + daywise['admissions'] - daywise['discharges']
        daywise['occupied'] = occupied

        data['daywise'].append(daywise)
        cur_date += datetime.timedelta(days=1)
        if cur_date >= datetime.date.today():
            break
    
    return jsonify(data)  