from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    # Home and setup pages
    path('', views.home, name='home'),
    path('avatar/', views.avatar_selection, name='avatar_selection'),
    
    # Main dashboard - shows all levels and progress
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Admin panel
    path('admin/', views.admin_panel, name='admin_panel'),
    
    # Game Levels (Sequential unlock required)
    # Level 1: Order of Numbers (25 points) - Always unlocked
    path('level/order-of-numbers/', views.order_of_numbers, name='order_of_numbers'),
    
    # Level 2: Numerals & Words (50 points) - Unlocks after Level 1
    path('level/numerals-words/', views.numerals_words, name='numerals_words'),
    
    # Level 3: Comparing Numbers (50 points) - Unlocks after Level 2
    path('level/comparing-numbers/', views.comparing_numbers, name='comparing_numbers'),
    
    # Level 4: Addition & Subtraction (50 points) - Unlocks after Level 3
    path('level/addition-subtraction/', views.addition_subtraction, name='addition_subtraction'),
    
    # Level 5: Revision Challenge (100 points) - Unlocks after Level 4
    path('level/revision-challenge/', views.revision_challenge, name='revision_challenge'),
    
    # API endpoints for AJAX requests
    path('api/complete-level/', views.complete_level, name='complete_level'),
]