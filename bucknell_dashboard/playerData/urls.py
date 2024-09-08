from django.urls import path
from . import views

urlpatterns = [
    path('playerData/', views.playerData, name='playerData'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('playerData/playerDisplay/<str:name>', views.playerDisplay, name='playerDisplay')
]