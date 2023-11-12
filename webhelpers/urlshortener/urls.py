from django.urls import path
from urlshortener.views import LinkPairView, link_redirect

urlpatterns = [
    path('url/create', LinkPairView.as_view()),
    path('url/<str:alias>', link_redirect),
]
