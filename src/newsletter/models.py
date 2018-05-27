from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from anymail.signals import tracking

import logging
logger = logging.getLogger(__name__)


class Category(models.Model):
    class Meta:
        verbose_name_plural = _("Categories")

    title = models.CharField(max_length=200)
    tag = models.CharField(max_length=50)
    mailchimp_list_id = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Subscriber(models.Model):
    class Meta:
        verbose_name_plural = _("Subscribers")

    email = models.EmailField(unique=True)
    subscriptions = models.ManyToManyField(Category, through='Subscription')

    def __str__(self):
        return self.email

class Subscription(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)

    def __str__(self):
        return "{}: {} - {}".format(self.subscriber, self.category, self.status)


@receiver(tracking)
def handle_unsubscribe(sender, event, esp_name, **kwargs):
    logger.debug("Incoming webhook: {}".format(event))
    if event.event_type == 'unsubscribed':
        tags = event.tags
        subscriber = Subscriber.objects.get(email=event.recipient)
        for tag in tags:
            category = Category.objects.get(tag=tag)
            subscriber.subscriptions.remove(category)
            logger.info("{} unsubscribed from '{}'".format(event.recipient, tag))
