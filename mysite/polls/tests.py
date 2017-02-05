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