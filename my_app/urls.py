from django.urls import path
from . import views

app_name = 'craiglist'
urlpatterns = [
    path('', views.home, name='home'),
]