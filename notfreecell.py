#please read the report to understand design choices and the some complicated parts within the methods used in this class. Thank you.
import os
from stack import Stack
from card import Card
from deck import Deck

class NotFreecell:
    '''implements rules of the freecell game using deck class'''

    def __init__(self):
        self.list_of_cell_slots = ['[ ]', '[ ]', '[ ]', '[ ]']
        self.list_of_suit_stacks = ['[ ]', '[ ]', '[ ]', '[ ]']
        for suit in range(0, len(self.list_of_suit_stacks)):
            self.list_of_suit_stacks[suit] = Stack()
            self.list_of_suit_stacks[suit].push('[ ]')
        self.deck_in_play = Deck(1, 13, 2)

        self.value_stack = ['', '', '', '']
        for suit in range(0, len(self.list_of_suit_stacks)):
            self.value_stack[suit] = Stack()
            self.deck_in_play.stack_of_rev_value[suit] = Stack()
            for value in range(0, len(self.deck_in_play.list_of_value)):
                self.value_stack[suit].push(self.deck_in_play.list_of_value[value])
            while not self.value_stack[suit].is_empty():
                self.deck_in_play.stack_of_rev_value[suit].push(self.value_stack[suit].pop())
        # how many cards per suit: op1
        self.op1 = self.deck_in_play.value_end - self.deck_in_play.value_start + 1
        # total cards in play: op2
        self.op2 = self.op1 * self.deck_in_play.nbr_suits
        # cascades required to arrange all cards: op3
        if self.op2 % 8 != 0:
            self.op3 = self.op2 // 8 + 1
        else:
            self.op3 = self.op2 // 8
        # total cascades required for playing the game: op4
        # create empty cascade with worst case possibility ie K in row 7 initially for a standard deck of 52 cards
        self.op4 = self.op3 + self.op1 - 1
        self.cascade = []
        self.size = self.op4
        self.empty = ' '

        i = 0
        while i < self.size:
            self.cascade.append([self.empty] * 8)
            i = i + 1

    def new_game(self):
        place_card = 0
        while place_card < len(self.deck_in_play.list_of_cards):
            self.cascade[place_card // 8][place_card % 8] = self.deck_in_play.list_of_cards[place_card]
            place_card = place_card + 1

    def linear_search(self, the_list, target_item):
        n = len(the_list)
        for i in range(n):
            if the_list[i] == target_item:
                return i
        return False

    def move_card_cascade(self, face, suit, to_face, to_suit):

        card_to_move = Card(face, suit)
        card_dest = Card(to_face, to_suit)
        for i in range(0, self.size):
            for j in range(0, 8):
                if isinstance(self.cascade[i][j], str):
                    pass
                elif card_to_move == self.cascade[i][j] and isinstance(self.cascade[i + 1][j], str):
                    store_card = self.cascade[i][j]
                    for k in range(0, self.size):
                        for l in range(0, 8):
                            if isinstance(self.cascade[k][l], str):
                                pass
                            elif card_dest == self.cascade[k][l] and isinstance(self.cascade[k + 1][l], Card):
                                if self.cascade[k + 1][l] != store_card:
                                    print('Invalid Move')
                            elif card_dest == self.cascade[k][l] and isinstance(self.cascade[k + 1][l], str):
                                if (card_to_move.card_colour == 0 and card_dest.card_colour == 1) or (
                                        card_to_move.card_colour == 1 and card_dest.card_colour == 0):
                                    if self.linear_search(self.deck_in_play.list_of_value,card_to_move.card_face) == self.linear_search(self.deck_in_play.list_of_value, card_dest.card_face) - 1:
                                        self.cascade[k + 1][l] = store_card
                                        self.cascade[i][j] = ' '
                                    else:
                                            print('Invalid Move')
                                else:
                                    print('Invalid Move')
                elif card_to_move == self.cascade[i][j] and isinstance(self.cascade[i + 1][j], Card):
                    print('Invalid Card')

    def move_card_to_cell(self, face, suit, cell_slot):
        cell_slot = cell_slot - 1
        card_to_move = Card(face, suit)
        if isinstance(self.list_of_cell_slots[cell_slot], str):
            for i in range(0, self.size):
                for j in range(0, 8):
                    if isinstance(self.cascade[i][j], str):
                        pass
                    elif card_to_move == self.cascade[i][j] and isinstance(self.cascade[i + 1][j], str):
                        store_card = self.cascade[i][j]
                        self.cascade[i][j] = ' '
                        self.list_of_cell_slots[cell_slot] = store_card
        else:
            print('Slot is not empty')

    def move_card_from_cell(self, cell_slot, to_face, to_suit):
        cell_slot = cell_slot - 1
        card_dest = Card(to_face, to_suit)
        if not isinstance(self.list_of_cell_slots[cell_slot], str):
            for k in range(0, self.size):
                for l in range(0, 8):
                    if isinstance(self.cascade[k][l], str):
                        pass
                    elif card_dest == self.cascade[k][l] and isinstance(self.cascade[k + 1][l], Card):
                        if self.cascade[k + 1][l] != self.list_of_cell_slots[cell_slot]:
                            print('Invalid Move')
                    elif card_dest == self.cascade[k][l] and isinstance(self.cascade[k + 1][l], str):
                        if (self.list_of_cell_slots[cell_slot].card_colour == 0 and card_dest.card_colour == 1) or (
                                self.list_of_cell_slots[cell_slot].card_colour == 1 and card_dest.card_colour == 0):
                            if (self.linear_search(self.deck_in_play.list_of_value,
                                                   self.list_of_cell_slots[cell_slot].card_face) == self.linear_search(
                                    self.deck_in_play.list_of_value, card_dest.card_face) - 1):
                                self.cascade[k + 1][l] = self.list_of_cell_slots[cell_slot]
                                self.list_of_cell_slots[cell_slot] = '[ ]'
                            else:
                                print('Invalid Move')

                        else:
                            print('Invalid Move')

    def move_to_foundation(self, face, suit):
        card_to_move = Card(face, suit)
        if card_to_move.card_face == self.deck_in_play.stack_of_rev_value[card_to_move.card_suit_nbr - 1].peek():

            for i in range(0, self.size):
                for j in range(0, 8):
                    if isinstance(self.cascade[i][j], str):
                        pass
                    elif card_to_move == self.cascade[i][j] and isinstance(self.cascade[i + 1][j], str):
                        self.list_of_suit_stacks[card_to_move.card_suit_nbr - 1].push(card_to_move)
                        self.deck_in_play.stack_of_rev_value[card_to_move.card_suit_nbr - 1].pop()
                        self.cascade[i][j] = ' '
        else:
            print('Invalid Card')

    def move_from_foundation(self, suit, to_face, to_suit):
        card_dest = Card(to_face, to_suit)
        if not isinstance(self.list_of_suit_stacks[suit - 1].peek(), str):
            for k in range(0, self.size):
                for l in range(0, 8):
                    if isinstance(self.cascade[k][l], str):
                        pass
                    elif card_dest == self.cascade[k][l] and isinstance(self.cascade[k + 1][l], Card):
                        if self.cascade[k + 1][l] != self.list_of_suit_stacks[suit - 1].peek():
                            print('Invalid Move')
                    elif card_dest == self.cascade[k][l] and isinstance(self.cascade[k + 1][l], str):
                        if (self.list_of_suit_stacks[
                                    suit - 1].peek().card_colour == 0 and card_dest.card_colour == 1) or (
                                self.list_of_suit_stacks[
                                        suit - 1].peek().card_colour == 1 and card_dest.card_colour == 0):
                            if (self.linear_search(self.deck_in_play.list_of_value, self.list_of_suit_stacks[
                                    suit - 1].peek().card_face) == self.linear_search(self.deck_in_play.list_of_value,
                                                                                      card_dest.card_face) - 1):
                                self.deck_in_play.stack_of_rev_value[suit - 1].push(
                                    self.list_of_suit_stacks[suit - 1].peek().card_face)
                                self.cascade[k + 1][l] = self.list_of_suit_stacks[suit - 1].pop()
                            else:
                                print('Invalid Move')
                        else:
                            print('Invalid Move')

    def move_from_cell_to_foundation(self, cell_slot):
        cell_slot = cell_slot - 1
        if not isinstance(self.list_of_cell_slots[cell_slot], str):
            if (self.list_of_cell_slots[cell_slot].card_face == self.deck_in_play.stack_of_rev_value[
                    self.list_of_cell_slots[cell_slot].card_suit_nbr - 1].peek()):
                self.list_of_suit_stacks[self.list_of_cell_slots[cell_slot].card_suit_nbr - 1].push(
                    self.list_of_cell_slots[cell_slot])
                self.deck_in_play.stack_of_rev_value[self.list_of_cell_slots[cell_slot].card_suit_nbr - 1].pop()
                self.list_of_cell_slots[cell_slot] = '[ ]'

            else:
                print('Invalid Card')

    def move_to_empty_cascade(self, value, suit, cascade_slot=0):
        cslot = cascade_slot - 1
        card_to_move = Card(value, suit)
        if cascade_slot != 0:
            if isinstance(self.cascade[0][cslot], str):
                for i in range(0, self.size):
                    for j in range(0, 8):
                        if isinstance(self.cascade[i][j], str):
                            pass
                        elif card_to_move == self.cascade[i][j] and isinstance(self.cascade[i + 1][j], str):
                            self.cascade[i][j] = ' '
                            self.cascade[0][cslot] = card_to_move
                for slot in range(0, len(self.list_of_cell_slots)):
                    if isinstance(self.list_of_cell_slots[slot], str):
                        pass
                    elif self.list_of_cell_slots[slot] == card_to_move:
                        self.list_of_cell_slots[slot] = '[ ]'
                        self.cascade[0][cslot] = card_to_move
                for slot in range(0, len(self.list_of_suit_stacks)):
                    if isinstance(self.list_of_suit_stacks[slot].peek(), str):
                        pass
                    elif self.list_of_suit_stacks[slot].peek() == card_to_move:
                        self.deck_in_play.stack_of_rev_value[card_to_move.card_suit_nbr - 1].push(
                            self.list_of_suit_stacks[card_to_move.card_suit_nbr - 1].peek().card_face)
                        self.cascade[0][cslot] = self.list_of_suit_stacks[card_to_move.card_suit_nbr - 1].pop()
            else:
                print('Slot not empty')

    def __str__(self):
        cascade_string = ''
        for item in self.list_of_cell_slots:
            cascade_string += str(item) + '\t'
        for item in range(0, len(self.list_of_suit_stacks)):
            cascade_string += str(self.list_of_suit_stacks[item].peek()) + '\t'
        cascade_string.strip('\t')
        cascade_string += '\n'
        cascade_string += '-----------------------------------------------------------\n'
        for row in self.cascade:
            for item in row:
                cascade_string += str(item) + '\t'  # whats str(item)
            cascade_string.strip('\t')
            cascade_string += '\n'
        cascade_string += '-----------------------------------------------------------'
        return cascade_string






def main():
    i = 0
    while i < 1:
        user_input = str(input("Press P to play or Q to quit:"))
        if user_input.upper() == 'P':
            f1=NotFreecell()
            f1.deck_in_play.create_deck()
            f1.deck_in_play.shuffle()
            f1.new_game()
            print(f1)
            j = 0
            while j < 1:
                count = f1.size * 8 + 4
                for row in range(0, f1.size):
                    for column in range(0, 8):
                        if isinstance(f1.cascade[row][column], str):
                            count = count - 1
                        else:
                            pass
                for slots in range (0, len(f1.list_of_cell_slots)):
                    if isinstance(f1.list_of_cell_slots[slots], str):
                        count = count - 1
                    else:
                        pass
                if count == 0:
                    print("\n\nCongratulations!!! You Won!")
                    input("Press Enter to exit")
                    j=1
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f1)
                move_input = str(input("Press M to select move or Q to quit: "))


                if move_input.upper() == 'M':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f1)
                    print("1. Move card to cascade slot")
                    print("2. Move card to free cell slot")
                    print("3. Move card to foundation")
                    next_move = input("Choose option to move:")
                    if next_move == '1':
                        k=0
                        while k < 1:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(f1)
                            print("1. Move card from one cascade slot to another")
                            print("2. Move card from cell to cascade slot")
                            print("3. Move card from foundation to cascade slot")
                            print("4. Move card to empty cascade slot")
                            move_cascade = input("Choose option to move card:")
                            if move_cascade == '1':
                                mcard_face = input("select card value to be moved:")
                                mcard_suit = input("select card suit to be moved:")
                                dcard_face = input("select card value of destination")
                                dcard_suit = input("select card suit of destination")
                                f1.move_card_cascade(mcard_face.upper(), mcard_suit.upper(), dcard_face.upper(), dcard_suit.upper())
                                k = 1
                            elif move_cascade == '2':
                                x=0
                                while x<1:
                                    try:
                                        cell = int(input("select cell slot (1-4):"))
                                        x=1
                                    except(ValueError):
                                        print('Oops, please enter an integer')
                                dcard_face = input("select card value of destination")
                                dcard_suit = input("select card suit of destination")
                                if cell < 5:
                                    f1.move_card_from_cell(cell,dcard_face.upper(), dcard_suit.upper())
                                    k = 1
                            elif move_cascade == '3':
                                x=0
                                while x<1:
                                    try:
                                        foundation = int(input("select foundation slot (1-4):"))
                                        x=1
                                    except(ValueError):
                                        print('Oops, please enter an integer')

                                dcard_face = input("select card value of destination")
                                dcard_suit = input("select card suit of destination")
                                if foundation < 5:
                                    f1.move_from_foundation(foundation, dcard_face.upper(), dcard_suit.upper())
                                    k = 1
                            elif move_cascade == '4':
                                mcard_face = input("select card value to be moved:")
                                mcard_suit = input("select card suit to be moved:")
                                x=0
                                while x<1:
                                    try:
                                        cslot = int(input("select empty cascade slot (1-8):"))
                                        x=1
                                    except(ValueError):
                                        print('Oops, please enter an integer')

                                if(cslot < 9):
                                    f1.move_to_empty_cascade(mcard_face.upper(), mcard_suit.upper(), cslot)
                                    k=1

                    elif next_move == '2':
                        l=0
                        while l < 1:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(f1)
                            print("1. Move card from cascade to free cell slot")
                            # print("2. Move card from foundation to free cell slot")
                            # print("3. Move card from one free cell slot to another")
                            move_cell = input("Choose option to move card:")
                            if move_cell == '1':

                                mcard_face = input("select card value to be moved:")
                                mcard_suit = input("select card suit to be moved:")
                                x=0
                                while x<1:
                                    try:
                                        cell = int(input("select cell slot (1-4):"))
                                        x=1
                                    except(ValueError):
                                        print('Oops, please enter an integer')

                                if(cell < 5):
                                    f1.move_card_to_cell(mcard_face.upper(), mcard_suit.upper(), cell)
                                    l = 1
                            # elif move_cell == '2':
                            #     l = 1
                            # elif move_cell == '3':
                            #     l = 1
                            else:
                                pass

                    elif next_move == '3':
                        m=0
                        while m<1:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(f1)
                            print("1. Move card from cascade to foundation")
                            print("2. Move card from free cell slot to foundation")
                            move_foundation = input("Choose option to move card:")
                            if move_foundation == '1':
                                mcard_face = input("select card value to be moved to foundation:")
                                mcard_suit = input("select card suit to be moved to foundation:")
                                f1.move_to_foundation(mcard_face.upper(), mcard_suit.upper())
                                m = 1
                            elif move_foundation == '2':
                                x=0
                                while x < 1:
                                    try:
                                        cell = int(input("select cell slot (1-4) to move to foundation:"))
                                        x = 1
                                    except(ValueError):
                                        print('Oops, please enter an integer')
                                if cell < 5:
                                    f1.move_from_cell_to_foundation(cell)
                                    m = 1
                            else:
                                m = 1

                    else:
                        print("Incorrect Value!")


                elif move_input.upper() == 'Q':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Thank you for playing NotFreeCell!")
                    input("Press Enter to exit")
                    j = 1
                else:
                    print("Please enter either M to move or Q to quit!")

            i = 1
        elif user_input.upper() == 'Q':
            print("Ok tata byebye")
            i = 1
        else:
            print("Please enter either P to play or Q to quit!")


if __name__ == "__main__":
    main()

# f1=NotFreecell()
# f1.deck_in_play.create_deck()
# f1.deck_in_play.shuffle()
# # print(f1)
# f1.new_game()
# print(f1)
# # f1.move_card('9','S','X','P')
# # print(f1)
# # print(f1.deck_in_play)
