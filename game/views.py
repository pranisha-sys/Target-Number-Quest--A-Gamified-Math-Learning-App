from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
import json

def login_view(request):
    """Login page - renders login.html"""
    if request.user.is_authenticated:
        return redirect('game:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'redirect': '/game/'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})
    
    return render(request, 'game/login.html')

def signin_view(request):
    """Sign in (registration) page - renders signin.html"""
    if request.user.is_authenticated:
        return redirect('game:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Username already exists'})
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Email already exists'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return JsonResponse({'success': True, 'redirect': '/game/'})
    
    return render(request, 'game/signin.html')

def logout_view(request):
    """Logout user"""
    logout(request)
    return redirect('game:login')

@login_required(login_url='/game/login/')
def home(request):
    """Home page - renders home.html (requires login)"""
    return render(request, 'game/home.html', {
        'username': request.user.username
    })

@login_required(login_url='/game/login/')
def game(request):
    """Main game page - renders game.html (requires login)"""
    player_name = request.GET.get('name', request.user.username)
    return render(request, 'game/game.html', {'player_name': player_name})

@login_required
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

@login_required
def check_solution(request):
    """Check if the player's solution is correct"""
    if request.method == 'POST':
        data = json.loads(request.body)
        result = data.get('result')
        target = request.session.get('target')
        
        if result == target:
           return JsonResponse({'success': True, 'redirect': '/game/'})
        else:
            difference = abs(target - result)
            return JsonResponse({
                'success': False, 
                'message': f'Close! You were off by {difference}',
                'difference': difference
            })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)