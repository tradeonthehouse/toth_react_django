from django.urls import path, include
from monthlymodel.views import StrategyModelViewSet,PositionalImageDownload,PositionalDataModelSet,\
    StockSymbolImagesDownload,PerformanceDataViewSet, BlogPostModelViewSet,\
        UserStrategySubscribeViewSet
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("api/users/", include(("api.routers", "api"), namespace="api")),
    path('getstrategydata/', StrategyModelViewSet.as_view({'get': 'list'}), name='mymodel-list'),
    path('positionalimage/<int:id>/',PositionalImageDownload.as_view()),
    path('stocksymbolimage/<str:stocksymbol>/',StockSymbolImagesDownload.as_view()),
    path('getperformancedata/', PerformanceDataViewSet.as_view()),
    path('content/posts/',BlogPostModelViewSet.as_view({'post': 'create', 'get': 'list_all'})),
    path('content/posts/<str:Title>/',BlogPostModelViewSet.as_view({'get': 'list'})),
    path('subscribestrategy/',UserStrategySubscribeViewSet.as_view({'post': 'create', 'get': 'list', 'delete': 'delete'}),),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)