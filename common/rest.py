from functools import wraps
from flask import Blueprint, jsonify, make_response


class Rest(Blueprint):
    def route(self, rule, **options):
        """Like :meth:`Flask.route` but for a blueprint.  The endpoint for the
        :func:`url_for` function is prefixed with the name of the blueprint.
        """

        def decorator(f):
            decorated_rule = rule
            endpoint = options.pop("endpoint", f.__name__)
            self.add_url_rule(decorated_rule, endpoint, self.rest(f),
                              **options)
            return f

        return decorator

    def rest(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                data = func(*args, **kwargs)
                if data is None:
                    return make_response()
                if isinstance(data, (dict, list, tuple, set)):
                    return jsonify(data)
                else:
                    return jsonify(data.__dict__)
            except Exception as e:
                res = make_response()
                res.data = str(e)
                res.status = '201'
                return res

        return wrapper
