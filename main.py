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

    def calc_hand(self):
        for card in self.cards:
            # Number Cards
            if card[0] in RANKS[1:10]:
                self.value += int(card[0])
            # Picture Cards
            elif card[0] in RANKS[10:13]:
                self.value += 10
            # Aces
            else:
                # If hand value is under 10 take ace as 11, else 1
                if self.value <= 10:
                    self.value += 11
                else:
                    self.value += 1

    def add_card(self, card):
        self.cards.append(card)
        self.calc_hand()

# ------------------------- Play game ---------------------------- #
def blackjack_game():
    '''
    Plays an automated game of blackjack
    Returns:
    Won: True if player won, False if dealer won
    Hand: Player's starting hand
    '''    
    deck = Deck()
    deck.shuffle()

    player = Hand()
    dealer = Hand()

    

    # Deal starting hands
    for i in range(2):
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())

    starting_hand = player.cards

    # Player's go

    while player.value < 18:
        player.add_card(deck.deal())

    if player.value > 21: 
        # Player is bust
        return False, starting_hand
    # Dealer's go
    while dealer.value < player.value:
        dealer.add_card(deck.deal())
    if dealer.value > 21:
        # Dealer is bust
        return True, starting_hand
    else:
        # Dealer won
        return False, starting_hand


won, hand = blackjack_game()

print(won, hand)