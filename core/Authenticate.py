from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from apps.authentication.models import User


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.filter(Q(telephone=username) | Q(email=username)).first()
        if user and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
