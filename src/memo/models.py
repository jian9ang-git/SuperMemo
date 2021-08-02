from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import OneToOneField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user_images/%Y/%m/%d', default='user_images/default.jpg')


class Goal(models.Model):
    name = models.CharField(max_length=50)
    profile = models.ForeignKey(Profile,  verbose_name='Профиль', related_name='goals', on_delete=models.CASCADE,
                                default=None)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=50, default=None)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Theme(models.Model):
    name = models.CharField(max_length=200, db_index=True, default=None)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=200, db_index=True, default=None)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)
    theme = models.ForeignKey(Theme, verbose_name='Цель', related_name='questions', on_delete=models.CASCADE,
                              default=None)
    lesson = models.ForeignKey(Lesson, related_name='questions', on_delete=models.CASCADE,
                               default=None)

    def __str__(self):
        return self.question
