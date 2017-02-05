# url 패키지에서 urls 모듈을 import
from django.conf.urls import url
# 작성한 views.py 파일을 import
from . import views

app_name = 'polls'
urlpatterns = [
        # /polls/
        url(r'^$', views.index, name='index'),
        # /polls/5
        url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
        # /polls/5/results/
        url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
        # /polls/5/vote/
        url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),        
]
