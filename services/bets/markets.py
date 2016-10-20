from db.models import *


def create_markets(sport_id, event):
    team1 = Team.query.get(event.team1_id)
    team2 = Team.query.get(event.team1_id)
    markets = Market.query.filter_by(sport_id=sport_id)
    bets = []
    for m in markets:
        bet = Bet()
        bet.name = "%s %s" % (m.code, event.name)
        bet.event_id = event.id
        bet.bet_code = markets.code
        bet.market_id = m.id
        outcomes = []
        for o in m.outcomes:
            if o == "1":
                outcomes.append(team1.name)
            elif o == "2":
                outcomes.append(team2.name)
            else:
                outcomes.append(o)
        bet.set_outcomes(outcomes)
        bets.append(bet)
    return bets
