import requests

from django.conf import settings
from django.utils.text import slugify

import logging
logger = logging.getLogger(__name__)


def slugify_unique(instance, field_to_slugify):
    """
    Idea taken from http://fazle.me/auto-generating-unique-slug-in-django/
    """
    model = instance._meta.model
    base_slug = slugify(getattr(instance, field_to_slugify))
    # Continue the slugification
    unique_slug = base_slug
    num = 1
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = '{}-{}'.format(slug, num)
        num += 1
    return unique_slug

def update_webhook_urls(protocol='https', new_base_url='beta.comunidadibiza.es'):
    """
    protocol: http or https
    The original url is
    https://VzhoWuZaXCqbA6Nn:mH4hMjin8XIovNai@beta.comunidadibiza.es/anymail/mailgun/tracking/

    The ngrok url changes, but is in the format of a7fd6bc8.ngrok.io
    """
    api_key = settings.ANYMAIL['MAILGUN_API_KEY']
    sender_domain = settings.ANYMAIL['MAILGUN_SENDER_DOMAIN']
    webhook_authorization = settings.ANYMAIL['WEBHOOK_AUTHORIZATION']
    webhooks = [
        # 'bounce',
        # 'deliver',
        # 'drop',
        # 'spam',
        'unsubscribe',
        # 'click',
        # 'open'
    ]
    new_url = '{}://{}@{}/anymail/mailgun/tracking/'.format(
        protocol, webhook_authorization, new_base_url
    )
    for webhook_id in webhooks:
        requests.put(
            ("https://api.mailgun.net/v3/domains/{}/webhooks/{}".format(sender_domain, webhook_id)),
            auth=('api', api_key),
            data={'url': new_url})
        print("{}: {} has been updated with {}.".format(sender_domain, webhook_id, new_url))


def remove_unsubscribe(email, tag='*'):
    api_key = settings.ANYMAIL['MAILGUN_API_KEY']
    sender_domain = settings.ANYMAIL['MAILGUN_SENDER_DOMAIN']
    result = requests.delete(
        "https://api.mailgun.net/v3/{}/unsubscribes/{}".format(sender_domain, email),
        auth=("api", api_key),
        data={'tag': tag}
        )
    logger.info("Response: {}".format(result.text))
    return result
