import random
from card import Card

class Deck:
    """specifies a deck consisting of Card objects for use in play"""

    def __init__(self, value_start, value_end, number_of_suits):
        self.value_start = value_start
        self.value_end = value_end
        self.nbr_suits = number_of_suits
        self.list_of_cards = []
        self.stack_of_rev_value = ['', '', '', '']
        self.list_of_value = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'X', 'J', 'Q', 'K']
        self.list_of_suit = ['C', 'D', 'H', 'S']

# create deck for arbitrary number of suits
    def create_deck(self):
        if self.nbr_suits <= len(self.list_of_suit):
            for i in range(0, self.nbr_suits):
                for j in range(self.value_start - 1, self.value_end):
                    x = Card(self.list_of_value[j], self.list_of_suit[i])
                    self.list_of_cards.append(x)
        else:
            for loop in range(0, self.nbr_suits // len(self.list_of_suit)):
                for i in range(0, len(self.list_of_suit)):
                    for j in range(self.value_start - 1, self.value_end):
                        x = Card(self.list_of_value[j], self.list_of_suit[i])
                        self.list_of_cards.append(x)
            for i in range(0, self.nbr_suits % len(self.list_of_suit)):
                for j in range(self.value_start - 1, self.value_end):
                    x = Card(self.list_of_value[j], self.list_of_suit[i])
                    self.list_of_cards.append(x)

    def shuffle(self):
        seed1 = random.randint(0, len(self.list_of_cards))//2
        seed2 = seed1 + random.randint(0, len(self.list_of_cards))
        seed3 = seed2 + random.randint(0, len(self.list_of_cards))
        temp_card = 0
        shuffled_deck = self.list_of_cards
        temp_card = shuffled_deck[0]
        shuffled_deck[0] = shuffled_deck[seed1]
        shuffled_deck[seed1] = temp_card
        while seed2 > 0:
            for i in range(1, len(shuffled_deck)):
                for j in range(1, len(shuffled_deck) - i):
                    temp_card = shuffled_deck[i]
                    shuffled_deck[i] = shuffled_deck[j]
                    shuffled_deck[j] = temp_card

            seed2 -= 1
        while seed3 > 0:
            for i in range(1, len(shuffled_deck)):
                for j in range(1, len(shuffled_deck) - i):
                    temp_card = shuffled_deck[-i]
                    shuffled_deck[-i] = shuffled_deck[-j]
                    shuffled_deck[-j] = temp_card

            seed3 -= 1

    def add(self, value, suit):
        new_card = Card(value, suit)
        self.list_of_cards.append(new_card)

    def draw(self):
        return self.list_of_cards.pop()

    def get_value_start(self):
        return self.value_start

    def get_value_end(self):
        return self.value_end

    def get_nbr_suits(self):
        return self.nbr_suits

    def get_list_of_value(self):
        return self.list_of_value

    def get_list_of_suit(self):
        return self.list_of_suit

    def get_list_of_cards(self):
        return self.list_of_cards

    def get_stack_of_rev_value(self):
        rep = []
        for i in range(0, len(self.stack_of_rev_value)):
            if isinstance(self.stack_of_rev_value[i], str):
                rep.append(self.stack_of_rev_value[i])
            else:
                rep.append(self.stack_of_rev_value[i].peek())

        return rep

    def set_value_start(self, value):
        self.value_start = value

    def set_value_end(self, value):
        self.value_end = value

    def set_nbr_suits(self, suits):
        self.nbr_suits = suits

    def set_list_of_value(self, value, position):
        position = position - 1
        self.list_of_value[position] = value

    def set_list_of_suit(self, value, position):
        position = position - 1
        self.list_of_suit[position] = value

    def set_list_of_cards(self, value, suit, position):
        position = position - 1
        self.list_of_cards[position] = Card(value, suit)

# only works if decks are not shuffled
    def __eq__(self, other):
        count = 0
        if len(self.list_of_cards) == len(other.list_of_cards):
            for i in range (0, len(self.list_of_cards)):
                if self.list_of_cards[i] == other.list_of_cards[i]:
                    count = count + 1
            if count == len(self.list_of_cards):
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        deck_rep = ''
        for card in range(0, len(self.list_of_cards)):
            deck_rep += str(self.list_of_cards[card]) + '\n'

        return deck_rep




# do = Deck(1,13,8)
# do.set_list_of_suit('C',2)
# do.set_list_of_suit('C',3)
# do.set_list_of_suit('C',4)

# do.create_deck()
# print(do)

# do1 = Deck(1,13,4)
# do1.create_deck()
# do1.shuffle()
# do1.get_stack_of_rev_value()
# print(do1)

# do1=Deck(1,13,6)
# do1.shuffle()
# do1.add('K','G')
# for i in range (0,40):
#     draw_card=do1.draw()
#     print('drawn card:',draw_card)

# for k in range(0,len(do1.list_of_cards)):
#     print(do1.list_of_cards[k])

# print("New list")
# for k in range(0,len(do1.list_of_cards)):
#    print(do1.list_of_ref_cards[k])
