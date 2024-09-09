from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.playerData, name='home'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('home/playerDisplay/<str:name>', views.playerDisplay, name='playerDisplay')
]