from flask import request
from common import rest
from db.models import *

api = rest.Rest("api", __name__)


@api.route("/events")
def get_events():
    args = request.args
    return to_dict(Event.query.filter_by(**args).all())


@api.route("/sports")
def get_sports():
    return to_dict(Sport.query.all())


@api.route("/countries")
def get_countries():
    return to_dict(Country.query.all())


@api.route("/leagues", cached=True, timeout=50)
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
