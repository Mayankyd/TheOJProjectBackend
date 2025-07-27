from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views
from .views import (
    ai_syntax_suggest,
    ai_hint,
    solved_count,
    solved_problems_view,
    LeaderboardView,
)

urlpatterns = [
    # API Endpoints
    path('test/', views.test_submit, name='test_submit'),
    path('submit/', views.submit, name='submit'),
    path('api/problems/', views.problem_list, name='problem_list_api'),
    path('ai_syntax_suggest/', ai_syntax_suggest, name='ai_syntax_suggest'),
    path('ai_hint/', ai_hint, name='ai_hint'),
    path('api/solved-count/', solved_count, name='solved_count'),
    path('api/solved/', solved_problems_view, name='solved_problems'),
    path('api/leaderboard/', LeaderboardView.as_view(), name='leaderboard'),

    # Frontend Catch-All (React SPA)
    re_path(r'^.*$', TemplateView.as_view(template_name="index.html")),
]
