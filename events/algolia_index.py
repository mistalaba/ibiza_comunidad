from algoliasearch_django import AlgoliaIndex

class EventIndex(AlgoliaIndex):
    fields = (
        'title', 'description', 'created_by', 'get_absolute_url',
        'start_datetime', 'end_datetime', 'algolia_photo_url', 'algolia_photo_url_medium',
        'price', 'location_friendly_name'
    )
    # geo_field = 'location'
    settings = {
        'searchableAttributes': ['title', 'description', 'created_by'],
        'attributesForFaceting': ['created_by']
    }
    index_name = 'Event'
