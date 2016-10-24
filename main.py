from flask import Flask, render_template
from flask_admin import Admin

from api import api
from db import models
from auth import auth
from common import cache
from admin import admin

app = Flask(__name__)
app.config.from_pyfile('app.conf')
cache.cache.init_app(app)
# db init
models.db.init_app(app)
# init API
app.register_blueprint(api.api)
# auth init
auth.init_app(app)
app.register_blueprint(auth.auth, url_prefix='/auth')
admin.init_app(app)


@app.route('/')
@app.route('/login', methods=['GET'])
@app.route('/register', methods=['GET'])
@app.route('/logout', methods=['GET'])
def home():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
