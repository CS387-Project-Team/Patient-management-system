from flask import flash, g, Response, jsonify, render_template, redirect, url_for
import application
from application import default, my_jsonify
import datetime
from pandas import DataFrame

def show_dis_symp():
    if not g.is_doctor:
        return redirect(url_for('dashboard'))
    sql='''SELECT * from symptom;'''
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)

    db.execute(sql)

    rows=db.fetchall()

    data={}
    data['symptoms']=my_jsonify(rows)

    sql='''SELECT * from disease;'''
    db.execute(sql)

    rows=db.fetchall()

    data['disease']=my_jsonify(rows)

    # print(data)


    return render_template('dis_symp/showall.html',data=data)


def add_disease(request):
    if not g.is_doctor:
        return redirect(url_for('dashboard'))
    print(request)
    name=request.get('dis_name')
    info_link=request.get('info_link')

    try:
        ## check for repitition
        sql='''SELECT count(*) from disease where lower(disease_name)=lower(%s);'''
        conn = application.connect()
        db = conn.cursor(cursor_factory=application.DictCursor)

        db.execute(sql,(name,))
        if db.fetchone()[0]>0:
            flash('Disease already exists', 'danger')
            return redirect(url_for('view_dis_symp'))
        else:
            sql = '''SELECT 1+max(disease_id) as new_id
                        from disease'''
            db.execute(sql)
            row = db.fetchone()
            disease_id = row['new_id']

            sql='''INSERT into disease values(%s,%s,%s);'''
            db.execute(sql,(disease_id,name,info_link))

        conn.commit()
        conn.close()
        flash('New Disease added', 'success')

    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()

    return redirect(url_for('view_dis_symp'))



def add_symptom(request):
    if not g.is_doctor:
        return redirect(url_for('dashboard'))
    print(request)
    name=request.get('symp_name')

    try:
        ## check for repitition
        sql='''SELECT count(*) from symptom where lower(symp_name)=lower(%s);'''
        conn = application.connect()
        db = conn.cursor(cursor_factory=application.DictCursor)

        db.execute(sql,(name,))
        if db.fetchone()[0]>0:
            flash('Symptom already exists', 'danger')
            return redirect(url_for('view_dis_symp'))
        else:
            sql = '''SELECT 1+max(symp_id) as new_id
                        from symptom'''
            db.execute(sql)
            row = db.fetchone()
            symp_id = row['new_id']

            sql='''INSERT into symptom values(%s,%s);'''
            db.execute(sql,(symp_id,name))

        conn.commit()
        conn.close()
        flash('New Symptom added', 'success')

    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()

    return redirect(url_for('view_dis_symp'))








