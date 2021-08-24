from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import LessonPage, EndLessonPage, AddThemePage, ChooseThemePage, AddSectionPage, ChooseSectionPage


urlpatterns = [

    path('new-lesson/choose_section/', ChooseSectionPage.as_view(), name='choose_section'),
    path('new-lesson/choose_theme/', ChooseThemePage.as_view(), name='choose_theme'),
    path('new-lesson/add_section/', AddSectionPage.as_view(), name='add_section'),
    path('new-lesson/add_theme/', AddThemePage.as_view(), name='add_theme'),
    path('learning-page/lesson/', LessonPage.as_view(), name='lesson_page'),
    path('learning-page/end-lesson/', EndLessonPage.as_view(), name='end_lesson'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
