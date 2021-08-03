from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import LessonPage, start_lesson

urlpatterns = [
    path('learning-page/<int:goal_id>', start_lesson, name='new_lesson'),
    path('learning-page/', start_lesson, name='new_lesson'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)