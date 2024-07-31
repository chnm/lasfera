from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"toponyms", views.ToponymViewSet, basename="toponyms")
router.register(r"toponym-detail", views.ToponymViewSet, basename="toponym-detail")
router.register(
    r"manuscript-detail", views.SingleManuscriptViewSet, basename="manuscript-detail"
)

urlpatterns = [
    path("", views.index, name="index"),
    path("manuscripts/", views.manuscripts, name="manuscripts"),
    path("manuscripts/<str:siglum>/", views.manuscript, name="manuscript"),
    path("toponyms/", views.toponyms, name="toponyms"),
    path("toponyms/<int:toponym_param>/", views.toponym, name="toponym_detail"),
    path("toponym-search/", views.search_toponyms, name="search_toponyms"),
    path("stanzas/", views.stanzas, name="stanzas"),
    path("api/", include(router.urls)),
]
