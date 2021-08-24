from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.decorators.http import require_POST
from memo.models import Lesson, Question, Goal, Theme, Section
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from lesson.forms import ChooseSectionForm, ChooseThemeForm, LearningForm


@method_decorator(login_required, name='dispatch')
class SurePage(View):
    def get(self, request, *args, **kwargs):
        section = Section.objects.get(pk=request.session['lesson_section_id'])
        theme = Theme.objects.get(pk=request.session['lesson_theme_id'])
        goal = Goal.objects.get(pk=request.session['goal_id'])
        return render(request, 'sure_page.html', {'goal': goal, 'section': section, 'theme': theme})

    def post(self, request, *args, **kwargs):
        pass


@method_decorator(login_required, name='dispatch')
class LessonPage(View):
    def get(self, request, *args, **kwargs):

        profile = request.user.profile
        goal = Goal.objects.get(pk=request.session['goal_id'])
        name = goal.lesson.count + 1
        lesson = Lesson.objects.create(name=name, goal=goal, profile=profile)
        request.session['active_lesson_id'] = lesson.id

        form = LearningForm
        return render('lesson.html', {'form': form, 'lesson': lesson})

    def post(self, request, *args, **kwargs):
        form = LearningForm(request.POST or None)
        cd = form.cleaned_data
        goal = Goal.objects.get(pk=request.session['goal_id'])
        section = Section.objects.get(pk=request.session['lesson_section_id'])
        theme = Theme.objects.get(pk=request.session['lesson_theme_id'])
        if form.is_valid():
            question = cd['question']
            answer = cd['answer']
            Question.objects.create(question=question,
                                    answer=answer,
                                    profile=request.user.profile,
                                    goal=goal,
                                    section=section,
                                    theme=theme)
            form = LearningForm
            return render('lesson.html', {'form': form})
        else:
            return render('lesson.html', {'form': form})


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
