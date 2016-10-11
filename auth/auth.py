import datetime
from functools import wraps
import uuid

from flask import request, session, g
from flask_bcrypt import Bcrypt

from common import rest
from db.models import db

auth = rest.Rest('auth', __name__)
app = None
bcrypt = None


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, id, username, password, admin=False):
        self.id = id
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.email)


def init_app(current_app):
    global app
    global bcrypt
    app = current_app
    bcrypt = Bcrypt(app)


def get_user(id):
    pass


@auth.before_request
def before_request():
    if not (session.get('token') and session.get('user_id')):
        token = generate_token()
        session['token'] = token
        session['user_id'] = token
        session['username'] = 'Anonymous'
        g.user_id = token
    else:
        g.user_id = session.get('user_id')
        g.username = session.get('username')


def auth_context(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('token'):
            token = generate_token()
            session['token'] = token
            session['user_id'] = token
            session['username'] = 'Anonymous'
            g.user_id = token
        else:
            g.user_id = session.get('user_id')
            g.username = session.get('username')
        return func(*args, **kwargs)

    return wrapper


@auth.route('/register', methods=['POST'])
def register():
    json_data = request.json or request.form
    username = json_data['username']
    password = json_data['password']
    user = User(
            id=generate_token(),
            username=username,
            password=password
    )
    if User.query.filter_by(username=username).first():
        raise Exception('User with name %s is already registered' % username)
    try:
        db.session.add(user)
        db.session.commit()
        session['logged_in'] = True
        session['token'] = generate_token()
        session['user_id'] = user.id
        db.session.close()
    except Exception as e:
        db.session.close()
        raise e


@auth.route('/login', methods=['POST'])
def login():
    json_data = request.json or request.form
    user = User.query.filter_by(username=json_data['username']).first()
    if user and bcrypt.check_password_hash(
            user.password, json_data['password']):
        session['logged_in'] = True
        session['token'] = generate_token()
        session['username'] = user.username
        session['user_id'] = user.id
        print('a')
    else:
        raise Exception("Invalid username of password")


@auth.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('token', None)


@auth.route('/status')
def status():
    if session.get('logged_in'):
        return {'status': True, 'user_id': session.get('user_id')}
    else:
        return {'status': False}


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            raise Exception("Login required")
        user = User.query.get(user_id)
        if not user:
            raise Exception("Login required")
        return func(*args, **kwargs)

    return wrapper


def generate_token():
    return str(uuid.uuid4())
