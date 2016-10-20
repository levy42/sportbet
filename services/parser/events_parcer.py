from abc import ABCMeta, abstractmethod
import os


class Parser(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_events(self, league_id):
        pass

    @abstractmethod
    def get_results(self, events_ids=None):
        pass

    @abstractmethod
    def get_last_day_results(self, leagues_ids=None):
        pass


def load_parcers():
    dirs = [x[0] for x in os.walk('./services/parser/')]
    parsers = {}
    for d in dirs:
        parser = __import__('Parser',
                            fromlist=['services', 'parser', d, 'parser'])
        parsers[d] = parser()
    return parsers


PARSERS = load_parcers()
