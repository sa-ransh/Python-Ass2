class Card:
    """specifies a card"""

    def __init__(self, value, suit):
        self.card_face = value
        self.card_suit = suit
        if self.card_suit == 'C' or self.card_suit == 'S':
            self.card_colour = 1
            if self.card_suit == 'C':
                self.card_suit_nbr = 1
            if self.card_suit == 'S':
                self.card_suit_nbr = 4
        if self.card_suit == 'D' or self.card_suit == 'H':
            self.card_colour = 0
            if self.card_suit == 'D':
                self.card_suit_nbr = 2
            if self.card_suit == 'H':
                self.card_suit_nbr = 3

    def __str__(self):
        return self.card_face + '~' + self.card_suit

    def __eq__(self, other):
        if self.card_face == other.card_face and self.card_suit == other.card_suit:
            return True
        else:
            return False

    def get_face(self):
        return self.card_face

    def get_suit(self):
        return self.card_suit

    def get_colour(self):
        return self.card_colour

    def get_card_suit_nbr(self):
        return self.card_suit_nbr

    def set_face(self, value):
        self.card_face = value

    def set_suit(self, suit):
        self.card_suit = suit

    def set_colour(self, colour):
        self.card_colour = colour

    def set_card_suit_nbr(self, number):
        self.card_suit_nbr = number