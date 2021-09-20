import os
from unittest.mock import patch

from django.http import HttpResponse, HttpResponseRedirect
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from unittest.mock import MagicMock
from memo.forms import PersonalDataEditForm
from memo.models import Profile, Goal
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import authenticate, login
from memo.views import ProfilePage, ProfilePageBasic, EditPage, HomePage


class AccountTest(TestCase):
    def setUp(self):
        number_of_goals = 2
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create(username='testuser1',
                                        email='testemail@test.test',
                                        )
        self.user.set_password('121212test')
        self.user.save()
        self.profile = Profile.objects.create(user=self.user)
        for goal_num in range(number_of_goals):
            Goal.objects.create(name=f'TEST_GOAL {goal_num}', profile=self.profile)

    @patch('account.views.redirect')
    @patch('account.views.LoginForm')
    def test_login_view_not_valid_form(self, mock_login_form, mock_redirect):
        mock_login_form().is_valid.return_value = False
        expected_result = HttpResponse()
        mock_redirect.return_value = expected_result
        actual_result = self.client.post(reverse('account:login'), data={})
        mock_redirect.assert_called_with('account:login')
        self.assertEqual(actual_result, expected_result)

    @patch('account.views.authenticate')
    @patch('account.views.LoginForm')
    def test_login_view_user_is_none(self, mock_login_form, mock_authenticate):
        mock_login_form().is_valid.return_value = True
        mock_authenticate.return_value = None
        expected_result = HttpResponse('Invalid login')
        actual_result = self.client.post(reverse('account:login'), data={})
        self.assertEqual(actual_result.content, expected_result.content)
        self.assertEqual(actual_result.status_code, 200)

    @patch('account.views.authenticate')
    @patch('account.views.LoginForm')
    def test_login_view_inactive_user(self, mock_login_form, mock_authenticate):
        self.user.is_active = False
        self.user.save()
        mock_login_form().is_valid.return_value = True
        mock_authenticate.return_value = self.user

        expected_result = HttpResponse('Disabled account')
        actual_result = self.client.post(reverse('account:login'), data={})
        self.assertEqual(actual_result.content, expected_result.content)
        self.assertEqual(actual_result.status_code, 200)
        self.user.is_active = True
        self.user.save()
        # Todo нужны ли 2 последние строчки? - СДелать not_active_user active_true

    @patch('account.views.redirect')
    @patch('account.views.authenticate')
    @patch('account.views.LoginForm')
    def test_login_view_valid_form_active_user(self, mock_login_form, mock_authenticate, mock_redirect):
        mock_login_form().is_valid.return_value = True
        mock_authenticate.return_value = self.user
        expected_result = HttpResponse()
        mock_login_form().cleaned_data = {'username': 'testuser1', 'password': '121212test'}
        mock_redirect.return_value = expected_result
        actual_result = self.client.post(reverse('account:login'), data={})
        mock_redirect.assert_called_with('memo:profile', username='testuser1')
        self.assertEqual(actual_result, expected_result)
        self.assertEqual(actual_result.status_code, 200)