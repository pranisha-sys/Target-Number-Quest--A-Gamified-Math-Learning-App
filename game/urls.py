from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.home, name='home'),  # /game/
    path('login/', views.login_view, name='login'),  # /game/login/
    path('signin/', views.signin_view, name='signin'),  # /game/signin/
    path('logout/', views.logout_view, name='logout'),  # /game/logout/
    path('game/', views.game, name='game'),  # /game/game/
    path('new-game/', views.new_game, name='new_game'),  # /game/new-game/
    path('check-solution/', views.check_solution, name='check_solution'),  # /game/check-solution/
]