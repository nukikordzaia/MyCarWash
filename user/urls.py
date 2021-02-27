from django.urls import path

from user.views import UserRegistrationView, LoginView, LogoutView, UserDetailView

app_name = 'user'

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', LoginView.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
    path('detail/', UserDetailView.as_view(), name='detail'),
]
