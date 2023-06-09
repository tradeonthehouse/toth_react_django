from django.urls import path, include
from monthlymodel.views import StrategyModelViewSet,PositionalImageDownload,PositionalDataModelSet,StockSymbolImagesDownload,PerformanceDataViewSet
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("api/users/", include(("api.routers", "api"), namespace="api")),
    path('getstrategydata/', StrategyModelViewSet.as_view({'get': 'list'}), name='mymodel-list'),
    path('positionalimage/<int:id>/',PositionalImageDownload.as_view()),
    path('stocksymbolimage/<str:stocksymbol>/',StockSymbolImagesDownload.as_view()),
    path('getperformancedata/', PerformanceDataViewSet.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)