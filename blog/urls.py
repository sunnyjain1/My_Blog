from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.BlogIndex.as_view(), name="index"),
    url(r'^features/$', views.features.as_view(), name="features"),
    url(r'^register/$', views.register.as_view(), name="register"),
    url(r'^login/$', views.Login.as_view(), name="login"),
    url(r'^search/$', views.search, name="search"),
    url(r'^logout/$', views.Logout.as_view(), name="logout"),
    url(r'^request/$', views.req.as_view(), name="req"),
    url(r'^authenticate/$', views.Authen.as_view(), name="authen"),
    url(r'^message/$', views.message, name="msg"),
    url(r'^send/$', views.send.as_view(), name="snt"),
    url(r'^entry/(?P<slug>\S+)/', views.BlogDetail, name="entry_detail"),
)
