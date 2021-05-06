import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import application
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = application.connect()
        db = conn.cursor(cursor_factory=application.DictCursor)
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            db.execute(
                'SELECT id FROM person WHERE username = %s',(username,)
            ) 
            if db.fetchone() is not None:
                error = 'User {} is already registered.'.format(username)
        hashed = application.bcrypt.generate_password_hash(password)
        if error is None:
            sql = 'select 1+max(id) as id from person'
            db.execute(sql)
            row = db.fetchone()
            new_id = row['id']
            sql = '''INSERT INTO person (id, name, address, pincode, contact, gender, email_id, dob, qualification, username, password)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    '''
            db.execute(
                sql, (new_id, request.form.get('name'), request.form.get('address'), request.form.get('pincode'), request.form.get('contact'), request.form.get('gender'), request.form.get('email_id'), request.form.get('dob'), request.form.get('qualification'), username, hashed.decode('UTF-8'),)
            )
            conn.commit()
            return redirect(url_for('auth.login'))
        conn.close()
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = application.connect()
        db = conn.cursor(cursor_factory=application.DictCursor)
        error = None
        db.execute(
            'SELECT * FROM person WHERE username = %s', (username,)
        )
        user = db.fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not application.bcrypt.check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        conn.close()
        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        conn = application.connect()
        db = conn.cursor(cursor_factory=application.DictCursor)
        db.execute(
            'SELECT * FROM person WHERE id = %s', (user_id,)
        )
        g.user = db.fetchone()
        db.execute('SELECT count(*) from support_staff where staff_id=%s',(user_id,))
        if db.fetchone()[0]==0:
            g.is_support=False
        else:
            g.is_support=True
        
        db.execute('SELECT count(*) from doctor where doc_id=%s',(user_id,))
        if db.fetchone()[0]==0:
            g.is_doc=False
        else:
            g.is_doc=True
        
        db.execute('SELECT count(*) from admin where id=%s',(user_id,))
        if db.fetchone()[0]==0:
            g.is_admin=False
        else:
            g.is_admin=True
        
        conn.close()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view