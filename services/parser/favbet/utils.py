import json
import datetime
import requests
from db.models import *

cookie = '__cfduid=d9d2f28b98a63cb5a1f84742d681d221a1476293546; showtime=show; _ym_uid=1476297148123869219; _pk_ref.1044.0b5f=%5B%22%22%2C%22%22%2C1476346962%2C%22https%3A%2F%2Fwww.google.com.ua%2F%22%5D; _pk_id.1044.0b5f=dbd2dc04cbe8d4fd.1476346962.1.1476346962.1476346962.; LANG=en; _ym_isad=2; _ga=GA1.2.579091414.1476293551; _gat=1; __utmt=1; __utma=117381777.579091414.1476293551.1476535026.1476538197.11; __utmb=117381777.1.10.1476538197; __utmc=117381777; __utmz=117381777.1476293551.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); PHPSESSID=82301079DF6729B3A329A6E24C; pull=94d0531a5b153274a90c687c90c24427'


def get_sports():
    sports = json.loads(
            file("./services/parser/favbet/resources/sports").read())
    sports_models = []
    for s in sports:
        sport = Sport()
        sport.id = s['sport_id']
        sport.name = s['sport_name']
        sports_models.append(sport)
    return sports_models


def get_leagues():
    leagues_structure = json.loads(
            file("./services/parser/favbet/resources/leagues").read())
    sports = leagues_structure['sports']
    leagues_models = {}
    for s in sports:
        categories = s['categories']
        for c in categories:
            leagues = c['tournaments']
            for l in leagues:
                if leagues_models.get(l['tournament_id']):
                    continue
                league = League()
                league.id = l['tournament_id']
                league.country_code = c['country_id']
                league.name = l['tournament_name']
                league.sport_id = s['sport_id']
                leagues_models[l['tournament_id']] = league
    return leagues_models.values()


def get_teams(league_id):
    headers = {
        'cookie': cookie
    }
    data = {'tournaments': '{"tournaments":[%s]}' % league_id}
    leagues_structure = json.loads(
            requests.post('https://www.favbet.com/bets/events/', data,
                          headers=headers).content)
    sports = leagues_structure['markets']
    teams_models = {}
    for s in sports:
        leagues = s['tournaments']
        for l in leagues:
            if not l.get('events'):
                continue
            for e in l['events']:
                head_market = e.get('head_market')
                if not head_market:
                    continue
                for o in head_market['outcomes']:
                    id = o.get('participant_id')
                    if id and not teams_models.get(1):
                        team = Team()
                        team.id = o['participant_id']
                        team.sport_id = s['sport_id']
                        team.name = o['participant_name']
                        teams_models[team.id] = team

    return teams_models.values()


def get_events(league_id):
    headers = {
        'cookie': cookie
    }
    data = {'tournaments': '{"tournaments":[%s]}' % league_id}
    leagues_structure = json.loads(
            requests.post('https://www.favbet.com/bets/events/', data,
                          headers=headers).content)
    sports = leagues_structure['markets']
    event_models = {}
    for s in sports:
        leagues = s['tournaments']
        for l in leagues:
            if not l.get('events'):
                continue
            for e in l['events']:
                head_market = e.get('head_market')
                if not head_market:
                    continue
                main_outcomes = head_market['outcomes']
                event = Event()
                event.id = e['event_id']
                event.name = e['event_name']
                event.date = datetime.datetime.fromtimestamp(e['event_dt'])
                o_len = len(main_outcomes)
                event.team1_id = main_outcomes[0]['participant_id']
                event.team2_id = main_outcomes[o_len - 1]['participant_id']
                event_models[event.id] = event
    return event_models.values()


def get_countries():
    leagues_structure = json.loads(
            file("./services/parser/favbet/resources/leagues").read())
    sports = leagues_structure['sports']
    countries_models = {}
    for s in sports:
        categories = s['categories']
        for c in categories:
            if countries_models.get(c['category_name']):
                continue
            country = Country()
            country.name = c['category_name']
            country.id = c['country_id']
            country.code = c['country_id']
            countries_models[country.id] = country
    return countries_models.values()


def get_events_with_results_json(date=None, sport_id=None, league_id=None,
                                 country_id=None):
    # en_page = requests.get("https://www.favbet.com/en/bets/results/")
    # cookie = en_page.headers.get('set-cookie')
    date = str(date)
    cookie = '__cfduid=d9d2f28b98a63cb5a1f84742d681d221a1476293546; showtime=show; _ym_uid=1476297148123869219; _pk_ref.1044.0b5f=%5B%22%22%2C%22%22%2C1476346962%2C%22https%3A%2F%2Fwww.google.com.ua%2F%22%5D; _pk_id.1044.0b5f=dbd2dc04cbe8d4fd.1476346962.1.1476346962.1476346962.; pull=da5eb157abd568c9f2f19e3e0429f5ed; _gat=1; __utmt=1; LANG=en; _ga=GA1.2.579091414.1476293551; __utma=117381777.579091414.1476293551.1476442613.1476518292.9; __utmb=117381777.4.10.1476518292; __utmc=117381777; __utmz=117381777.1476293551.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _ym_isad=2; PHPSESSID=FE89C638B23CEC7FEDF5AE1B6C'
    headers = {
        'cookie': cookie
    }
    data = {"date": date, "sport_id": sport_id, "category_id": country_id,
            "tournament_id": league_id}
    result = json.loads(
            requests.post("https://www.favbet.com/bets/results/filter/", data,
                          headers=headers).content)
    events = result['events']
    pages = result['pages']['paginator_next']
    for page in pages:
        data = {"date": date, "sport_id": sport_id,
                "category_id": country_id,
                "tournament_id": league_id, "page": page}
        result = json.loads(
                requests.post("https://www.favbet.com/bets/results/filter/",
                              data, headers=headers).content)
        events += result['events']
    return events


def event_results(date=None, sport_id=None, league_id=None, country_id=None):
    # en_page = requests.get("https://www.favbet.com/en/bets/results/")
    # cookie = en_page.headers.get('set-cookie')
    date = str(date)
    headers = {
        'cookie': cookie
    }
    data = {"date": date, "sport_id": sport_id, "category_id": country_id,
            "tournament_id": league_id}
    result = json.loads(
            requests.post("https://www.favbet.com/bets/results/filter/", data,
                          headers=headers).content)
    events = result['events']
    pages = result['pages']['paginator_next']
    for page in pages:
        data = {"date": date, "sport_id": sport_id,
                "category_id": country_id,
                "tournament_id": league_id, "page": page}
        result = json.loads(
                requests.post("https://www.favbet.com/bets/results/filter/",
                              data, headers=headers).content)
        events += result['events']
    results = {}
    for e in events:
        results[e['event_id']] = e['result_game_total_result_total']
    return results

# def get_results(date1, date2, sport_id=None, country_id=None,
#                      league_id=None):
#     dates = [date1 + datetime.timedelta(days=i) for i in
#              range((date2 - date1).days + 1)]
#     event_models = []
#     for date in dates:
#         events = get_events_with_results_json(date, sport_id, league_id, country_id)
#         for e in events:
#             event = Event()
#             event.date =
