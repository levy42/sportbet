from services.parser import events_parcer
from flask_template import app
from db.models import *
from sqlalchemy import update
import constants as c

parser_name = app.config.get('parser', 'favbet')
parser = events_parcer.PARSERS[parser_name]


def update_results():
    today_results = parser.get_last_day_results()
    for r in today_results:
        full_result = today_results[r]
        result = parse_result(full_result)
        update(Event).where(Event.id == r).values(result=result,
                                                  result_info=full_result)


def update_events():
    pass


def clean_events():
    pass


def get_leagues_ids():
    leagues = League.query.filter_by(active=True)


def parse_result(result):
    main_score = result.split(' ')[0]
    a, b = main_score.split(':')
    if a > b:
        return c.HOME_WIN
    elif a < b:
        return c.AWAY_WIN
    elif:
        return c.DRAW
