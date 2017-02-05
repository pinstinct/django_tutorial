from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Choice, Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
            'latest_question_list':latest_question_list,
            }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You're lookin at the result of question %s."
    return HttpResponse(response % question_id)


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


