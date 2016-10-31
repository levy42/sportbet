from flask import request
from common import rest
from db.models import *
import json

api = rest.Rest("api", __name__)


@api.route("/events", cached=False, timeout=20)
def get_events():
    args = request.args
    return to_dict(Event.query.filter_by(**args).all()) * 10


@api.route("/sports", cached=True)
def get_sports():
    return to_dict(Sport.query.all())


@api.route("/countries")
def get_countries():
    return to_dict(Country.query.all())


@api.route("/leagues")
def get_leagues():
    args = request.args
    params = {}
    if args.get('sport_id'):
        params['sport_id'] = int(args['sport_id'])
    if args.get('country_id'):
        params['country_code'] = args['country_code']
    return to_dict(League.query.filter_by(**params).all())


@api.route("/teams")
def get_teams():
    args = request.args
    return to_dict(Team.query.filter_by(**args).all())


@api.route("/markets/<int:event_id>")
def get_markets(event_id):
    pass


@api.route("/evaluate")
def evaluate_event():
    params = request.json
    event_id = params['event_id']
    bet_id = params['bet_id']
    evaluations = json.loads(params['evaluations'])
    pass
