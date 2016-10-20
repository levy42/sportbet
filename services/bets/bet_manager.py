from db.models import *
import constants as const


d_idef evaluate_event(user_id, event_id, bet_id, values):
    bet = Bet.query.get(bet_id)
    evaluation = Evaluation()
    evaluation.event_id = event_id
    evaluation.bet_id = bet_id
    evaluation.name = bet.name
    evaluation.user_id = user
    evaluation.set_values(values)
    db.session.create(evaluation)
    db.session.commit()

