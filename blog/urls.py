from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.BlogIndex.as_view(), name="index"),
    url(r'^features/$', views.features.as_view(), name="features"),
    url(r'^register/$', views.register.as_view(), name="register"),
    url(r'^login/$', views.login.as_view(), name="login"),
    url(r'^search/$', views.search, name="search"),
    url(r'^message/$', views.message, name="msg"),
    url(r'^entry/(?P<slug>\S+)$', views.BlogDetail.as_view(), name="entry_detail"),
)
