from django.urls import path

from .views import (
    AuthUserRegistrationView,
    UserView,
)

urlpatterns = [
    path('register', AuthUserRegistrationView.as_view(), name='register'),
    path('user', UserView.as_view(), name='user')
]
