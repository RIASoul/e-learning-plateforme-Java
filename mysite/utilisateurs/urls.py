from django.urls import path
from utilisateurs.views import acceuil, user_login, user_logout, register, edit_profile, change_password, profile

urlpatterns = [
    path('', acceuil, name="acceuil"),
    path('register', register, name="register"),
    path('login/', user_login, name="login"),
    path('logout', user_logout, name="logout"),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('change_password/', change_password, name='change_password'),
    path('profile/', profile, name='profile'),
]