from django.urls import path

from urlshortener.views import LinkPairView, link_redirect, get_request_count, enter_password, get_referers_count

urlpatterns = [
    path('url', LinkPairView.as_view()),
    path('url/<str:alias>', link_redirect),
    path('url/<str:alias>/password/', enter_password, name='password-form'),
    path('url/<str:alias>/request-count', get_request_count),
    path('url/<str:alias>/referers-top', get_referers_count),
]
