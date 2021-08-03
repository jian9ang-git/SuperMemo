from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.decorators.http import require_POST

from .lesson import LessonCart
from memo.models import Lesson
from memo.models import Question, Goal


@require_POST
def start_lesson(request, *args, **kwargs):
    lesson_cart = LessonCart(request)
    lesson_counter = request.user.profile.goals.lessons.count()
    goal = Goal.objects.get(pk=kwargs['goal_id'])
    lesson = Lesson.objects.create(name=lesson_counter+1, goal=goal)
    return render('lesson.html', {'lesson_cart': lesson_cart})


class LessonPage(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class EndLessonPage(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass