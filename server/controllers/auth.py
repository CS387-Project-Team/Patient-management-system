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
            db.execute(
                "INSERT INTO person (username, password) VALUES (%s, %s)",
                (username, hashed.decode('UTF-8'),)
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
        db = conn.cursor(cursor_factory=application.DictCursor)
        db.execute(
            'SELECT * FROM person WHERE id = %s', (user_id,)
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