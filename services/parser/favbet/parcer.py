from services.parser import events_parcer
import utils


class Parser(events_parcer.Parser):
    def get_events(self, leagues_ids=None, datetime=None):
        pass

    def get_results(self, events_ids=None):
        pass

    def get_last_day_results(self, leagues_ids=None):
        if not leagues_ids:
            mapped_results = {}
            results = utils.event_results()
            for r in results.keys():
                mapped_results[self._team_in_id(r)] = results[r]
        else:
            raise NotImplementedError

    def get_event(self, id):
        pass

    def _team_in_id(self, external_id):
        return external_id

    def _team_ex_id(self, internal_id):
        return internal_id

    def _league_in_id(self, external_id):
        return external_id

    def _league_ex_id(self, internal_id):
        return internal_id


parcer = Parser()
