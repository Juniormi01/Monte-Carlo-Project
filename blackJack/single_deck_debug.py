import Single_Deck
import time

deck = Single_Deck.normal_deck()

outer_test = 10
inner_test = 60

# Method 3
print("Method 3")
start_time = time.time()

for j in range(outer_test):
    deck.shuffle_cards()
    for i in range(inner_test):
        deck.draw_card_single()

print(time.time() - start_time)
