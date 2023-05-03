import random
from collections import deque

# Function to draw a card from an infinite deck
# This function simulates drawing a card by generating a random number between 1 and 13 (inclusive)
# The value returned is the min value between the card number and 10 (following Blackjack rules where King, Queen and Jack are worth 10)
def draw_card_infinite():
    card = random.randint(1, 13)
    return min(card, 10)

# Function to check if a hand has an Ace (represented as 1)
# It checks if 1 is in the hand and the total value of the hand (including 11 for Ace) does not exceed 21
def soft(hand):
    return 1 in hand and sum(hand) + 10 <= 21

# Function to calculate the value of a hand
# If the hand is soft (contains an Ace that can be counted as 11), it adds 10 to the total hand value
def hand_value(hand):
    if soft(hand):
        return sum(hand) + 10
    return sum(hand)

# Function to calculate the soft value of a hand
def soft_hand_value(hand):
    return sum(hand)

# Policy 1: Stick if hand value is equal or greater than 17, else hit
def policy1(hand, d_card):
    return hand_value(hand) < 17

# Policy 2: Stick if hand value is equal or greater than 17 and is hard else hit unless the hand value equals to 21
def policy2(hand, d_card):
    return (hand_value(hand) < 17 and not soft(hand)) or hand_value(hand) == 21

# Policy 3: Always stick (never hit)
def policy3(hand, d_card):
    return False

# Policy 4: Follows a basic hand chart, not considering soft hands
# Stick if hand value is 17 or more, or if it is between 12 and 16 (inclusive) and dealer's card is less than 7.
# Hit in all other cases.
def policy4(hand, d_card):
    if hand_value(hand) >= 17:
        return False
    if hand_value(hand) < 17 and hand_value(hand) > 11 and  d_card < 7:
        return False
    return True

# Policy 5: Follows a basic hand chart, considering soft hands
# Decision depends on both player's hand and dealer's card
def policy5(hand, d_card):

    # Soft hand decision-making
    if soft(hand):
        if soft_hand_value(hand) < 8:
            return True
        elif soft_hand_value(hand) > 8:
            return False
        elif soft_hand_value(hand) == 8 and d_card <= 8:
            return False
        elif soft_hand_value(hand) == 8 and d_card > 8:
            return True

    # Hard hand decision-making
    if hand_value(hand) >= 17:
        return False
    if hand_value(hand) < 17 and hand_value(hand) > 11 and  d_card < 7:
        return False
    return True

# Function to create a single deck of cards
# This function creates a shuffled deck with 52 cards (4 sets of 1 to 13), where each card value is the minimum between the card number and 10
def create_single_deck():
    deck = [min(card, 10) for _ in range(4) for card in range(1, 14)]
    random.shuffle(deck)
    return deque(deck)

# Function to draw a card from a single deck
# This function returns the card at the top of the deck and removes it from the deck
def draw_card_single(deck):
    return deck.popleft()

# Function to simulate a game of Blackjack for a given policy and deck type
# The game is simulated by playing out the dealer's and player's turns and then comparing their hand values to determine the result
def play_game(policy, infinite_deck=False, single_deck=False):
    # Deciding the deck and draw card method based on the deck type
    if single_deck:
        deck = create_single_deck()
        draw_card = lambda: draw_card_single(deck)
    else:
        draw_card = draw_card_infinite if infinite_deck else draw_card_infinite

    # Initialize hands for player and dealer by drawing two cards each
    hand = [draw_card(), draw_card()]
    d_hand = [draw_card(), draw_card()]

    # If player is dealt Blackjack (a hand value of 21), return 1 as the result
    if hand_value(hand) == 21:
        return 1

    # Player turn: keep hitting until the policy says to stick
    while policy(hand, d_hand[0]):
        hand.append(draw_card())

    # Dealer turn: keep hitting until hand value reaches 17 or more
    while hand_value(d_hand) < 17:
        d_hand.append(draw_card())

    # Calculate the final values for both player and dealer
    player_final = hand_value(hand)
    d_final = hand_value(d_hand)

    # Determine the result of the game based on the final hand values
    if player_final > 21:         # player busts
        return -1
    elif d_final > 21:            #dealer busts
        return 1
    elif player_final > d_final:  # player has a higher hand value
        return 1
    elif player_final == d_final:  # both player and dealer have the same hand value
        return 0
    else:  # dealer has a higher hand value
        return -1

    # Function to run Monte Carlo simulations for the given policy and deck type
    # The simulations are run for a specified number of times (default is 100000),
    # and the results are accumulated to determine the win rate for the player and dealer, as well as the draw rate.


def run_monte_carlo(policy, infinite_deck=False, single_deck=False, num_simulations=100000):
    dealer_wins = 0
    player_wins = 0
    draws = 0

    for _ in range(num_simulations):
        result = play_game(policy, infinite_deck, single_deck)
        if result == -1:  # dealer wins
            dealer_wins += 1
        elif result == 1:  # player wins
            player_wins += 1
        else:  # draw
            draws += 1

    return dealer_wins, player_wins, draws


if __name__ == "__main__":
    policies = [policy1, policy2, policy3, policy4, policy5]
    deck_types = [{"infinite_deck": True, "single_deck": False},
                  {"infinite_deck": False, "single_deck": True}]

    # Main loop to iterate over all policies and deck types
    # For each policy and deck type, it runs the Monte Carlo simulations to calculate the player's winning probability
    # The results are then printed out for each policy and deck type
    for i, policy in enumerate(policies, 1):
        for j, deck_type in enumerate(deck_types, 1):
            dealer_wins, player_wins, draws = run_monte_carlo(policy, **deck_type, num_simulations=100000)
            winning_probability = player_wins / (dealer_wins + player_wins + draws) * 100
            deck_name = "Infinite Deck" if j == 1 else "Single Deck"
            print(f"{deck_name} - Policy {i}: Player Winning Probability = {winning_probability}%")
            print(f"Dealer wins: {dealer_wins}, Player wins: {player_wins}, Draws: {draws}\n")
