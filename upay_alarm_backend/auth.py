from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from upay_alarm_backend.models import UserProfile


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception as e:
            return None