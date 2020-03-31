from django.urls import path
from . import views

app_name = 'storm'

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_user, name='logout_user'),
    path('idea/submit/', views.idea_submit, name='idea_submit'),
]