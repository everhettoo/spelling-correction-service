from unittest import TestCase

from schemas import ReviewResponse


class TestReviewResponse(TestCase):
    def test_process(self):
        text = "Bart is actually ax good boy."
        res = ReviewResponse(text, text.split(' '))
        res.process()
