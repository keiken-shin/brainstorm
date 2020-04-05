from django.urls import path
from . import views

app_name = 'storm'

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('idea/<int:id>/', views.idea, name='idea'),
    path('logout/', views.logout_user, name='logout_user'),
    path('idea/form/', views.idea_form, name='idea_form'),
    path('idea/submit/', views.idea_submit, name='idea_submit'),
    path('selection/<int:id>/', views.selection, name="selection"),
    path('jury', views.jury, name='jury'),
]