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

# ------------------------- Play game ---------------------------- #
def blackjack_game():
    '''
    Plays an automated game of blackjack
    Returns:
    Won: True if player won, False if dealer won
    Value: Value of player's starting hand
    '''    
    print('------------- Playing Blackjack -----------')

    deck = Deck()
    deck.shuffle()

    player = Hand()
    dealer = Hand()

    print('Dealing hands')

    # Deal starting hands
    for i in range(2):
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())
    ###################### testing
    player.cards = [('7', 'Clubs'), ('7', 'Spades')]

    # Set dealer upcard
    upcard = dealer.cards[0]

    print(f"Player's hand: {player.print_cards()}")
    print(f"Dealer's hand {[upcard, 'hidden']}")

    starting_hand = player.value

    # Check if blackjack
    if dealer.soft and dealer.value == 11:
        # Dealer has natural so wins
        print('Dealer has blackjack')
        return False, starting_hand
    elif player.soft and player.value == 11:
        print('Player has blackjack')
        return True, starting_hand

    print('-'*20)
    print("Player's go...")
    # Player plays

    # Check if they can/want to split
    if player.cards[0][0] == player.cards[1][0]:
        print('Player has a pair.')
        split = input("Would you like to split? ")
        if split not in ['y', 'n']:
            split = input('Enter y or n: ')
        if split == 'y':
            # Split into two hands
            print('Splitting into two hands...')
            player_left = Hand()
            player_right = Hand()
            player_left.add_card(player.cards[0])
            player_right.add_card(player.cards[1])
            # Play both hands
            player_left.play_hand(deck)
            player_right.play_hand(deck)
            # Use the highest valid value hand
            if player_left.value < player_right.value <= 21:
                player = player_right
            else:
                player = player_left
    else:
        player.play_hand(deck)

    
    print('-'*20)
    print('Dealer\'s go...')
    print(f'Dealer\'s hand: {dealer.print_cards()}')
    # Dealer plays
    # Dealer twists until hand >= 17
    while dealer.value < 17:
        # If dealer has an ace and taking as 11 
        # brings it over 16 but not bust, must stick
        if dealer.soft and 16 < dealer.value + 10 <= 21:
            dealer.value += 10
            break
        # Otherwise deal another card
        print('Dealer twists...')
        new_card = deck.deal()
        print(f'Dealt: {new_card}')
        dealer.add_card(new_card)
        print(f'Dealer\'s hand: {dealer.print_cards()}')

    print('-'*20)
    print(f"Player's final hand: {player.print_cards()}")
    print(f"Dealer's final hand: {dealer.print_cards()}")

    # If player's hand soft, try both 11 and 1 for ace
    if player.soft and player.value < 12:
        player.value += 10

    # If dealer value higher than player value and valid
    return not (dealer.value <= 21 and dealer.value >= player.value), starting_hand





if __name__ == '__main__':

    won, hand = blackjack_game()
    if won:
        print('Player won')
    else:
        print('Dealer won')


    # # Matplotlib
    # plt.figure()
    # # Build results array
    # results = np.zeros(22)

    # # Run n games
    # n = 100000
    # for i in range(n):
    #     won, value = blackjack_game()
    #     if won:
    #         results[value] += 1
    # print(sum(results))
    # plt.bar(range(22), results/n * 100)
    # plt.show()