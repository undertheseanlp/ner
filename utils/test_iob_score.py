from unittest import TestCase

from utils.scorer import iob_score


class TestIob_score(TestCase):
    def test_iob_score_1(self):
        y_true = [["O", "O", "B-ORG", "I-ORG"]]
        y_pred = [["O", "O", "B-ORG", "I-ORG"]]
        score = iob_score(y_true, y_pred)
        self.assertEqual(score, 1)

    def test_iob_score_2(self):
        y_true = [["O", "O", "B-ORG", "I-ORG", "O"]]
        y_pred = [["O", "O", "B-ORG", "I-ORG", "O"]]
        score = iob_score(y_true, y_pred)
        self.assertEqual(score, 1)

    def test_iob_score_3(self):
        y_true = [["O", "O", "B-ORG", "I-ORG", "O"]]
        y_pred = [["O", "O", "B-ORG", "O", "O"]]
        score = iob_score(y_true, y_pred)
        self.assertEqual(score, 0)

    def test_iob_score_4(self):
        y_true = [["B-LOC", "O", "B-ORG", "I-ORG", "O"]]
        y_pred = [["B-LOC", "O", "B-ORG", "O", "O"]]
        score = iob_score(y_true, y_pred)
        self.assertEqual(score, 0.5)

