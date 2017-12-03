from django.db import models
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    class Meta:
        verbose_name_plural = _("Categories")

    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Subscriber(models.Model):
    class Meta:
        verbose_name_plural = _("Subscribers")

    email = models.EmailField(unique=True)
    subscriptions = models.ManyToManyField(Category)

    def __str__(self):
        return self.email
