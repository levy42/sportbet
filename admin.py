import inspect
import os.path as op
from flask_admin import Admin
from flask_admin.contrib.sqlamodel import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
import db.models as models

admin = Admin(name='admin')


def get_columns(cls):
    column_list = [x for x in cls.__table__.columns]
    result = []
    for column in column_list:
        result.append(column.name)
    return result


def create_model_view(cls, session):
    custom_class = ModelView
    custom_class.column_filters = tuple(get_columns(cls))
    custom_class.column_searchable_list = ('id', 'name')
    model_view = custom_class(cls, session)
    return model_view


for name, obj in inspect.getmembers(models):
    if inspect.isclass(obj):
        if obj is not models.Base and issubclass(obj, models.Base):
            admin.add_view(create_model_view(obj, models.db.session))

path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
