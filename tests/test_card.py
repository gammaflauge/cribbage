import unittest

from cribbage.card import Card


class TestCard(unittest.TestCase):
    def setUp(self):
        self.deck = []
        for suit in ["C", "D", "H", "S"]:
            for rank in range(1, 14):
                self.deck.append(Card(rank, suit))

    def test_str(self):
        self.assertEqual(str(self.deck[0]), "AC")
        self.assertEqual(str(self.deck[1]), "2C")
        self.assertEqual(str(self.deck[12]), "KC")
        self.assertEqual(str(self.deck[13]), "AD")
        self.assertEqual(str(self.deck[17]), "5D")
        self.assertEqual(str(self.deck[23]), "JD")
        self.assertEqual(str(self.deck[26]), "AH")
        self.assertEqual(str(self.deck[33]), "8H")
        self.assertEqual(str(self.deck[35]), "TH")
        self.assertEqual(str(self.deck[50]), "QS")
        self.assertEqual(str(self.deck[51]), "KS")

    def test_build_deck(self):
        my_deck = Card.build_deck()
        for i, card in enumerate(my_deck):
            self.assertEqual(card.rank, self.deck[i].rank)
            self.assertEqual(card.suit, self.deck[i].suit)

    def test_eq(self):
        card_1 = Card(5, "H")
        card_2 = Card(5, "H")
        card_3 = Card(5, "S")
        card_4 = Card(6, "H")
        self.assertEqual(card_1, card_2)
        self.assertNotEqual(card_1, card_3)
        self.assertNotEqual(card_1, card_4)


if __name__ == "__main__":
    unittest.main()
