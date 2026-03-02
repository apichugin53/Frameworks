from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


UserModel = get_user_model()


class UserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password, **kwargs)
        if not user:
            try:
                user = UserModel.objects.get(email=username)
                return super().authenticate(request, user.username, password, **kwargs)
            except UserModel.DoesNotExist:
                return None
        return user
