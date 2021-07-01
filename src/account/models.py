from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question_theme = models.CharField(max_length=50)
    question = models.CharField(max_length=100)
    question_answer = models.CharField(max_length=100)

    def __str__(self):
        return self.question_theme


class Goal(models.Model):
    goals_number = models.IntegerField(default=0)
    goal_name = models.CharField(max_length=50)
    goal_slug = models.SlugField(max_length=200, db_index=True, unique=True, null=True)
    goal_total_questions = models.IntegerField()
    goal_done_questions = models.IntegerField()
    goal_question = models.ForeignKey(Question,  verbose_name='Вопрос', on_delete=models.CASCADE)

    def __str__(self):
        return self.goal_name


class MemoUser(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    goals = models.ForeignKey(Goal, verbose_name='Цели', on_delete=models.CASCADE)

    def __str__(self):
        return self.user['username']
