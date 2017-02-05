import datetime

from django.urls import reverse
from django.test import TestCase
from django.utils import timezone


from .models import Question


def create_question(question_text, days):
    """
    question_text, days를 받아 질문(question)을 생성합니다.
    :param question_text: 질문
    :param days: 날짜 offset(과거에 발행된 질문은 -, 아직 발행되지 않은 질문은 +)
    :return: Question 객체 생성
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionViewTest(TestCase):

    def test_index_view_with_no_questions(self):
        """
        질문이 없으면 적절한 메시지를 출력합니다.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        과거 pub_date를 가진 질문은 index 페이지에 보여줍니다.
        """
        create_question(question_text='Past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )

    def test_index_view_with_a_future_question(self):
        """
        미래 pub_date를 가진 질문은 index 페이지에 보여주지 않습니다.
        """
        create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_question_and_past_question(self):
        """
        과거와 미래 질문 모두 있더라도, 오직 과거 질문만 보여줍니다.
        """
        create_question(question_text='Past question', days=-30)
        create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        index 페이지에 여러개의 질문을 보여줍니다.
        """
        create_question(question_text='Past question 1.', days=-30)
        create_question(question_text='Past question 2.', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        미래의 pub_date를 가진 질문의 detail 뷰는 '404 not found'를 반환합니다.
        :return: 404 not found
        """
        future_question = create_question(question_text='Future question', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        과거의 pub_date를 가진 질문의 detail 뷰는 질문 내용을 반환합니다.
        """
        past_question = create_question(question_text='Past Question', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        pub_date 값이 미래의 날짜라면,
        was_published_recently()는 False를 반환해야 합니다.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        pub_date 값이 하루 이상 과거의 날짜라면,
        was_published_recently()는 False를 반환해야 합니다.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        pub_date 값이 하루 이내라면,
        was_published_recently()는 True를 반환해야 합니다.
        :return:
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)