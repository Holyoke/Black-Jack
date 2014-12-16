#Black Jack
#Press the "play" button in the top left corner to play!

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
message =""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


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



'''
Implement the methods __init__, __str__, add_card for the Hand class. We suggest modeling a hand as a list of cards. For help in implementing the __str__ method for hands, refer back to practice exercise number four from last week. Remember to use the string method for cards to convert each card object into a string. Once you have implemented the Hand class, test it using the provided testing template.
'''        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        string = ''
        for card in self.hand:
            string += str(card)
            string += " "
        return string      
        
    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        aces = 0
        
        #check for aces in hand
        for card in self.hand:
            if card.get_rank() == 'A':
                aces += 1
                
        for card in self.hand:
            value += VALUES[card.get_rank()]
            
        if aces == 0:
            return value
        else:
            if value + 10 > 21:
                return value
            else:
                return value + 10
        #fucking voodoo 
       
        
    def draw(self, canvas, p):
        pos = p
        for card in self.hand:
            card.draw(canvas, p)
            pos[0] = pos[0] + 90
        if in_play == True:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [115.5,229], CARD_BACK_SIZE)
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))
#        self.deck = [(suit, rank) for suit in SUITS for rank in RANKS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        string = ''
        for card in self.deck:
            string += str(card.get_suit() )
            string += str(card.get_rank() )
            string += ' '
        return "Deck contains: "+ string

#define event handlers for buttons
def deal():
    global message, outcome, in_play, player_hand, dealer_hand, deck,score
    outcome = ""
    message = ""
    
    if in_play == True:
    # your code goes here
        message = "Dealing new hand and subtracting score"
        score -= 1
        
        deck = Deck() 
        player_hand = Hand()
        dealer_hand = Hand()
    
        deck.shuffle()
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
    else:
        message = "Hit or Stand?"
        
        deck = Deck() 
        player_hand = Hand()
        dealer_hand = Hand()
    
        deck.shuffle()
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())        
#    print player_hand
#    print player_hand.get_value()
#    print dealer_hand
#    print deck
    in_play = True

def hit():
    global in_play, player_hand, dealer_hand, deck, message,outcome,score
    
    
    # if the hand is in play, hit the player 
    if (player_hand.get_value() <= 21) and in_play:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() <= 21:
            message = "Hit or Stand?"
            in_play = True
        else:
            in_play = False
            message = "You busted! Press 'Deal' to Play again."
            outcome = "Dealer: " + str(dealer_hand.get_value()) + "  Player: " + str(player_hand.get_value())
            score -= 1
                
    else:
        score -= 1
        message = "You busted! Press 'Deal' to Play again."
        outcome = "Dealer: " + str(dealer_hand.get_value()) + "  Player: " + str(player_hand.get_value())
        in_play = False
        deal()
    
            
    # if busted, assign an message to outcome, update in_play and score
       
def stand():
    global in_play, score, message, outcome, dealer_hand,player_hand
    if in_play == False:
        message = "That hand is already over. Deal again."
        print message
    else:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            message = "You win! Press 'Deal' to Play again."
            score += 1
            in_play = False
        elif dealer_hand.get_value() >= player_hand.get_value():
            message = "Dealer wins. Press 'Deal' to Play again."
            score -= 1
            in_play = False
        elif dealer_hand.get_value() < player_hand.get_value():
            message = "You win! Press 'Deal' to Play again."
            score += 1
            in_play = False
        outcome = "Dealer: " + str(dealer_hand.get_value()) + "  Player: " + str(player_hand.get_value())
        print message
        print outcome
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", [40,80], 48, "White")
    canvas.draw_text("Score: " + str(score), [450,80], 36, "Black")
    canvas.draw_text("Dealer", [80,160], 30, "Black")
    canvas.draw_text("Player", [80,430], 30, "Black")
    canvas.draw_text(message, [200,355], 24, "Black")
    canvas.draw_text(outcome, [350,160], 24, "Black")
    player_hand.draw(canvas, [80,450])
    dealer_hand.draw(canvas, [80,180])

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
