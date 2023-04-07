import random
from collections import deque

# Function to draw a card from an infinite deck
def draw_card_infinite():
    card = random.randint(1, 13)
    return min(card, 10)

# Check if a hand has an Ace
def soft(hand):
    return 1 in hand and sum(hand) + 10 <= 21

# Calculate the value of a hand
def hand_value(hand):
    if soft(hand):
        return sum(hand) + 10
    return sum(hand)

# Calculate the soft value of a hand
def soft_hand_value(hand):
    return sum(hand)

# Policy 1: If your hand ≥ 17, stick. Else hit.
def policy1(hand, d_card):
    return hand_value(hand) < 17

# Policy 2: If your hand ≥ 17 and is hard, stick. Else hit unless your hand = 21
def policy2(hand, d_card):
    return (hand_value(hand) < 17 and not soft(hand)) or hand_value(hand) == 21

# Policy 3: Always stick
def policy3(hand, d_card):
    return False

# Policy 4: Basic hand chart (Does not include logic for soft hands)
def policy4(hand, d_card):
    if hand_value(hand) >= 17:
        return False
    if hand_value(hand) < 17 and hand_value(hand) > 11 and  d_card < 7:
        return False
    return True

# Policy 5: Basic hand chart (Includes logic for soft hands)
def policy5(hand, d_card):

    # Soft hand
    if soft(hand):
        if soft_hand_value(hand) < 8:
            return True
        elif soft_hand_value(hand) > 8:
            return False
        elif soft_hand_value(hand) == 8 and d_card <= 8:
            return False
        elif soft_hand_value(hand) == 8 and d_card > 8:
            return True

    # Hard hand
    if hand_value(hand) >= 17:
        return False
    if hand_value(hand) < 17 and hand_value(hand) > 11 and  d_card < 7:
        return False
    return True

# Create a single deck of cards
def create_single_deck():
    deck = [min(card, 10) for _ in range(4) for card in range(1, 14)]
    random.shuffle(deck)
    return deque(deck)

# Draw a card from a single deck
def draw_card_single(deck):
    return deck.popleft()

# Simulate Blackjack for the given policy and deck type
def play_game(policy, infinite_deck=False, single_deck=False):
    if single_deck:
        deck = create_single_deck()
        draw_card = lambda: draw_card_single(deck)
    else:
        draw_card = draw_card_infinite if infinite_deck else draw_card_infinite

    hand = [draw_card(), draw_card()]
    d_hand = [draw_card(), draw_card()]

    # Player is dealt Blackjack
    if hand_value(hand) == 21:
        return 1

    # Player turn
    while policy(hand, d_hand[0]):
        hand.append(draw_card())

    # Dealer turn
    while hand_value(d_hand) < 17:
        d_hand.append(draw_card())

    player_final = hand_value(hand)
    d_final = hand_value(d_hand)

    if player_final > 21:
        return -1
    elif d_final > 21:
        return 1
    elif player_final > d_final:
        return 1
    elif player_final == d_final:
        return 0
    else:
        return -1

# Monte Carlo simulations for the given policy and deck type
def run_monte_carlo(policy, infinite_deck=False, single_deck=False, num_simulations=100000):
    dealer_wins = 0
    player_wins = 0
    draws = 0

    for _ in range(num_simulations):
        result = play_game(policy, infinite_deck, single_deck)
        if result == -1:
            dealer_wins += 1
        elif result == 1:
            player_wins += 1
        else:
            draws += 1

    return dealer_wins, player_wins, draws

if __name__ == "__main__":
    policies = [policy1, policy2, policy3, policy4, policy5]
    deck_types = [{"infinite_deck": True, "single_deck": False},
                  {"infinite_deck": False, "single_deck": True}]

    # Iterate over all policies and deck types
    for i, policy in enumerate(policies, 1):
        for j, deck_type in enumerate(deck_types, 1):
            dealer_wins, player_wins, draws = run_monte_carlo(policy, **deck_type, num_simulations=100000)
            winning_probability = player_wins / (dealer_wins + player_wins + draws) * 100
            deck_name = "Infinite Deck" if j == 1 else "Single Deck"
            print(f"{deck_name} - Policy {i}: Player Winning Probability = {winning_probability}%")
            print(f"Dealer wins: {dealer_wins}, Player wins: {player_wins}, Draws: {draws}\n")
