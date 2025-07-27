from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('login.urls')),         # Auth and login APIs
    path('compiler/', include('Compiler.urls')), # Judge logic
]

# ✅ Serve static files (during development only)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(BASE_DIR.parent, 'frontend', 'dist'))

# ✅ Catch-all for React SPA must come last
urlpatterns += [
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
