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
        self.assertEqual(cribbage.scoring.score_hand(self.hand_67899), 20)
        self.assertEqual(cribbage.scoring.score_hand(self.hand_Q9T8J), 5)

    def test_stack_sum(self):
        stack = []
        self.assertEqual(cribbage.scoring.stack_sum(stack), 0)
        stack.append(Card(5, "H"))
        self.assertEqual(cribbage.scoring.stack_sum(stack), 5)
        stack.append(Card(12, "D"))
        self.assertEqual(cribbage.scoring.stack_sum(stack), 15)

    def test_score_stack(self):
        stack = []
        with self.assertRaises(RuntimeError):
            cribbage.scoring.score_stack(stack)

        stack.append(Card(2, "H"))
        self.assertEqual(cribbage.scoring.score_stack(stack), 0)

        # 2H 2D --> pair scores 2
        stack.append(Card(2, "D"))
        self.assertEqual(cribbage.scoring.score_stack(stack), 2)

        # 2H 2D 2S --> three of a kind scores 6
        stack.append(Card(2, "S"))
        self.assertEqual(cribbage.scoring.score_stack(stack), 6)

        # 2H 2D 2S 2C --> four of a kind scores 12
        stack.append(Card(2, "C"))
        self.assertEqual(cribbage.scoring.score_stack(stack), 12)

        # 2H 2D 2S 2C 7H --> 15 = scores 2
        stack.append(Card(7, "H"))
        self.assertEqual(cribbage.scoring.score_stack(stack), 2)

        # 2H 2D 2S 2C 7H 6H --> 21 = no score
        stack.append(Card(6, "H"))
        self.assertEqual(cribbage.scoring.score_stack(stack), 0)

        # 2H 2D 2S 2C 7H 6H 5H --> 26 = run of 3
        stack.append(Card(5, "H"))
        self.assertEqual(cribbage.scoring.score_stack(stack), 3)

        # 2H 2D 2S 2C 7H 6H 5H 4H --> 30 = run of 4
        stack.append(Card(4, "H"))
        self.assertEqual(cribbage.scoring.score_stack(stack), 4)

        # 2H 2D 2S 2C 7H 6H 5H 4H AH --> 31 = 2 points
        stack.append(Card(1, "H"))
        self.assertEqual(cribbage.scoring.score_stack(stack), 2)

        stack = []
        stack.append(Card(4, "H"))
        self.assertEqual(cribbage.scoring.score_stack(stack), 0)
        stack.append(Card(6, "H"))
        self.assertEqual(cribbage.scoring.score_stack(stack), 0)
        stack.append(Card(5, "H"))
        # 15 + run of 3
        self.assertEqual(cribbage.scoring.score_stack(stack), 5)
        stack.append(Card(5, "D"))
        self.assertEqual(cribbage.scoring.score_stack(stack), 2)
        # 4 6 5 5 3 -> should not be another run
        stack.append(Card(3, "D"))
        self.assertEqual(cribbage.scoring.score_stack(stack), 0)
        # 4 6 5 5 3 4 -> should a run of 3 (and no more)
        stack.append(Card(4, "D"))
        self.assertEqual(cribbage.scoring.score_stack(stack), 3)


if __name__ == "__main__":
    unittest.main()
