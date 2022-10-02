import numpy as np
import random
import matplotlib.pyplot as plt
from constants import *

# ------------------------ Rules ------------------------ # 

'''
Player and dealer are dealt two cards each
Player goes first
Player will twist if value < 18, stick if >= 18 and is bust if > 21
Dealer goes after
If dealer value >= player value, dealer sticks and wins. Otherwise twists until 
true or bust.
'''

# ------------------------ Classes ----------------------- #

class Deck():
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for rank in RANKS:
            for suit in SUITS:
                self.cards.append((rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()


class Hand(Deck):
    def __init__(self):
        self.cards = []
        self.value = 0
        self.soft = False

    def calc_hand(self):
        self.value = 0
        for card in self.cards:
            # Number Cards
            if card[0] in RANKS[1:10]:
                self.value += int(card[0])
            # Picture Cards
            elif card[0] in RANKS[10:13]:
                self.value += 10
            # Aces
            else:
                # Hand is soft, take ace as 1 and 
                # set soft to True
                self.value += 1
                self.soft = True

    def add_card(self, card):
        self.cards.append(card)
        self.calc_hand()

    def print_cards(self):
        return [f'{card[0]} of {card[1]}' for card in self.cards]

    def play_hand(self, deck):
        while self.value <= 21:
            print(f'Hand: {self.print_cards()}')
            move = input('Twist or stick? ')
            if move not in ['t', 's']:
                print('Enter t or s')
            elif move == 't':
                print('Twist...')
                new_card = deck.deal()
                self.add_card(new_card)
                print(f'Dealt: {new_card}')
            else:
                print('Stick...')
                break
    
    def play_hand_ai(self, deck, upcard):
        while self.value <= 21:
            move = choose_move(self, upcard)
            if move == 't':
                new_card = deck.deal()
                self.add_card(new_card)
            else:
                break
        if self.soft:
            if self.value < 12:
                self.value += 10

# --------------------------- AI -------------------------------- #

def choose_move(hand:Hand(), upcard:tuple):
    """
    Chooses player's move based on their hand and
    the dealer's upcard
    Returns: 't' or 's' accordingly
    """
    if upcard[0] in RANKS[1:10]:
        upval = int(upcard[0])
    else:
        # All picture cards treated the same
        upval = 10

    if hand.soft:
        # Hand is soft so play accordingly
        non_ace = hand.value - 1
        if non_ace > 7:
            return 's'
        elif non_ace == 7 and upval < 9:
            return 's'
        else:
            return 't'
    else:
        # Hand not soft
        if hand.value == 12 and 4 <= upval <= 6:
            return 's'
        elif 12 < hand.value < 17 and upval < 7:
            return 's'
        elif hand.value > 17:
            return 's'
        else:
            return 't'

def choose_split(hand:Hand(), upcard:tuple):
    """
    Chooses if player wants to split based on hand and upcard
    Returns 'y' or 'n' accordingly
    """
    if upcard[0] in RANKS[1:10]:
        upval = int(upcard[0])
    else:
        # All picture cards treated the same
        upval = 10
    val = hand.value

    if val == 22 or val == 16:
        return 'y'
    elif val == 18 and upval not in [7, 10]:
        return 'y'
    elif val == 14 and upval < 8:
        return 'y'
    elif val == 12 and 2 < upval < 7:
        return 'y'
    elif val in [4, 6] and 3 < upval < 8:
        return 'y'
    else: 
        return 'n'

# ------------------------- Play game ---------------------------- #
def blackjack_game():
    '''
    Plays an automated game of blackjack
    Returns:
    Won: True if player won, False if dealer won
    Value: Value of player's starting hand
    '''    
    # print('------------- Playing Blackjack -----------')

    deck = Deck()
    deck.shuffle()

    player = Hand()
    dealer = Hand()


    # Deal starting hands
    for i in range(2):
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())
    
    # Set dealer upcard
    upcard = dealer.cards[0]

    starting_hand = player.value

    # Check if blackjack
    if dealer.soft and dealer.value == 11:
        # Dealer has natural so wins
        return False, starting_hand
    elif player.soft and player.value == 11:
        return True, starting_hand

    # Check if they can/want to split
    if player.cards[0][0] == player.cards[1][0]:
        split = choose_split(player, upcard)
        if split == 'y':
            # Split into two hands
            player_left = Hand()
            player_right = Hand()
            player_left.add_card(player.cards[0])
            player_right.add_card(player.cards[1])
            # Play both hands
            player_left.play_hand_ai(deck, upcard)
            player_right.play_hand_ai(deck, upcard)

            # Use the highest valid value hand
            if player_left.value > 21:
                player = player_right
            elif player_right.value > 21:
                player = player_left
            elif player_right.value > player_left.value:
                player = player_right
            else:
                player = player_left
    else:
        player.play_hand_ai(deck, upcard)


    # Dealer plays
    # Dealer twists until hand >= 17
    while dealer.value < 17:
        # If dealer has an ace and taking as 11 
        # brings it over 16 but not bust, must stick
        if dealer.soft and 16 < dealer.value + 10 <= 21:
            dealer.value += 10
            break
        # Otherwise deal another card
        new_card = deck.deal()
        dealer.add_card(new_card)

    # If player's hand soft, try both 11 and 1 for ace
    if player.soft and player.value < 12:
        player.value += 10

    # If dealer value higher than player value and valid
    return (player.value <= 21 and dealer.value < player.value), starting_hand





if __name__ == '__main__':

    # Matplotlib
    plt.figure()
    # Build results array
    results = np.zeros(22)

    # Run n games
    n = 100000
    for i in range(n):
        won, value = blackjack_game()
        if won:
            results[value] += 1
    print(sum(results))
    plt.bar(range(22), results/n * 100)
    plt.show()