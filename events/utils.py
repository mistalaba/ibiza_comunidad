import facebook


def get_facebook_events():
    """
    https://developers.facebook.com/tools/explorer/145634995501895/?method=GET&path=20498816064%2Fevents%3Ffields%3Dend_time%2Cstart_time%2Cname%26since%3D2017-12-10%26until%3D2018-01-01&version=v2.5
    """
    # TODO: Save this to the db
    access_token = 'EAANf8JBWOggBAEfykLqQZCl4JlGuRXlhwT7mwgrZCT2ZCKXiZAS8yLKmIMkw6LFHORq1l6in7jezTbgZC0cnWLFEJfKY8kNj8WL98KD4WSZBeZCDIXeVLeiLwX9lkr56s8sa9cXAZAFGDMSqwxQQpngJuX8p7K4vXqeH5ZBCrPbkB8faO5IH2NZB0ZCJqxRLMIb3rgZD'
    graph = facebook.GraphAPI(access_token=access_token, version="2.5")

    # Get events from Ibiza Winter Residents
    events_json = graph.request('20498816064/events?fields=cover,description,end_time,start_time,name,place')

    event_list = []
    for event in events_json['data']:
        cover = event.get('cover')
        cover_url = ''
        if cover:
            cover_url = cover['source']
        current_event = {
            'name': event['name'],
            'description': event.get('description'),
            'start_datetime': event.get('start_time'),
            'end_datetime': event.get('end_time'),
            'photo': cover_url,
        }
        event_list.append(current_event)
    return event_list

