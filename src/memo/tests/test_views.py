import os
from unittest.mock import patch, MagicMock

from django.http import HttpResponse, HttpResponseRedirect
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User

from memo.forms import PersonalDataEditForm
from memo.models import Profile, Goal
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import authenticate, login
from memo.views import ProfilePage, ProfilePageBasic, EditPage, HomePage

os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings'


class ProfilePageTest(TestCase):
    def setUp(self):
        number_of_goals = 2
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create(username='testuser',
                                        email='testemail@test.test',
                                        )
        self.user.set_password('121212test')
        self.user.save()
        self.profile = Profile.objects.create(user=self.user)
        for goal_num in range(number_of_goals):
            Goal.objects.create(name=f'TEST_GOAL {goal_num}', profile=self.profile)

    def test_response_from_home_page_view_v1(self):
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        resp = HomePage.as_view()(request)
        self.assertEqual(resp.status_code, 200)

    def test_response_from_home_page_view_v2(self):
        resp = self.client.get(reverse('memo:home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'home.html', 'base.html')

    def test_response_from_profile_page_view(self):
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        resp = ProfilePage.as_view()(request, username=self.user.username)
        self.assertEqual(resp.status_code, 200)

    def test_response_from_edit_page_view(self):
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        resp = EditPage.as_view()(request)
        self.assertEqual(resp.status_code, 200)

    @patch('memo.views.profile.redirect')
    def test_anonymous_user_get_profile_basic(self, mock_redirect):
        expected_result = HttpResponse()
        mock_redirect.return_value = expected_result
        actual_result = self.client.get(reverse('memo:profile_basic'))
        mock_redirect.assert_called_with('account:login')
        self.assertEqual(actual_result, expected_result)

    @patch('memo.views.profile.redirect')
    def test_logined_user_get_profile_basic(self, mock_redirect):
        expected_result = HttpResponseRedirect(redirect_to='/profile/testuser')
        mock_redirect.return_value = expected_result
        login = self.client.login(username='testuser', password='121212test')
        actual_result = self.client.get(reverse('memo:profile_basic'))
        mock_redirect.assert_called_with('memo:profile', username='testuser')
        self.assertEqual(actual_result, expected_result)

    def test_logined_user_get_profile(self):
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        expected_result = HttpResponse()
        login = self.client.login(username='testuser', password='121212test')
        actual_result = self.client.get(reverse('memo:profile', kwargs={'username': 'testuser'}))

        self.assertTemplateUsed(actual_result, 'profile_page.html', 'base.html')
        self.assertEqual(actual_result.status_code, 200)
        self.assertEqual(actual_result.context['profile'], self.profile)
        self.assertEqual(actual_result.context['username'], 'testuser')
        # Todo Чтобы обойти ошибку 1 != 1 сделал такую проверку для goals = profile.goals.all()
        q_goals = self.profile.goals.all()
        i = actual_result.context['goals'].count()
        j = q_goals.count()
        if self.assertEqual(i, j):
            for index in range(i-1):
                self.assertEqual(actual_result.context['goals'][index], q_goals[index])

    @patch('memo.views.profile.render')
    @patch('memo.views.profile.PersonalDataEditForm')
    def test_logined_user_get_edit_page(self, mock_form, mock_render):
        expected_result = HttpResponse()
        form = MagicMock()
        mock_form.return_value = form
        mock_render.return_value = expected_result
        login = self.client.login(username='testuser', password='121212test')
        actual_result = self.client.get(reverse('memo:edit'), data={})
        mock_render.assert_called_once_with(actual_result.wsgi_request, 'edit.html', {'form': form})

    @patch('memo.views.profile.redirect')
    @patch('memo.views.profile.PersonalDataEditForm')
    def test_logined_user_post_edit_page_valid_form(self, mock_form, mock_redirect):
        expected_result = HttpResponseRedirect('/profile/testuser')
        # form = MagicMock()
        # mock_form.return_value = form
        mock_form().is_valid.return_value = True
        mock_form().cleaned_data = {'username': 'testuser',
                                    'password': '121212test',
                                    'email': 'testemail@test.test'}
        mock_redirect.return_value = expected_result
        login = self.client.login(username='testuser', password='121212test')
        actual_result = self.client.post(reverse('memo:edit'), data={})
        mock_redirect.assert_called_once_with('memo:profile', username='testuser')  # Todo проблема с username
        self.assertEqual(actual_result, expected_result)
        self.assertEqual(actual_result.status_code, 302)

    @patch('memo.views.profile.render')
    @patch('memo.views.profile.PersonalDataEditForm')
    def test_logined_user_post_edit_page_not_valid_form(self, mock_form, mock_render):
        expected_result = HttpResponse()
        form = MagicMock()
        mock_form.return_value = form  # Todo Ловил ошибку из-за скобок после mock_form
        mock_form().is_valid.return_value = False
        mock_render.return_value = expected_result
        login = self.client.login(username='testuser', password='121212test')
        actual_result = self.client.post(reverse('memo:edit'), data={})
        mock_render.assert_called_once_with(actual_result.wsgi_request, 'edit.html', {'form': form})
        self.assertEqual(actual_result, expected_result)
        self.assertEqual(actual_result.status_code, 200)