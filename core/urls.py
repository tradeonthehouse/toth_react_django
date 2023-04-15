from django.urls import path, include
from monthlymodel.views import StrategyModelViewSet

urlpatterns = [
    path("api/users/", include(("api.routers", "api"), namespace="api")),
    path('getstrategydata/', StrategyModelViewSet.as_view({'get': 'list'}), name='mymodel-list'),
]

