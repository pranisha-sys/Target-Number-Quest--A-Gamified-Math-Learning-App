from django.shortcuts import render
from django.http import JsonResponse
import random
import json

def home(request):
    """Home page with welcome screen"""
    return render(request, 'game/home.html')

def game(request):
    """Main game page"""
    player_name = request.GET.get('name', 'Player')
    return render(request, 'game/game.html', {'player_name': player_name})

def new_game(request):
    """Generate a new game with random numbers and target"""
    if request.method == 'POST':
        numbers = [random.randint(1, 25) for _ in range(6)]
        target = random.randint(100, 999)
        
        request.session['numbers'] = numbers
        request.session['target'] = target
        request.session['moves'] = 0
        
        return JsonResponse({
            'numbers': numbers,
            'target': target
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def check_solution(request):
    """Check if the player's solution is correct"""
    if request.method == 'POST':
        data = json.loads(request.body)
        result = data.get('result')
        target = request.session.get('target')
        
        if result == target:
            return JsonResponse({'success': True, 'message': 'Perfect! You hit the target!'})
        else:
            difference = abs(target - result)
            return JsonResponse({
                'success': False, 
                'message': f'Close! You were off by {difference}',
                'difference': difference
            })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)