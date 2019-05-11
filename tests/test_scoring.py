import unittest

from cribbage.card import Card
import cribbage.scoring


class TestScoring(unittest.TestCase):
    def setUp(self):
        self.deck = Card.build_deck()
        self.all_clubs = self.deck[:13]
        self.all_diamonds = self.deck[13:26]
        self.all_hearts = self.deck[26:39]
        self.all_spades = self.deck[39:]
        self.hand_5555 = [Card(5, "C"), Card(
            5, "D"), Card(5, "H"), Card(5, "S")]
        self.hand_6789_suited = [Card(6, "C"), Card(
            7, "C"), Card(8, "C"), Card(9, "C")]
        self.hand_Q9T8J = [Card(12, "C"), Card(9, "S"), Card(
            10, "D"), Card(8, "C"), Card(11, "D")]
        self.hand_67899 = [
            Card(6, "C"),
            Card(7, "C"),
            Card(8, "C"),
            Card(9, "C"),
            Card(9, "H"),
        ]
        self.hand_77889 = [
            Card(7, "C"),
            Card(7, "H"),
            Card(8, "C"),
            Card(8, "D"),
            Card(9, "S"),
        ]
        self.hand_TJQK_unsuited = [
            Card(10, "C"),
            Card(11, "S"),
            Card(13, "D"),
            Card(12, "C"),
        ]

    def test_flush_check(self):
        self.assertTrue(cribbage.scoring.flush_check(self.all_clubs[0:5]))
        self.assertTrue(cribbage.scoring.flush_check(self.all_clubs))
        self.assertTrue(cribbage.scoring.flush_check(self.all_diamonds[0:5]))
        self.assertTrue(cribbage.scoring.flush_check(self.all_diamonds))
        self.assertTrue(cribbage.scoring.flush_check(self.all_hearts[0:5]))
        self.assertTrue(cribbage.scoring.flush_check(self.all_hearts))
        self.assertTrue(cribbage.scoring.flush_check(self.all_spades[0:5]))
        self.assertFalse(cribbage.scoring.flush_check(self.deck))
        self.assertFalse(cribbage.scoring.flush_check(self.hand_5555))
        self.assertTrue(cribbage.scoring.flush_check(self.hand_6789_suited))
        self.assertFalse(cribbage.scoring.flush_check(self.hand_77889))
        self.assertFalse(cribbage.scoring.flush_check(self.hand_TJQK_unsuited))

    def test_pair_count(self):
        self.assertEqual(cribbage.scoring.pair_count(self.deck), 78)
        self.assertEqual(cribbage.scoring.pair_count(self.all_clubs), 0)
        self.assertEqual(cribbage.scoring.pair_count(
            self.all_diamonds + self.all_hearts), 13)
        self.assertEqual(cribbage.scoring.pair_count(self.hand_5555), 6)
        self.assertEqual(cribbage.scoring.pair_count(self.hand_6789_suited), 0)
        self.assertEqual(cribbage.scoring.pair_count(self.hand_77889), 2)
        self.assertEqual(cribbage.scoring.pair_count(
            self.hand_TJQK_unsuited), 0)

    def test_fifteen_count(self):
        self.assertEqual(cribbage.scoring.fifteen_count(self.deck[0:3]), 0)
        self.assertEqual(cribbage.scoring.fifteen_count(self.deck[0:5]), 1)
        self.assertEqual(cribbage.scoring.fifteen_count(self.hand_5555), 4)
        self.assertEqual(cribbage.scoring.fifteen_count(
            self.hand_6789_suited), 2)
        self.assertEqual(cribbage.scoring.fifteen_count(self.hand_77889), 4)
        self.assertEqual(cribbage.scoring.fifteen_count(
            self.hand_TJQK_unsuited), 0)
        self.assertEqual(cribbage.scoring.fifteen_count(self.hand_5555), 4)

    def test_check_if_run(self):
        self.assertTrue(cribbage.scoring._check_if_run([1, 2, 3, 4, 5]))
        self.assertTrue(cribbage.scoring._check_if_run([5, 4, 3, 2, 1]))
        self.assertFalse(cribbage.scoring._check_if_run([1, 2]))
        self.assertTrue(cribbage.scoring._check_if_run([2, 1, 3]))
        self.assertFalse(cribbage.scoring._check_if_run([1, 2, 4]))

    def test_run_count(self):
        self.assertEqual(cribbage.scoring.run_count(self.hand_5555), 0)
        self.assertEqual(cribbage.scoring.run_count(self.hand_6789_suited), 4)
        self.assertEqual(cribbage.scoring.run_count(self.hand_77889), 12)
        self.assertEqual(cribbage.scoring.run_count(
            self.hand_TJQK_unsuited), 4)
        self.assertEqual(cribbage.scoring.run_count(self.hand_67899), 8)
        self.assertEqual(cribbage.scoring.run_count(self.hand_Q9T8J), 5)

    def test_score_hand(self):
        self.assertEqual(cribbage.scoring.score_hand(self.hand_5555), 20)
        self.assertEqual(cribbage.scoring.score_hand(
            self.hand_6789_suited), 12)
        self.assertEqual(cribbage.scoring.score_hand(self.hand_77889), 24)
        self.assertEqual(cribbage.scoring.score_hand(
            self.hand_TJQK_unsuited), 4)
        self.assertEqual(cribbage.scoring.score_hand(self.hand_67899), 16)
        self.assertEqual(cribbage.scoring.score_hand(self.hand_Q9T8J), 5)


if __name__ == "__main__":
    unittest.main()
