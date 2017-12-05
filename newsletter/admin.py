from django.contrib import admin

from .models import Subscriber, Category

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
