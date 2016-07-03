# http://www.codeskulptor.org/#user41_LpOIw30VGuKP0iM.py
# implementation of card game - Memory
import simplegui
import random

# define general state of cards
flip_count = 0
cards = []
exposed = []
flip_card1 = 0
flip_card2 = 0
turn = 0
card_amount = 16

# helper function to initialize globals
def new_game():
    # shuffle the cards
    global cards
    global flip_count
    global exposed
    global flip_card1
    global flip_card2
    global turn
    global card_amount
    global label
    cards = range(card_amount/2) + range(card_amount/2)
    random.shuffle(cards)
    # reset all cards state
    flip_count = 0
    exposed = [False]*card_amount
    flip_card1 = 0
    flip_card2 = 0
    turn = 0
    label.set_text("Turns = " + str(turn))
    # print all initalized states for reference
    print cards
    print flip_count
    print exposed
    print flip_card1
    print flip_card2
    print turn
# define event handlers
def mouseclick(position):
    global cards
    global flip_count
    global exposed
    global flip_card1
    global flip_card2
    global turn
    global label
    # add game state logic here
    # determine which card is clicked
    x = position[0]
    card_index = x / 50
    # the content of the clicked card

    # when click a card, determine whether the card is exposed.
    # if the card is exposed, nothing happens.
    if exposed[card_index]:
        return
    # if the card is covered, flip the card to exposed.
    if 0 == flip_count:
        exposed[card_index] = True
        flip_card1 = card_index
        flip_count = 1

    elif 1 == flip_count:
        exposed[card_index] = True
        flip_card2 = card_index
        flip_count = 2

        # when all cards are exposed, end the game.
        all_exposed = True
        for card_exposed in exposed:
            if False == card_exposed:
                all_exposed = False
        if all_exposed:
            turn += 1
            label.set_text("Turns = " + str(turn))
    elif 2 == flip_count:
        # flip the next card.
        exposed[card_index] = True
        # previously, two cards are flipped.
        # determine whether the two previous flipped cards are paired.
        if cards[flip_card1] == cards[flip_card2]:
            pass
        else:
            exposed[flip_card1] = False
            exposed[flip_card2] = False

        flip_card1 = card_index
        flip_count = 1

        # record the end of a turn.
        turn += 1
        label.set_text("Turns = " + str(turn))
    else:
        print "Error!"

# cards are logically 50x100 pixels in size
def draw(canvas):
    global cards
    global flip_count
    global exposed
    global flip_card1
    global flip_card2

    card_index = 0
    for card in cards:
        card_str = str(card)
        card_x = 50 * card_index
        # if the card is exposed, draw the card content
        if exposed[card_index]:
            canvas.draw_text(card_str, (card_x+5, 80), 80, 'red')
        # if the card is still covered, draw the cover
        else:
            canvas.draw_polygon([[card_x, 0],
                                        [card_x + 50, 0],
                                        [card_x + 50, 100],
                                        [card_x, 100]], 1, 'green', 'red')
        card_index += 1


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric
