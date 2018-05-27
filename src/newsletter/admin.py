from django.contrib import admin

from .models import Subscriber, Category, Subscription

class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 1

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    inlines = [SubscriptionInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'category', 'status']
    list_filter = ['status', 'category']
