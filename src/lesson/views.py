from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.decorators.http import require_POST
from .lesson import LessonCart
from memo.models import Lesson
from memo.models import Question, Goal
from .forms import LearningForm


def start_lesson(request, *args, **kwargs):
    goal = Goal.objects.get(pk=kwargs['goal_id'])
    request.session['goal_id'] = goal.id
    lesson_counter = goal.lessons.count()
    name = lesson_counter + 1
    lesson = Lesson.objects.create(name=name, goal=goal)
    request.session['lesson_id'] = lesson.id
    request.session['lesson_name'] = lesson.name
    return redirect('lesson:lesson_page')


@require_POST
def next_lesson(request, *args, **kwargs):
    pass


class LessonPage(View):
    def get(self, request, *args, **kwargs):
        goal = Goal.objects.get(pk=request.session['goal_id'])
        section = request.session['section']
        theme = request.session['theme']
        if section != '' and theme != '':
            form = LearningForm(initial={'section': section, 'theme': theme},
                                instance=goal)
        else:
            form = LearningForm(instance=goal)
        return render(request, 'lesson.html', {'form': form, 'lesson_name': request.session['lesson_name']})

    def post(self, request, *args, **kwargs):
        form = LearningForm(request.POST)
        lesson_cart = LessonCart(request)
        lesson = Lesson.objects.get(pk=request.session['lesson_id'])
        if form.is_valid():
            cd = form.cleaned_data
            question = Question.objects.create(question=cd['question'],
                                               answer=cd['answer'],
                                               theme=cd['theme'],
                                               section=cd['section'],
                                               goal=lesson.goal)
            lesson_cart.add(question=question)
            request.session['section'] = cd['section']
            request.session['theme'] = cd['theme']
        return render(request, 'lesson.html', {'form': form, 'lesson_name': request.session['lesson_name']})


class EndLessonPage(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass