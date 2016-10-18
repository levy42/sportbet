from flask_sqlalchemy import SQLAlchemy, orm

db = SQLAlchemy()


# models
class Base(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)


class Sport(db.Model, Base):
    pass


class Country(db.Model, Base):
    code = db.Column(db.String, index=db.Index('code_index'))


class League(db.Model, Base):
    country_code = db.Column(db.String, db.ForeignKey("country.code"))
    sport_id = db.Column(db.Integer, db.ForeignKey("sport.id"))
    active = db.Column(db.Boolean, default=True)


class Team(db.Model, Base):
    country_code = db.Column(db.String, db.ForeignKey("country.code"))
    sport_id = db.Column(db.Integer, db.ForeignKey("sport.id"))


class Event(db.Model, Base):
    team1_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    team2_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    date = db.Column(db.DateTime)
    result = db.Column(db.Integer)
    result_info = db.Column(db.String(100))
    info = db.Column(db.Text)


class Bet(db.Model, Base):
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    user_id = db.Column(db.Integer())
    applier_id = db.Column(db.Integer)
    bet_code = db.Column(db.String)


class Market(db.Model, Base):
    code = db.Column(db.String)


class UserProfile(db.Model, Base):
    user_id = db.Column(db.Integer)
    rate = db.Column(db.Float)
    balance = db.Column(db.Integer)


def to_dict(result):
    if isinstance(result, list):
        _list = []
        for row in result:
            _list.append({x.name: getattr(row, x.name) for x in
                          row.__table__.columns})
        return _list
    else:
        return {x.name: getattr(result, x.name) for x in
                result.__table__.columns}
