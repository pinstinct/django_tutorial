from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        최근 5개의 질문 반환합니다.
        (미래의 게시될 질문은 포함하지 않음)
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DeleteView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        index 페이지에 게시되지 않은 질문들은 제외합니다
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(genesric.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 폼을 다시 보여
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 데이터가 두번 포스트되는 것을 방지하기 위해,
        # 항상 POST 데이터를 성공적으로 처리한 후 HttpResponseRedirect 반환
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
