from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user_images/%Y/%m/%d', default='user_images/default.jpg')


class Goal(models.Model):
    name = models.CharField(max_length=50)
    profile = models.ForeignKey(Profile,  verbose_name='Профиль', related_name='goals', on_delete=models.CASCADE,
                                default=None)

    def __str__(self):
        return self.name


class Question(models.Model):
    theme = models.SlugField(max_length=100, db_index=True, default=None)
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    goal = models.ForeignKey(Goal, verbose_name='Цель', related_name='questions', on_delete=models.CASCADE,
                             default=None)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.theme
