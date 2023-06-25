from django.urls import path, include
from monthlymodel.views import StrategyModelViewSet,PositionalImageDownload
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("api/users/", include(("api.routers", "api"), namespace="api")),
    path('getstrategydata/', StrategyModelViewSet.as_view({'get': 'list'}), name='mymodel-list'),
    path('positionalimage/<int:id>/',PositionalImageDownload.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)