from flask.ext.script import Manager
from main import app
from db.models import db
from db.models import *
from services.parser.favbet import utils

manager = Manager(app)


@manager.command
def initdb():
    """Creates all database tables."""
    db.create_all()


@manager.command
def dropdb():
    """Drops all database tables."""
    db.drop_all()


@manager.command
def create_sports():
    sports = utils.get_sports()
    for s in sports:
        db.session.add(s)
    db.session.commit()


@manager.command
def create_countries():
    countries = utils.get_countries()
    for c in countries:
        db.session.add(c)
    db.session.commit()


@manager.command
def create_teams():
    leagues_ids = [l.id for l in League.query.all()]
    for id in leagues_ids:
        teams = utils.get_teams(id)
        for m in teams:
            db.session.merge(m)
        db.session.commit()


@manager.command
def create_leagues():
    leagues = utils.get_leagues()
    for l in leagues:
        db.session.add(l)
    db.session.commit()


@manager.command
def create_events():
    leagues_ids = [l.id for l in League.query.all()]
    for id in leagues_ids:
        try:
            events = utils.get_events(id)
            for e in events:
                db.session.merge(e)
            db.session.commit()
        except Exception as e:
            print(e)

def create_market():
    import constants
    market = Market()
    market.code = '1X2'
    market.name = 'Winner'
    market.outcomes_string  ='[1,X,2]'
    market.type = constants.MarketType.COEFFICIENT
    db.session



if __name__ == '__main__':
    manager.run()
