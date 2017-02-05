import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


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