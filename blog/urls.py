from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.BlogIndex.as_view(), name="index"),
    url(r'^features/$', views.features.as_view(), name="features"),
    url(r'^press/$', views.press.as_view(), name="press"),
    url(r'^hires/$', views.hires.as_view(), name="hires"),
    url(r'^about/$', views.about.as_view(), name="about"),
    url(r'^entry/(?P<slug>\S+)$', views.BlogDetail.as_view(), name="entry_detail"),
)
