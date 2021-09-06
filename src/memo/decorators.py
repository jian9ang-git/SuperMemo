from functools import wraps

from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.views import View


class TestMixin1(UserPassesTestMixin):

    def __init__(self, request, *args, **kwargs):
        self.session = request.session

    def test_func(self):
        if self.session['active_lesson_id']:
            return redirect('lesson:lesson_page')
