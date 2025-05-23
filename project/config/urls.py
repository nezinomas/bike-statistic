from django.conf import settings
from django.conf.urls import static
from django.urls import include, path
from django.views.defaults import page_not_found, permission_denied, server_error

from ..data.views import DataList as IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("", include("project.users.urls")),
    path("", include("project.bikes.urls")),
    path("goals/", include("project.goals.urls")),
    path("data/", include("project.data.urls")),
    path("reports/", include("project.reports.urls")),
]

urlpatterns += [
    path(
        "403/",
        permission_denied,
        kwargs={"exception": Exception("Permission Denied")},
        name="error403",
    ),
    path(
        "404/",
        page_not_found,
        kwargs={"exception": Exception("Page not Found")},
        name="error404",
    ),
    path("500/", server_error, name="error500"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static.static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
