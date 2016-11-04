import os.path as op
import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy, Model
from flask_admin import Admin
from flask_admin.contrib.sqlamodel import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from common.rest import Rest

api = Rest("api", __name__)
app = Flask(__name__)
app.config.from_pyfile('app.conf')
app.register_blueprint(api)
db = SQLAlchemy(app)
admin = Admin(app)


class Base(object):
    column_searchable_list = ('id', 'name')
    id = db.Column(db.Integer, autoincrement=True)
    name = db.Column(db.String)


class Sport(Base, Model):
    pass


class OutcomeType(Base, Model):
    code = db.Column(db.String)
    full_code = db.Column(db.String)
    sport_id = db.Column(db.Integer)


# admin.add_view(ModelView(OutcomeType, db.session))
# admin.add_view(ModelView(Sport), db.session)
# path = op.join(op.dirname(__file__), 'static')
# admin.add_view(FileAdmin(path, '/static/', name='Models'))
#
models = {}


def _hash(p1, p2, range1, range2):
    return p1 * range2 + p2 if range1 > range2 else p2 * range1 + p1


def _calculate(model_id, input_params):
    m = models[model_id]
    h_params = {}
    for i, v in enumerate(input_params):
        h_params[i] = ((m['params'][i]['map'][v], m['params'][i]['range']))
    outcomes = []
    for i in m['stage1']:
        t = m['stage1'][i]
        print t
        if len(t['params']) == 1:
            hash_i = input_params
        else:
            hash_i = _hash(h_params[t['params'][0]][0],
                           h_params[t['params'][1]][0],
                           h_params[t['params'][0]][0],
                           h_params[t['params'][1]][0])
        o_type = t['outcome_type']
        v = t['values'][hash_i]
        outcomes.append({'value': v, 'parameter': o_type['parameter'],
                         'name': o_type['name'], 'id': o_type['id']})
        if t['out_param']:
            h_params[t['out_param']['id']] = t['out_param']['map'][v]
    for i in models[id]['stage2']:
        t = m['stage1'][i]
        if len(t['params']) == 1:
            hash_i = input_params
        else:
            hash_i = _hash(h_params[t['params'][0]][0],
                           h_params[t['params'][1]][0],
                           h_params[t['params'][0]][0],
                           h_params[t['params'][1]][0])
        o_type = t['outcome_type']
        v = t.values[hash_i]
        outcomes.append({'value': v, 'p': o_type['p'],
                         'name': o_type['name'], 'id': o_type['id']})
    return outcomes


@api.route("/sports")
def get_sports():
    return Sport.query.all()


@api.route("/outcomes")
def get_outcome_types():
    return OutcomeType.query.all()


@api.route("/caclulate/<int:id>")
def calculate(id):
    return _calculate(id, request.args)


@api.route("load/<name>")
def add_model(name):
    model = json.loads(file("models/" + name).read())
    models[model['id']] = model


@api.route("free/<id>")
def del_model(id):
    del models[id]


model = json.loads(file("models/" + "fake_model").read())
models[model['id']] = model
print _calculate(1, ["1"])
