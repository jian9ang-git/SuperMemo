from django.test import TestCase, RequestFactory

from django.contrib.auth.forms import User
from django.contrib.auth import get_user_model
from memo.models import Profile, Goal, Question, Section, Theme, Lesson
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest import mock


#  Вы должны тестировать все аспекты, касающиеся вашего кода,
#  но не библиотеки, или функциональность, предоставляемые Python, или Django.
#  python3 manage.py test --verbosity 2    0, 1, 3, 4 - получение более подробной инфы о тестах
# python3 manage.py test catalog.tests   # Run the specified module
# python3 manage.py test catalog.tests.test_models  # Run the specified module
# python3 manage.py test catalog.tests.test_models.YourTestClass # Run the specified class
# python3 manage.py test catalog.tests.test_models.YourTestClass.test_one_plus_one_equals_two  # Run the specified meth
# setUpTestData() - тест + создание объектов, которые не будут изменены
# setup() - тест + создания объектов, которые МОГУТ быть изменены

class MemoTestCases(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='TESTUSER',
                                        password='121212test')
        self.profile = Profile.objects.create(user=self.user,
                                              photo=SimpleUploadedFile('user_images/default.jpg',
                                                                       content=b'',
                                                                       content_type='default.jpg'))
        self.goal = Goal.objects.create(name='TEST_GOAL', profile=self.profile)
        self.section = Section.objects.create(name='TEST_SECTION', goal=self.goal)
        self.theme = Theme.objects.create(name='TEST_THEME', section=self.section, goal=self.goal)
        self.lesson = Lesson.objects.create(name=123123, goal=self.goal, profile=self.profile)
        self.question = Question.objects.create(question='TEST_QUESTION',
                                                answer='TEST_ANSWER',
                                                lesson=self.lesson,
                                                section=self.section,
                                                theme=self.theme,
                                                goal=self.goal)

    def test_profile_id_equal_user_id(self):
        self.assertEquals(self.user.id, self.profile.id)

    def test_username_label(self):

        field_label_username = self.user._meta.get_field('username').verbose_name
        field_label_password = self.user._meta.get_field('password').verbose_name

        self.assertEquals(field_label_username, 'username')
        self.assertEquals(field_label_password, 'password')

    def test_profile_name_label(self):
        profile = self.profile
        field_label_user = profile._meta.get_field('user').verbose_name
        field_label_photo = profile._meta.get_field('photo').verbose_name

        self.assertEquals(field_label_photo, 'photo')
        self.assertEquals(field_label_user, 'user')

    def test_goal_fields_label(self):
        goal = self.goal
        field_label_name = goal._meta.get_field('name').verbose_name
        field_label_profile = goal._meta.get_field('profile').verbose_name

        self.assertEquals(field_label_name, 'name')
        self.assertEquals(field_label_profile, 'profile')

    def test_section_fields_labels(self):
        section = self.section
        field_label_name = section._meta.get_field('name').verbose_name
        field_label_goal = section._meta.get_field('goal').verbose_name

        self.assertEquals(field_label_goal, 'goal')
        self.assertEquals(field_label_name, 'name')

    def test_theme_fields_labels(self):
        theme = self.theme
        field_label_name = theme._meta.get_field('name').verbose_name
        field_label_section = theme._meta.get_field('section').verbose_name
        field_label_goal = theme._meta.get_field('goal').verbose_name

        self.assertEquals(field_label_name, 'name')
        self.assertEquals(field_label_section, 'section')
        self.assertEquals(field_label_goal, 'goal')

    def test_lesson_fields_labels(self):
        lesson = self.lesson
        field_label_name = lesson._meta.get_field('name').verbose_name
        field_label_goal = lesson._meta.get_field('goal').verbose_name
        field_label_profile = lesson._meta.get_field('profile').verbose_name
        field_label_start = lesson._meta.get_field('start').verbose_name
        field_label_end = lesson._meta.get_field('end').verbose_name
        field_label_ = lesson._meta.get_field('name').verbose_name

        self.assertEquals(field_label_name, 'name')
        self.assertEquals(field_label_goal, 'goal')
        self.assertEquals(field_label_profile, 'profile')
        self.assertEquals(field_label_start, 'start')
        self.assertEquals(field_label_end, 'end')

    def test_question_fields_labels(self):
        question = self.question
        field_label_question = question._meta.get_field('question').verbose_name
        field_label_answer = question._meta.get_field('answer').verbose_name
        field_label_section = question._meta.get_field('section').verbose_name
        field_label_theme = question._meta.get_field('theme').verbose_name
        field_label_goal = question._meta.get_field('goal').verbose_name

        self.assertEquals(field_label_question, 'question')
        self.assertEquals(field_label_answer, 'answer')
        self.assertEquals(field_label_section, 'section')
        self.assertEquals(field_label_theme, 'theme')
        self.assertEquals(field_label_goal, 'goal')

    # def test_date_of_death_label(self):
    #     author = Author.objects.get(id=1)
    #     field_label = author._meta.get_field('date_of_death').verbose_name
    #     self.assertEquals(field_label, 'died')
    #
    # def test_first_name_max_length(self):
    #     author = Author.objects.get(id=1)
    #     max_length = author._meta.get_field('first_name').max_length
    #     self.assertEquals(max_length, 100)
    #
    # def test_object_name_is_last_name_comma_first_name(self):
    #     author = Author.objects.get(id=1)
    #     expected_object_name = '%s, %s' % (author.last_name, author.first_name)
    #     self.assertEquals(expected_object_name, str(author))
    #
    # def test_get_absolute_url(self):
    #     author = Author.objects.get(id=1)
    #     # This will also fail if the urlconf is not defined.
    #     self.assertEquals(author.get_absolute_url(), '/catalog/author/1')
    #
    # def test_create_lesson(self):
    #     lesson = Lesson()
    #     factory = RequestFactory()
    #     request = factory.get('')