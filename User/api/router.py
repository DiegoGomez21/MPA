from django.urls import path
from User.api.views import RegisterView, UserView, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/register', RegisterView.as_view(template_name='user/register.html'), name='register'),
    path('auth/me', UserView.as_view()),
    path('auth/login', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('auth/token/refresh',TokenRefreshView.as_view())
]