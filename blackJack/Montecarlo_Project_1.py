import random
import Single_Deck

# Define a function to simulate drawing a card from an infinite deck
def draw_card_infinite():
    return random.randint(1, 13)

# Define a function to simulate drawing a card from a single deck
def draw_card_single(deck):
    if len(deck) == 0:
        deck = list(range(1, 14)) * 4
        random.shuffle(deck)
    return deck.pop()

# Define a function to simulate a game of blackjack with the given policy
def play_game(policy, infinite_deck=True):
    if infinite_deck:
        draw_card = draw_card_infinite
    else:
        draw_card = draw_card_single
        deck = list(range(1, 14)) * 4
        random.shuffle(deck)

    # Initialize the player's hand
    hand = [draw_card(), draw_card()]

    # Play the game according to the policy
    while True:
        if policy == 1:
            if sum(hand) >= 17:
                return sum(hand)
            else:
                hand.append(draw_card())
        elif policy == 2:
            if sum(hand) >= 17 and all(card <= 10 for card in hand):
                return sum(hand)
            elif sum(hand) == 21:
                return sum(hand)
            else:
                hand.append(draw_card())
        elif policy == 3:
            return 20
        elif policy == 4:
            if sum(hand) < 10:
                hand.append(draw_card())
            else:
                return sum(hand)
        elif policy == 5:
            if sum(hand) == 20:
                return sum(hand)
            else:
                hand.append(draw_card())

# Define a function to run Monte Carlo simulations for the given policy and version of the game
def run_monte_carlo(policy, num_simulations, infinite_deck=True):
    total_score = 0
    for i in range(num_simulations):
        score = play_game(policy, infinite_deck)
        total_score += score
    return total_score / num_simulations

# Run Monte Carlo simulations for all policies and versions of the game
num_simulations = 1000000
for policy in [1, 2, 3, 4, 5]:
    for infinite_deck in [True, False]:
        if infinite_deck:
            deck_type = "Infinite Deck"
        else:
            deck_type = "Single Deck"
        print("Policy", policy, ":", deck_type)
        avg_score = run_monte_carlo(policy, num_simulations, infinite_deck)
        print("Average Score:", round(avg_score, 2))
