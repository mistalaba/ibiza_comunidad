from algoliasearch_django import AlgoliaIndex

class EventIndex(AlgoliaIndex):
    fields = ('title', 'description', 'created_by')
    # geo_field = 'location'
    settings = {
        'searchableAttributes': ['title', 'description', 'created_by'],
        'attributesForFaceting': ['created_by']
    }
    index_name = 'Event'
