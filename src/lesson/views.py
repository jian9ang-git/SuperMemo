from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.decorators.http import require_POST
from .lesson import LessonCart
from memo.models import Lesson, Question, Goal, Theme, Section
from .forms import LearningForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


def start_lesson(request, *args, **kwargs):
    goal = Goal.objects.get(pk=kwargs['goal_id'])
    request.session['goal_id'] = goal.id

    lesson_counter = goal.lessons.count()
    name = lesson_counter + 1

    lesson = Lesson.objects.create(name=name, goal=goal, active_lesson=True, profile=request.user.profile)
    request.session['lesson_id'] = lesson.id
    request.session['lesson_name'] = lesson.name

    # lesson_cart = LessonCart(request)
    # lesson_cart.add(lesson=lesson)
    return redirect('lesson:lesson_page')


@method_decorator(login_required, name='dispatch')
class LessonPage(View):
    def get(self, request, *args, **kwargs):
        goal = Goal.objects.get(pk=request.session['goal_id'])
        last_used_theme = goal.themes.filter(last_used=True).first()
        if last_used_theme:
            request.session['last_used_theme_id'] = last_used_theme.id
            theme_name = last_used_theme.name
            section_name = last_used_theme.section.name
            form = LearningForm(initial={'section': section_name, 'theme': theme_name})
        else:
            form = LearningForm()
        return render(request, 'lesson.html', {'form': form, 'lesson_name': request.session['lesson_name']})

    def post(self, request, *args, **kwargs):
        form = LearningForm(request.POST)
        lesson = Lesson.objects.get(pk=request.session['lesson_id'])
        if form.is_valid():
            cd = form.cleaned_data
            last_used_theme = Theme.objects.get(last_used=True)  # TODO filter with user id

            if not Section.objects.get(name=cd['section']).exists():
                section = Section.objects.create(name=cd['section'],
                                                 goal=Goal.objects.get(pk=request.session['goal_id']))
            else:
                section = Section.objects.get(name=cd['section'])  # TODO filter with user id

            if not Theme.objects.get(name=cd['theme']).exists():   # TODO filter with user id
                last_used_theme.set(last_used=False)
                theme = Theme.objects.create(name=cd['theme'],
                                             section=section,
                                             goal=last_used_theme.goal,
                                             last_used=True)
            else:
                theme = Theme.objects.get(name=cd['theme'])
                if last_used_theme.id != theme.id:
                    last_used_theme.set(last_used=False)
                    theme.set(last_used=True)

            question = Question.objects.create(question=cd['question'],
                                               answer=cd['answer'],
                                               theme=theme,
                                               section=section,
                                               goal=lesson.goal,
                                               lesson=lesson)

            # request.session['section'] = cd['section']
            # request.session['theme'] = cd['theme']
        # return render(request, 'lesson.html', {'form': form, 'lesson_name': request.session['lesson_name']})
        return redirect('lesson:lesson_page')


class EndLessonPage(View):
    def get(self, request, *args, **kwargs):
        lesson = Lesson.objects.get(pk=request.session['lesson_id'])
        return render(request, 'end_lesson.html', {'lesson': lesson})

    def post(self, request, *args, **kwargs):
        lesson_cart = LessonCart(request)
        # lesson = lesson_cart[request.session['lesson_id']]['lesson']
        lesson = Lesson.objects.get(pk=request.session['lesson_id'])
        lesson.set(active_lesson=False)
        lesson_cart.clear()
