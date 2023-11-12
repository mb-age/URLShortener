from django.urls import path
from urlshortener.views import LinkPairView, link_redirect

urlpatterns = [
    path('link-pair', LinkPairView.as_view()),
    path('my-domain/<str:alias>', link_redirect),
]
