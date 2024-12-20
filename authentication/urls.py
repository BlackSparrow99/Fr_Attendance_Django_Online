from django.urls import path
from . import views


urlpatterns = [
    path("login", views.login_user, name="login"),
    path("delete-users", views.delete_users, name="delete_users"),
    path("register", views.register, name="register"),
    path("logout-user", views.logout_user, name="logout_user"),
    path("activate-user/<uidb64>/<token>", views.activate_user, name="activate"),
    path("login-user", views.profile_view, name="user_name"),
    path("user_privileges", views.admin_check_view, name="user_state"),
    path("resend-authentication", views.resend_authentication, name="resend_authentication"),
]
