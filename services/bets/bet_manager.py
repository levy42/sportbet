from services.parser.favbet.parcer import parcer
from db.models import *
import constants as const


def evaluate_event(user_id, event_id, bet_id, values):
    bet = Bet.query.get(bet_id)
    evaluation = Evaluation()
    evaluation.event_id = event_id
    evaluation.bet_id = bet_id
    evaluation.name = "%s %s" % (bet.bet_code, event.name)
    evaluation.user_id = user_id
    evaluation.set_values(values)


def update_events():
    pass


def update_results():
    """return list if event ID"""
    pass


def resolve_evaluations():
    pass
