from __future__ import unicode_literals

from django.urls import re_path

from .views import Rate
from . import app_settings

from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from .views import FooView, SizesView


urlpatterns = [
    re_path(r'(?P<content_type_id>\d+)/(?P<object_id>' + app_settings.STAR_RATINGS_OBJECT_ID_PATTERN + ')/', Rate.as_view(), name='rate'),
    path('', FooView.as_view(template_name='home_copy.html'), name='home'),
    path('sizes', SizesView.as_view(), name='sizes'),
    #path('', include(auth_urls)),
    #path('admin/', admin.site.urls),
]

app_name = 'star_ratings'
