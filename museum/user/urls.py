from django.urls import path
from .views import (
    login,
    logout,
    UserRegistrationView,
    UserProfileView,
    EmailVerificationView,
    basket_view,
)
from django.contrib.auth.decorators import login_required

app_name = "user"

urlpatterns = [
    path("login/", login, name="login"),
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path("logout", logout, name="logout"),
    path(
        "profile/<int:pk>/", login_required(UserProfileView.as_view()), name="profile"
    ),
    path(
        "verify/<str:email>/<uuid:code>/",
        EmailVerificationView.as_view(),
        name="email_verification",
    ),
    path("basket/", basket_view, name="basket"),
]
