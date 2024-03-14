"""
URL configuration for blogging_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path 
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.views.generic import TemplateView  # Import TemplateView if needed
from blog.views import home
from blog.views import search_posts
from blog.views import create_post_api
from django.views.generic import RedirectView
from blog.views import register

urlpatterns = [
    path('', RedirectView.as_view(url='register/', permanent=False)),  # Redirect to register page by default
    path('admin/', admin.site.urls),
    path('api/', include('blog.urls')),
    re_path('custom_path/', include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', RedirectView.as_view(url='/home/', permanent=False)),  # Redi
    path('home/', home, name='home'),  # Use the imported home view
    path('search/', search_posts, name='search_posts'),
    path('media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('api/create_post/', create_post_api, name='create_post_api'),  # For serving media files
    path('register/', register, name='register')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
