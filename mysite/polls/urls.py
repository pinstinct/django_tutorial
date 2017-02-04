# url 패키지에서 urls 모듈을 import
from django.conf.urls import url
# 작성한 views.py 파일을 import
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
]
