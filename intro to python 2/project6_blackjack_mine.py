
http://www.codeskulptor.org/#user41_qZVNG3NcSO_92.py
# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
score_text = ""
player_value_text = ""
dealer_value_text = ""
info_message = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


def draw_card_back(canvas, pos):
    canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = [];

    def __str__(self):
        # return a string representation of a hand
        cards_str = []
        for card in self.cards:
            cards_str.append(str(card))

        return " ".join(cards_str)

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video

        has_ace = False
        total_value = 0

        for card in self.cards:
            card_rank = card.get_rank()
            if card_rank == "A":
                has_ace = True

            card_value = VALUES[card_rank]

            total_value += card_value

        if has_ace:
            if total_value <= 11:
                total_value += 10

        return total_value

    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        offset = 0
        for card in self.cards:
            card.draw(canvas, [pos[0] + offset, pos[1]])
            offset += CARD_SIZE[0] + 10



# define deck class
class Deck:
    def __init__(self):
        # create a Deck object

        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck
        # use random.shuffle()
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        print "remaining cards " + str(len(self.cards))
        return self.cards.pop(0)

    def __str__(self):
        # return a string representing the deck
        cards_str = []
        for card in self.cards:
            cards_str.append(str(card))

        return " ".join(cards_str)

#define event handlers for buttons
def deal():
    global outcome, in_play, info_message
    global dealer_hand, player_hand
    global deck
    global player_value, dealer_value
    global score

    outcome = ""

    dealer_hand = Hand()
    player_hand = Hand()
    deck = Deck()
    deck.shuffle()

    dealer_value = 0
    player_value = 0
    player_value_text = ""
    dealer_value_text = ""
    info_message = "Hit or Stand?"

    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())

    in_play = True



def hit():
    # replace with your code below
    global in_play, outcome
    global player_hand
    global player_value, dealer_value
    global score, score_text
    global info_message
    global deck

    if not in_play:
        return

    # if the hand is in play, hit the player
    player_hand.add_card(deck.deal_card())

    # show total points of the player and dealer
    player_value = player_hand.get_value()
    dealer_value = dealer_hand.get_value()


    # if busted, assign a message to outcome, update in_play and score
    if player_value > 21:
        # player busted
        in_play = False
        outcome = "Player busted. You lose."
        info_message = "New Deal?"
        score -= 1


        print outcome
        print player_value
        print dealer_value
        print score
        print info_message

def stand():

    global in_play, outcome
    global dealer_hand, player_hand
    global player_value, dealer_value
    global score, score_text
    global info_message
    global deck

    if not in_play:
        return

    # show total points of the player and dealer
    player_value = player_hand.get_value()
    dealer_value = dealer_hand.get_value()

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while dealer_value < 17:
        dealer_hand.add_card(deck.deal_card())

    if dealer_value > 21:
        # dealer busted
        in_play = False
        outcome = "Dealer busted. You win!"
        score += 1
        info_message = "New Deal?"

        print outcome
        print player_value
        print dealer_value
        print score
        print info_message

        return

    in_play = False
    # assign a message to outcome, update in_play and score
    if dealer_value >= player_value:
        outcome = "You lose."
        score -= 1
        info_message = "New Deal?"
        print player_value
        print dealer_value
        print outcome
        print score
        print info_message
    else:
        outcome = "You win!"
        score += 1
        info_message = "New Deal?"
        print player_value
        print dealer_value
        print outcome
        print score
        print info_message

# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global dealer_hand, player_hand
    global in_play
    global score
    global player_value, dealer_value, player_value_text, dealer_value_text

    # convert player and dealer points and score to string
    player_value_text = str(player_value) + " points"
    dealer_value_text = str(dealer_value) + " points"
    score_text = str(score)

    # draw text
    canvas.draw_text('Blackjack', (120, 100), 50, 'Cyan')
    canvas.draw_text('Dealer:', (100, 180), 25, 'black')
    canvas.draw_text('Player:', (100, 380), 25, 'black')
    canvas.draw_text(outcome, (300, 180), 25, 'black')
    canvas.draw_text(player_value_text, (180, 380), 25, 'black')
    canvas.draw_text(dealer_value_text, (180, 180), 25, 'black')
    canvas.draw_text('score: '+ score_text, (400, 100), 25, 'black')
    canvas.draw_text(info_message, (300, 380), 25, 'black')

    # draw hand
    dealer_hand.draw(canvas, [100, 200])
    player_hand.draw(canvas, [100, 400])

    if in_play:
        draw_card_back(canvas, [100, 200])


dealer_hand = None
player_hand = None
deck = None

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
