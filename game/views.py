from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    """Home page view for Target Number Quest"""
    return render(request, 'game/home.html')

def admin_panel(request):
    """Admin panel view"""
    if not request.session.get('is_admin', False):
        pass
    return render(request, 'game/admin_panel.html')

def avatar_selection(request):
    """Avatar selection page view"""
    if request.method == 'POST':
        player_name = request.POST.get('player_name')
        avatar_type = request.POST.get('avatar_type')
        avatar_choice = request.POST.get('avatar_choice')
        buddy_name = request.POST.get('buddy_name')
        
        request.session['player_name'] = player_name
        request.session['avatar_type'] = avatar_type
        request.session['avatar_choice'] = avatar_choice
        request.session['buddy_name'] = buddy_name
        
        # Initialize game progress with proper structure
        request.session['game_progress'] = {
            'current_level': 'order_of_numbers',
            'levels_completed': [],
            'points_today': 0,
            'total_points': 0,
            'total_questions_answered': 0,
            'correct_answers': 0,
            # Points per level
            'level_points': {
                'order_of_numbers': 0,
                'numerals_words': 0,
                'comparing_numbers': 0,
                'addition_subtraction': 0,
                'revision_challenge': 0
            }
        }
        
        return redirect('game:dashboard')
    
    player_name = request.GET.get('name', request.session.get('player_name', ''))
    return render(request, 'game/avatar_selection.html', {'player_name': player_name})

def check_session(request):
    """Helper function to check if user has valid session"""
    return 'player_name' in request.session

def get_player_context(request):
    """Helper function to get common player context"""
    return {
        'player_name': request.session.get('player_name', 'Player'),
        'buddy_name': request.session.get('buddy_name', 'Buddy'),
        'avatar_choice': request.session.get('avatar_choice', '🐱'),
        'game_progress': request.session.get('game_progress', {})
    }

def dashboard(request):
    """Game dashboard view - shows all levels and progress"""
    if not check_session(request):
        return redirect('game:home')
    
    context = get_player_context(request)
    game_progress = context['game_progress']
    
    # Calculate statistics
    completed_levels = game_progress.get('levels_completed', [])
    total_levels = 5
    levels_completed_count = len(completed_levels)
    progress_percentage = int((levels_completed_count / total_levels) * 100)
    
    # Define level unlock logic with points structure
    levels_info = {
        'order_of_numbers': {
            'unlocked': True,
            'completed': 'order_of_numbers' in completed_levels,
            'points': 25,
            'earned_points': game_progress.get('level_points', {}).get('order_of_numbers', 0)
        },
        'numerals_words': {
            'unlocked': 'order_of_numbers' in completed_levels,
            'completed': 'numerals_words' in completed_levels,
            'points': 50,
            'earned_points': game_progress.get('level_points', {}).get('numerals_words', 0)
        },
        'comparing_numbers': {
            'unlocked': 'numerals_words' in completed_levels,
            'completed': 'comparing_numbers' in completed_levels,
            'points': 50,
            'earned_points': game_progress.get('level_points', {}).get('comparing_numbers', 0)
        },
        'addition_subtraction': {
            'unlocked': 'comparing_numbers' in completed_levels,
            'completed': 'addition_subtraction' in completed_levels,
            'points': 50,
            'earned_points': game_progress.get('level_points', {}).get('addition_subtraction', 0)
        },
        'revision_challenge': {
            'unlocked': 'addition_subtraction' in completed_levels,
            'completed': 'revision_challenge' in completed_levels,
            'points': 100,
            'earned_points': game_progress.get('level_points', {}).get('revision_challenge', 0)
        }
    }
    
    context.update({
        'levels': levels_info,
        'levels_completed': levels_completed_count,
        'total_levels': total_levels,
        'progress_percentage': progress_percentage,
        'points_today': game_progress.get('total_points', 0),
        'max_possible_points': 275  # 25 + 50 + 50 + 50 + 100
    })
    
    return render(request, 'game/dashboard.html', context)

def order_of_numbers(request):
    """Order of Numbers level - 25 points"""
    if not check_session(request):
        return redirect('game:home')
    
    context = get_player_context(request)
    context['level_name'] = 'Order of Numbers'
    context['level_id'] = 'order_of_numbers'
    context['next_level'] = 'numerals_words'
    context['level_points'] = 25
    
    return render(request, 'game/levels/order_of_numbers.html', context)

def numerals_words(request):
    """Numerals & Words level - 50 points"""
    if not check_session(request):
        return redirect('game:home')
    
    game_progress = request.session.get('game_progress', {})
    if 'order_of_numbers' not in game_progress.get('levels_completed', []):
        messages.error(request, 'Complete "Order of Numbers" first!')
        return redirect('game:dashboard')
    
    context = get_player_context(request)
    context['level_name'] = 'Numerals & Words'
    context['level_id'] = 'numerals_words'
    context['next_level'] = 'comparing_numbers'
    context['level_points'] = 50
    
    return render(request, 'game/levels/numerals_words.html', context)

def comparing_numbers(request):
    """Comparing Numbers level - 50 points"""
    if not check_session(request):
        return redirect('game:home')
    
    game_progress = request.session.get('game_progress', {})
    if 'numerals_words' not in game_progress.get('levels_completed', []):
        messages.error(request, 'Complete "Numerals & Words" first!')
        return redirect('game:dashboard')
    
    context = get_player_context(request)
    context['level_name'] = 'Comparing Numbers'
    context['level_id'] = 'comparing_numbers'
    context['next_level'] = 'addition_subtraction'
    context['level_points'] = 50
    
    return render(request, 'game/levels/comparing_numbers.html', context)

def addition_subtraction(request):
    """Addition & Subtraction level - 50 points"""
    if not check_session(request):
        return redirect('game:home')
    
    game_progress = request.session.get('game_progress', {})
    if 'comparing_numbers' not in game_progress.get('levels_completed', []):
        messages.error(request, 'Complete "Comparing Numbers" first!')
        return redirect('game:dashboard')
    
    context = get_player_context(request)
    context['level_name'] = 'Addition & Subtraction'
    context['level_id'] = 'addition_subtraction'
    context['next_level'] = 'revision_challenge'
    context['level_points'] = 50
    
    return render(request, 'game/levels/addition_subtraction.html', context)

def revision_challenge(request):
    """Revision Challenge level - 100 points"""
    if not check_session(request):
        return redirect('game:home')
    
    game_progress = request.session.get('game_progress', {})
    if 'addition_subtraction' not in game_progress.get('levels_completed', []):
        messages.error(request, 'Complete "Addition & Subtraction" first!')
        return redirect('game:dashboard')
    
    context = get_player_context(request)
    context['level_name'] = 'Revision Challenge'
    context['level_id'] = 'revision_challenge'
    context['next_level'] = None
    context['level_points'] = 100
    
    return render(request, 'game/levels/revision_challenge.html', context)

@csrf_exempt
def complete_level(request):
    """Mark a level as complete and award points"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            level_id = data.get('level_id')
            score = data.get('score', 0)
            
            game_progress = request.session.get('game_progress', {})
            
            # Add level to completed if not already there
            if level_id not in game_progress.get('levels_completed', []):
                if 'levels_completed' not in game_progress:
                    game_progress['levels_completed'] = []
                game_progress['levels_completed'].append(level_id)
                
                # Update level-specific points
                if 'level_points' not in game_progress:
                    game_progress['level_points'] = {}
                game_progress['level_points'][level_id] = score
                
                # Update total points
                game_progress['total_points'] = game_progress.get('total_points', 0) + score
                game_progress['points_today'] = game_progress.get('total_points', 0)
            
            # Save back to session
            request.session['game_progress'] = game_progress
            request.session.modified = True
            
            return JsonResponse({
                'success': True, 
                'points': game_progress['total_points'],
                'level_completed': level_id
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})