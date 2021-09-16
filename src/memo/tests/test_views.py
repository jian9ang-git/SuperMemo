import os
from unittest.mock import patch

from django.http import HttpResponse, HttpResponseRedirect
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
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create(username='testuser',
                                        email='testemail@test.test',
                                        )
        self.user.set_password('121212test')
        self.user.save()
        self.profile = Profile.objects.create(user=self.user,
                                              photo=SimpleUploadedFile('user_images/default.jpg',
                                                                       content=b'',
                                                                       content_type='default.jpg'))
        for goal_num in range(number_of_goals):
            Goal.objects.create(name=f'TEST_GOAL {goal_num}', profile=self.profile)

        # response = c.post(reverse('account:login'), data={})
        # self.user = c.login(username=self.user.username, password=self.user.password)

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
