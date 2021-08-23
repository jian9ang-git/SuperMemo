from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.decorators.http import require_POST
from memo.models import Lesson, Question, Goal, Theme
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from lesson.forms import ChooseSectionForm, ChooseThemeForm


@method_decorator(login_required, name='dispatch')
class LessonPage(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class EndLessonPage(View):
    def get(self, request, *args, **kwargs):
        lesson = Lesson.objects.get(pk=request.session['lesson_id'])
        return render(request, 'end_lesson.html', {'lesson': lesson})

    def post(self, request, *args, **kwargs):
        # lesson_cart = LessonCart(request)
        # lesson = lesson_cart[request.session['lesson_id']]['lesson']
        lesson = Lesson.objects.get(pk=request.session['lesson_id'])
        lesson.set(active_lesson=False)
        # lesson_cart.clear()
