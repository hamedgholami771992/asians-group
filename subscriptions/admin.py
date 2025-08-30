from django.contrib import admin
from .models import Feature, Plan, Subscription


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    filter_horizontal = ("features",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "plan", "start_date", "is_active")
    list_filter = ("is_active", "plan")
