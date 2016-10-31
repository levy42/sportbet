from services.parser import events_parcer
from main import app
from db.models import *
from sqlalchemy import update
import constants as c
from services.bets.markets import create_markets

parser_name = app.config.get('parser', 'favbet')
parser = events_parcer.PARSERS[parser_name]


def update_results():
    leagues_ids = _get_leagues_ids()
    today_results = parser.get_last_day_results(leagues_ids)
    for event_id, result in today_results.items():
        main, full = parse_result(result)
        update(Event).where(Event.id == event_id).values(result=main,
                                                         result_info=full)
        resolve_evaluations(event_id)


def update_events():
    leagues = League.query.filter_by(active=True).all()
    for league, leagues.id in leagues:
        try:
            events = parser.get_events(id)
            for e in events:
                event = Event.query.get(e.id)
                if not event:
                    db.session.create(e)
                    bets = create_markets(league.sport_id, e)
                    for b in bets:
                        db.session.create(b)
            db.session.commit()
        except Exception as e:
            print(e)


def resolve_evaluations(event_id):
    pass


def clean_events():
    pass


def _get_leagues_ids():
    leagues = League.query.filter_by(active=True).all()
    return [l.id for l in leagues]


def parse_result(result):
    main_score = result.split(' ')[0]
    a, b = main_score.split(':')
    if a > b:
        return c.HOME_WIN, result
    elif a < b:
        return c.AWAY_WIN, result
    else:
        return c.DRAW, result
