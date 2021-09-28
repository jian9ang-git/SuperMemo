import os
from unittest.mock import patch, MagicMock
from django.http import HttpResponse, HttpResponseRedirect
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import authenticate, login
import factory

from lesson.views import SurePage
from memo.views import ProfilePage, ProfilePageBasic, EditPage, HomePage, GoalPage
from memo.forms import PersonalDataEditForm, AddGoalForm
from memo.models import Profile, Goal, Section, Theme, Question, Lesson
from memo.tests.factories import UserFactory, ProfileFactory, GoalFactory, SectionFactory, ThemeFactory, LessonFactory,\
    QuestionFactory
os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings'


class LessonTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.user.set_password('121212test')
        self.user.save()
        self.profile = ProfileFactory(user=self.user)
        self.goal = GoalFactory(profile=self.profile)
        self.section1 = SectionFactory.create(goal=self.goal)
        self.section2 = SectionFactory.create(goal=self.goal)
        self.theme1 = ThemeFactory.create(section=self.section1, goal=self.goal)
        self.theme2 = ThemeFactory.create(section=self.section1, goal=self.goal)

        self.lesson = LessonFactory.create(profile=self.profile,
                                           goal=self.goal)

    def test_user_get_sure_page_v1(self):
        expected_result = HttpResponse
        login = self.client.login(username='test_user0', password='121212test')
        section = Section.objects.get(pk=1)
        theme = Theme.objects.get(pk=1)
        goal = Goal.objects.get(pk=1)
        session = self.client.session
        session['lesson_section_id'] = 1
        session['lesson_theme_id'] = 1
        session['goal_id'] = 1
        session.save()
        actual_result = self.client.get(reverse('lesson:sure'))

        self.assertEqual(actual_result.context['section'], section)
        self.assertEqual(actual_result.context['theme'], theme)
        self.assertEqual(actual_result.context['goal'], goal)
        self.assertTemplateUsed(actual_result, 'sure_page.html')

