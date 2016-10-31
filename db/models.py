from flask_sqlalchemy import SQLAlchemy
import json
from constants import MarketType, Result, EvaluationStatus

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
    result = db.Column(db.Enum(*Result._member_names_))
    result_info = db.Column(db.String(100))
    info = db.Column(db.Text)


class Bet(db.Model, Base):
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    bet_code = db.Column(db.String)
    market_id = db.Column(db.Integer, db.ForeignKey("market.id"))
    values = db.Column(db.String)
    outcomes = db.Column(db.Text)

    def get_values(self):
        return [float(v) for v in json.loads(self.values)]

    def set_values(self, values):
        self.values = json.dumps(values)

    def get_outcomes(self):
        return json.loads(self.outcomes)

    def set_outcomes(self, values):
        self.outcomes = json.dumps(values)


class Evaluation(db.Model, Base):
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    bet_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    values = db.Column(db.String)
    outcomes = db.Column(db.Text)
    status = db.Column(db.Enum(*EvaluationStatus._member_names_),
                       default=EvaluationStatus.NEW)

    def get_values(self):
        return [float(v) for v in json.loads(self.values)]

    def set_values(self, values):
        self.values = json.dumps(values)


class Alarm(db.Model, Base):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    text = db.Column(db.Text)
    datetime = db.Column(db.DateTime)
    is_read = db.Column(db.Boolean)


class Market(db.Model, Base):
    code = db.Column(db.String)
    type = db.Column('type', db.Enum(*MarketType._member_names_))
    outcomes = db.Column(db.Text)

    def get_outcomes(self):
        return json.loads(self.outcomes)


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
