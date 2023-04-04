import random
#       2, 3, 4, 5, 6, 7, 8, 9, 10, J,  Q,  K,  A
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4

class normal_deck:
    def __init__(self):
        self.amount = 52
        self.tempDeck = deck.copy()
    
    def draw_card_single(self):
        if self.amount <= 0:
            return -1
        else:
            self.amount = self.amount - 1
        print(self.tempDeck)
        card = self.tempDeck.pop(random.randint(0, len(self.tempDeck) - 1))
        return card

    
    # This function is used to refill the deck with the deck defined above the class
    def shuffle_cards(self):
        self.tempDeck = deck.copy()
        self.amount = 52