from django.conf import settings
from django.conf.urls import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('project.bikes.urls')),
    path('', include('project.goals.urls')),
    path('', include('project.reports.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    from django.views.defaults import server_error, page_not_found, permission_denied

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path('403/', permission_denied, kwargs={'exception': Exception("Permission Denied")}, name='error403'),
        path('404/', page_not_found, kwargs={'exception': Exception("Page not Found")}, name='error404'),
        path('500/', server_error, name='error500'),
    ]
    urlpatterns += static.static(settings.MEDIA_URL,
                                 document_root=settings.MEDIA_ROOT)

