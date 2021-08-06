from decimal import Decimal
from django.conf import settings
from django.db import models
from memo.models import Question


class LessonCart(object):

    def __init__(self, request):

        self.session = request.session
        lesson = self.session.get(settings.LESSON_SESSION_ID)
        if not lesson:
            lesson = self.session[settings.LESSON_SESSION_ID] = {}
        self.lesson = lesson

    def add(self, question):
        question_id = str(question.id)
        if question_id not in self.lesson:
            self.lesson[question_id] = {'question': question}

    def save(self):
        self.session[settings.LESSON_SESSION_ID] = self.lesson
        self.session.modified = True

    def remove(self, question):
        question_id = str(question.id)
        if question_id in self.lesson:
            del self.lesson[question_id]
            self.save()

    def __iter__(self):
        questions_ids = self.lesson.keys()
        questions = Question.objects.filter(id__in=questions_ids)
        for question in questions:
            self.lesson[str(question.id)]['product'] = question

    def __len__(self):
        return sum(1 for item in self.lesson.keys())

    def clear(self):
        del self.session[settings.LESSON_SESSION_ID]
        self.session.modified = True
