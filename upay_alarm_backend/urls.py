from django.urls import path
from upay_alarm_backend import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('verify/', views.EmailVeriView.as_view()),
    path('locationsetup/', views.locationSetupView.as_view()),
    path('query/', views.query_surplus)
]