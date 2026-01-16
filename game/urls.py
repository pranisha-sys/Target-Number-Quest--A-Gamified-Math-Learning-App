from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.home, name='home'),
    path('game/', views.game, name='game'),
    path('new-game/', views.new_game, name='new_game'),
    path('check-solution/', views.check_solution, name='check_solution'),
]