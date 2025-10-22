from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import QuizView, QuizListView, QuizResultView
from . import views
from programmes.views import (
    LessonCreateView,
    LessonListViewDetail,
    LessonUpdateView,
    LessonDeleteView,
    LessonListView
)

app_name = "programmes"

urlpatterns = [
    path('create/', LessonCreateView.as_view(), name="lessoncreate"),
    path('lessonlist/', LessonListView.as_view(), name='lessonlist'),
    path('lessonlist/<slug:slug>/', LessonListViewDetail.as_view(), name='lessonlistslug'),
    path('<slug:slug>/update', LessonUpdateView.as_view(), name="lessonupdate"),
    path('<slug:slug>/delete', LessonDeleteView.as_view(), name="lessondelete"),
    path('quiz/<int:pk>/', QuizView.as_view(), name='quiz_view'),
    path('quiz_list/<slug:slug>/', QuizListView.as_view(), name='quiz_list'),
    path('quiz_result/', QuizResultView.as_view(), name='quiz_result'),
    path('<slug:slug>/', LessonListViewDetail.as_view(), name="lessonlistdetail"),
    path('lessons/<slug:slug>/download_pdf/', views.download_lesson_pdf, name='download_lesson_pdf')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
