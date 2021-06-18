"""Path file"""

from django.urls import path
from crafts import views

urlpatterns = [
    path('', views.home, name="home"),
    path('info/', views.info, name="info"),
]