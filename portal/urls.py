"""portal URL Configuration"""

from django.conf.urls import url
from . import views

app_name = 'portal'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<lit_type_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<lit_type_id>[0-9]+)/contribute/$', views.contribute, name='contribute'),
    url(r'^contribute/$', views.contribute, name='contribute'),
    url(r'^contribute_b/$', views.contribute_b, name='contribute_b'),
    url(r'^literature/(?P<filter_by>[a-zA_Z]+)/$', views.literatures, name='literature'),
    url(r'^terms/$', views.termsandcondition, name='terms'),
]