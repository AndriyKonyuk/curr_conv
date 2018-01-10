from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.main_page, name='web'),
    url(r'^test$', views.return_json, name='test_return'),
    url(r'^db$', views.db_page, name='db_page'),
]