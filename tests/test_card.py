import unittest

from card import Card


class TestCard(unittest.TestCase):
    def setUp(self):
        self.deck = []
        for suit in ['C', 'D', 'H', 'S']:
            for rank in range(1, 14):
                self.deck.append(Card(rank, suit))
        self.all_clubs = self.deck[:13]
        self.all_diamonds = self.deck[13:26]
        self.all_hearts = self.deck[26:39]
        self.all_spades = self.deck[39:]
        self.hand_5555 = [Card(5, 'C'), Card(5, 'D'),
                          Card(5, 'H'), Card(5, 'S')]
        self.hand_6789_suited = [Card(6, 'C'), Card(7, 'C'),
                                 Card(8, 'C'), Card(9, 'C')]
        self.hand_77889 = [Card(7, 'C'), Card(7, 'H'),
                           Card(8, 'C'), Card(8, 'D'),
                           Card(9, 'S')]
        self.hand_TJQK_unsuited = [Card(10, 'C'), Card(11, 'S'),
                                   Card(13, 'D'), Card(12, 'C')]

    def test_str(self):
        self.assertEqual(str(self.deck[0]), 'AC')
        self.assertEqual(str(self.deck[1]), '2C')
        self.assertEqual(str(self.deck[12]), 'KC')
        self.assertEqual(str(self.deck[13]), 'AD')
        self.assertEqual(str(self.deck[17]), '5D')
        self.assertEqual(str(self.deck[23]), 'JD')
        self.assertEqual(str(self.deck[26]), 'AH')
        self.assertEqual(str(self.deck[33]), '8H')
        self.assertEqual(str(self.deck[35]), 'TH')
        self.assertEqual(str(self.deck[50]), 'QS')
        self.assertEqual(str(self.deck[51]), 'KS')

    def test_flush_check(self):
        self.assertTrue(Card.flush_check(self.all_clubs[0:5]))
        self.assertTrue(Card.flush_check(self.all_clubs))
        self.assertTrue(Card.flush_check(self.all_diamonds[0:5]))
        self.assertTrue(Card.flush_check(self.all_diamonds))
        self.assertTrue(Card.flush_check(self.all_hearts[0:5]))
        self.assertTrue(Card.flush_check(self.all_hearts))
        self.assertTrue(Card.flush_check(self.all_spades[0:5]))
        self.assertFalse(Card.flush_check(self.deck))
        self.assertFalse(Card.flush_check(self.hand_5555))
        self.assertTrue(Card.flush_check(self.hand_6789_suited))
        self.assertFalse(Card.flush_check(self.hand_77889))
        self.assertFalse(Card.flush_check(self.hand_TJQK_unsuited))

    def test_pair_count(self):
        self.assertEqual(Card.pair_count(self.deck), 78)
        self.assertEqual(Card.pair_count(self.all_clubs), 0)
        self.assertEqual(Card.pair_count(
            self.all_diamonds + self.all_hearts), 13)
        self.assertEqual(Card.pair_count(self.hand_5555), 6)
        self.assertEqual(Card.pair_count(self.hand_6789_suited), 0)
        self.assertEqual(Card.pair_count(self.hand_77889), 2)
        self.assertEqual(Card.pair_count(self.hand_TJQK_unsuited), 0)

    def test_fifteen_count(self):
        self.assertEqual(Card.fifteen_count(self.deck[0:3]), 0)
        self.assertEqual(Card.fifteen_count(self.deck[0:5]), 1)
        self.assertEqual(Card.fifteen_count(self.hand_5555), 4)
        self.assertEqual(Card.fifteen_count(self.hand_6789_suited), 2)
        self.assertEqual(Card.fifteen_count(self.hand_77889), 4)
        self.assertEqual(Card.fifteen_count(self.hand_TJQK_unsuited), 0)
        self.assertEqual(Card.fifteen_count(self.hand_5555), 4)

    def test_run_count(self):
        self.assertEqual(Card.run_count(self.hand_5555), 0)
        self.assertEqual(Card.run_count(self.hand_6789_suited), 4)
        self.assertEqual(Card.run_count(self.hand_77889), 12)
        self.assertEqual(Card.run_count(self.hand_TJQK_unsuited), 4)


if __name__ == "__main__":
    unittest.main()
