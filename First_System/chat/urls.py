from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('delete_user/<str:username>/', views.delete_user, name='delete_user'),
    path('<str:room_name>/', views.room, name='room'),
]