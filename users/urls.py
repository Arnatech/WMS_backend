from django.urls import path
from users.views import RegisterView, LoginView, UpdateUserView, SocialLoginView

urlpatterns = [
    path('login/', LoginView.as_view(),name = 'login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('update/', UpdateUserView.as_view(), name = 'update'),
    path('social-login/', SocialLoginView.as_view(), name = 'social-login'),
]