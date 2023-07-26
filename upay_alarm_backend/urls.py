from django.urls import path
from upay_alarm_backend.views import RegisterUserView, LoginView, LogoutView, EmailVeriView

urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('verify/', EmailVeriView.as_view())
]