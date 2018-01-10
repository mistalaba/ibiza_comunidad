from django.apps import AppConfig
import algoliasearch_django as algoliasearch

from .algolia_index import EventIndex

class EventsConfig(AppConfig):
    name = 'events'

    def ready(self):
        Event = self.get_model('Event')
        algoliasearch.register(Event, EventIndex)
