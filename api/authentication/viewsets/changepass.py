from api.user.models import User
from api.authentication.serializers.changepass import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer