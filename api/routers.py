from api.authentication.viewsets import (
    RegisterViewSet,
    LoginViewSet,
    ActiveSessionViewSet,
    LogoutViewSet,
    
)
from monthlymodel.views import UploadFileViewSet
from monthlymodel.views import BrokerModelViewSet
from monthlymodel.views import StrategyModelViewSet,PositionalDataModelSet
from rest_framework import routers
from api.user.viewsets import UserViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register(r"edit", UserViewSet, basename="user-edit")

router.register(r"register", RegisterViewSet, basename="register")

router.register(r"login", LoginViewSet, basename="login")

router.register(r"checkSession", ActiveSessionViewSet, basename="check-session")

router.register(r"logout", LogoutViewSet, basename="logout")

router.register(r"uploadmonthlymodel", UploadFileViewSet, basename="uploadmonthlymodel")

router.register(r"addbroker", BrokerModelViewSet, basename="addbroker")

router.register(r"getstrategydata", StrategyModelViewSet, basename="getstrategydata")

router.register(r"getpositionaldata", PositionalDataModelSet, basename="getpositionaldata")

urlpatterns = [
    *router.urls,
]
