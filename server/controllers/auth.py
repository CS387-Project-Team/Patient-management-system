import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import application
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = application.connect()
        db = conn.cursor()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            db.execute(
                'SELECT id FROM login WHERE username = %s',(username,)
            ) 
            if db.fetchone() is not None:
                error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO login (username, password) VALUES (%s, %s)',
                (username, generate_password_hash(password),)
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
        db = conn.cursor()
        error = None
        db.execute(
            'SELECT * FROM login WHERE username = %s', (username,)
        )
        user = db.fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('hello'))
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
        db = conn.cursor()
        db.execute(
            'SELECT * FROM login WHERE id = %s', (user_id,)
        )
        g.user = db.fetchone()
        conn.close()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.register'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view