import factory.fuzzy

from memo import models


# class UserFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = models.User
#     username = factory.fuzzy.FuzzyText(prefix='user', length=50)
#     password = '121212ab'
#
#
# class ProfileFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = models.Profile
#
#     user = factory.SubFactory(UserFactory)
#     photo = factory.django.ImageField(from_path='user_images/default.jpg')


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Goal

    name = factory.fuzzy.FuzzyText(prefix='goal', length=50)
    profile = factory.SubFactory(ProfileFactory)


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Section

    name = factory.fuzzy.FuzzyText(prefix='section', length=50)
    goal = factory.SubFactory(GoalFactory)


class ThemeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Theme

    name = factory.fuzzy.FuzzyText(prefix='theme', length=50)
    section = factory.SubFactory(SectionFactory)


class LessonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Lesson

    name = factory.fuzzy.FuzzyInteger(1, step=1)
    profile = factory.SubFactory(ProfileFactory)
    goal = factory.SubFactory(GoalFactory)
    section = factory.SubFactory(SectionFactory)
    theme = factory.SubFactory(ThemeFactory)


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Question

    question = factory.fuzzy.FuzzyText(prefix='questions', length=50)
    answer = factory.fuzzy.FuzzyText(prefix='answer', length=50)
    goal = factory.SubFactory(GoalFactory)
    lesson = factory.SubFactory(LessonFactory)
    section = factory.SubFactory(SectionFactory)
    theme = factory.SubFactory(ThemeFactory)
