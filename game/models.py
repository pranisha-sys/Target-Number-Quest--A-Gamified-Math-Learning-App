from django.db import models
from django.contrib.auth.models import User

class PlayerProfile(models.Model):
    """Store player information and progress"""
    name = models.CharField(max_length=100)
    total_score = models.IntegerField(default=0)
    highest_level = models.IntegerField(default=1)
    games_played = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-total_score']
    
    def __str__(self):
        return f"{self.name} - Level {self.highest_level}"

class GameSession(models.Model):
    """Track individual game sessions"""
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='sessions')
    score = models.IntegerField(default=0)
    level_reached = models.IntegerField(default=1)
    questions_answered = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    parent_approved = models.BooleanField(default=False)
    session_start = models.DateTimeField(auto_now_add=True)
    session_end = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-session_start']
    
    def __str__(self):
        return f"{self.player.name} - {self.session_start.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def accuracy(self):
        if self.questions_answered == 0:
            return 0
        return round((self.correct_answers / self.questions_answered) * 100, 2)

class Question(models.Model):
    """Store questions asked during sessions"""
    OPERATION_CHOICES = [
        ('+', 'Addition'),
        ('-', 'Subtraction'),
        ('*', 'Multiplication'),
        ('/', 'Division'),
    ]
    
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=200)
    operation = models.CharField(max_length=1, choices=OPERATION_CHOICES)
    correct_answer = models.IntegerField()
    user_answer = models.IntegerField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    time_taken_seconds = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.question_text} = {self.correct_answer}"

class Achievement(models.Model):
    """Track player achievements and badges"""
    ACHIEVEMENT_TYPES = [
        ('first_game', 'First Game Completed'),
        ('level_5', 'Reached Level 5'),
        ('level_10', 'Reached Level 10'),
        ('score_100', 'Scored 100 Points'),
        ('score_500', 'Scored 500 Points'),
        ('perfect_10', '10 Correct Answers in a Row'),
        ('speed_master', 'Answered 5 Questions in Under 30 Seconds'),
    ]
    
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='achievements')
    achievement_type = models.CharField(max_length=50, choices=ACHIEVEMENT_TYPES)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['player', 'achievement_type']
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.player.name} - {self.get_achievement_type_display()}"