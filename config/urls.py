from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from spotipie.views import base_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('spotipie/', include('spotipie.urls')),
    path('common/', include('common.urls')),
    path('', base_views.index, name='index')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
