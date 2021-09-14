import os
from unittest.mock import patch

from django.http import HttpResponse
from django.test import TestCase, RequestFactory

from django.contrib.auth.models import User
from memo.models import Profile, Goal
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.contrib.auth import authenticate, login
from memo.views import ProfilePage, ProfilePageBasic, EditPage, HomePage

os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings'


class ProfilePageTest(TestCase):
    def setUp(self):
        number_of_goals = 5
        self.user = User.objects.create(username='TESTUSER2',
                                        email='testemail@test.test',
                                        password='121212test')
        self.profile = Profile.objects.create(user=self.user,
                                              photo=SimpleUploadedFile('user_images/default.jpg',
                                                                       content=b'',
                                                                       content_type='default.jpg'))
        for goal_num in range(number_of_goals):
            Goal.objects.create(name='TEST_GOAL %s' % goal_num, profile=self.profile)

    def test_home(self):
        #  client = Client()
        # login = self.client.login(username='TESTUSER2', password='121212test')
        resp = self.client.get(reverse('memo:home'))
        self.assertEqual(resp.status_code, 200)

    def test_response_from_home_page_view(self):
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        resp = HomePage.as_view()(request)
        self.assertEqual(resp.status_code, 200)

    @patch('memo.views.profile.redirect')
    def test_anonimus_user_get_profile(self, mock_redirect):
        expected_result = HttpResponse()
        mock_redirect.return_value = expected_result
        actual_result = self.client.get(reverse('memo:profile_basic'))
        mock_redirect.assert_called_with('account:login')
        self.assertEqual(actual_result, expected_result)

    @patch('account.views.redirect')
    @patch('account.views.LoginForm')
    def test_login_view_not_valid_form(self, mock_login_form, mock_redirect):
        mock_login_form().is_valid.return_value = False
        expected_result = HttpResponse()
        mock_redirect.return_value = expected_result
        actual_result = self.client.post(reverse('account:login'), data={})
        mock_redirect.assert_called_with('account:login')
        self.assertEqual(actual_result, expected_result)

    # @patch('account.views.redirect')
    # @patch('account.views.LoginForm')
    # # @patch('account.views.user')
    # def test_logined_user_get_profile(self, mock_redirect, mock_login_form):
    #     mock_login_form().is_valid.return_value = True
    #     mock_redirect.return_value = HttpResponse()
    #     self.client.login(username='TESTUSER2', password='121212test')
    #     resp = self.client.get(reverse('memo:profile', kwargs={'username': 'TESTUSER2'}))
    #     self.assertEqual(resp.status_code, 200)

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


        # Проверка того, что мы используем правильный шаблон
        # self.assertTemplateUsed(resp, 'catalog/bookinstance_list_borrowed_user.html')
