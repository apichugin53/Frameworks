from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView

from webapp import settings

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name="home"),
    path('admin/', admin.site.urls),
    path('auth/', include('security.urls', namespace='auth')),
    path('dogs/', include('dogs.urls', namespace='dogs')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('users/', include('users.urls', namespace='users')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if settings.USE_DEBUG_TOOLBAR:
        from debug_toolbar.toolbar import debug_toolbar_urls

        urlpatterns += debug_toolbar_urls()
