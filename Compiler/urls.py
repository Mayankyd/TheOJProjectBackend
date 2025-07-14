from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views
from .views import ai_syntax_suggest
from .views import ai_hint

urlpatterns = [
    path('test/', views.test_submit, name='test_submit'),     # ✅ Place specific paths first
    path('submit/', views.submit, name='submit'),
    path('api/problems/', views.problem_list, name='problem_list_api'),
    path('ai_syntax_suggest/', ai_syntax_suggest),
    path('ai_hint/', ai_hint, name='ai_hint'),
    # Catch-all for frontend only after all backend views
    re_path(r'^.*$', TemplateView.as_view(template_name="index.html")),
]
