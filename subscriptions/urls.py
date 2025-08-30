from django.urls import path, include
from rest_framework.routers import DefaultRouter
from subscriptions.views import PlanViewSet, SubscriptionViewSet
from subscriptions.views.feature import FeatureViewSet


app_name = "subscriptions" 

router = DefaultRouter()
router.register("plans", PlanViewSet, basename="plan")
router.register("features", FeatureViewSet, basename="feature")
router.register("subscriptions", SubscriptionViewSet, basename="subscription")

urlpatterns = [
    path("", include(router.urls)),
]
