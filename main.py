from Card import Card
from Player import Player
import random

# TODO:
#     2. Begin training a player

# global variables
round_num = 1
num_players = 4
total_rounds = 60 // num_players
trump_suit = None


# function that changes face cards to numerical values:
def face_to_val(card_value) -> int:
    if card_value == 'Jack':
        return 11
    elif card_value == 'Queen':
        return 12
    elif card_value == 'King':
        return 13
    elif card_value == 'Ace':
        return 14
    elif card_value == 'Jester':
        return 1
    elif card_value == 'Wizard':
        return 15
    return int(card_value)


# function that creates the deck
def create_deck() -> [Card]:
    suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
    values = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    cards = [Card(value, suit) for value in values for suit in suits]
    for x in range(4):
        cards.append(Card('Wizard', 'Wizard'))
        cards.append(Card('Jester', 'Jester'))
    return cards


# prints all the cards in a list of cards (e.g., deck or hand)
def print_cards(cards: [Card]):
    for card in cards:
        print(card)


# function that deals cards to each player
def deal_cards(players: [Player], deck: [Card]):
    # set trump card and suit
    global trump_suit
    trump_suit = None
    if round_num != total_rounds:
        trump_card = deck[round_num * num_players]
        print(f"trump card: {trump_card}")
        if trump_card.suit == 'Wizard':
            trump_suit = 'Hearts'
        elif trump_card.suit == 'Jester':
            trump_suit = None
        else:
            trump_suit = trump_card.suit

    if trump_suit is None:
        print("There is no trump suit")
    else:
        print(f"Trump suit is: {trump_suit}")

    # put round_num cards in each players' hand
    for i in range(0, len(players)):
        for j in range(round_num):
            players[i].hand.append(deck[i + (j * num_players)])


def select_eligible_cards(card_list: [Card], desired_suit: str) -> [Card]:
    eligible_cards = []
    for card in card_list:
        if card.suit == desired_suit or card.suit == 'Wizard' or card.suit == 'Jester':
            eligible_cards.append(card)
    return eligible_cards


def select_random_card(card_list: [Card]) -> Card:
    if len(card_list) > 1:
        return card_list[random.randint(0, len(card_list) - 1)]
    return card_list[0]


def next_player(player_num: int) -> int:
    if player_num + 1 < num_players:
        return player_num + 1
    return 0


def play_round_random(players: [Player], scores: [int], dealer: [int]):
    print(f"round {round_num}!")

    # create lists to track cards played in a trick and how many tricks each player has won
    card_stack = [None] * num_players
    tricks_won = [0] * num_players

    # assign players a trick taken prediction
    for player in players:
        player.predicted_tricks = random.randint(0, round_num)

    # want to keep track of which player plays first card in each trick
    current_player = next_player(dealer)

    # play out the round completely
    for x in range(round_num):
        # want to keep track of `lead`ing suit for players to follow
        lead_suit = ""

        # each player plays one of their cards at random if there is no lead_suit and a random card of the lead suit
        # if they have one available
        for i in range(num_players):
            if lead_suit == "":
                card_being_played = select_random_card(players[current_player].hand)
                card_stack[current_player] = card_being_played
                if card_being_played.suit != "Wizard" and card_being_played.suit != "Jester":
                    lead_suit = card_being_played.suit
                players[current_player].hand.remove(card_being_played)
            else:
                eligible_cards = select_eligible_cards(players[current_player].hand, lead_suit)
                if not eligible_cards:
                    card_being_played = select_random_card(players[current_player].hand)
                    card_stack[current_player] = card_being_played
                    players[current_player].hand.remove(card_being_played)
                else:
                    card_being_played = select_random_card(eligible_cards)
                    card_stack[current_player] = card_being_played
                    players[current_player].hand.remove(card_being_played)
            current_player = next_player(current_player)

        # determine which player played the card that wins the trick
        best_card_played = 0
        for i in range(len(card_stack)):
            if card_stack[best_card_played].suit == 'Wizard':
                continue
            if card_stack[i].suit == 'Jester':
                continue
            if card_stack[i].suit == 'Wizard':
                best_card_played = i
                continue
            if card_stack[best_card_played].suit != trump_suit:
                if card_stack[i].suit == trump_suit:
                    best_card_played = i
                elif face_to_val(card_stack[i].value) > face_to_val(card_stack[best_card_played].value):
                    best_card_played = i
            else:
                if card_stack[i].suit == trump_suit:
                    if face_to_val(card_stack[i].value) > face_to_val(card_stack[best_card_played].value):
                        best_card_played = i

        print_cards(card_stack)
        print(f"player {best_card_played + 1} won the trick!")
        tricks_won[best_card_played] += 1

    for player in range(num_players):
        if tricks_won[player] == players[player].predicted_tricks:
            scores[player] += (20 + 10 * tricks_won[player])
        else:
            scores[player] -= (10 * abs(tricks_won[player] - players[player].predicted_tricks))


def clear_hands(players: [Player]):
    for player in players:
        player.hand.clear()


if __name__ == '__main__':
    # initialize game state variables
    players = []
    for i in range(num_players):
        players.append(Player([]))

    # create deck of cards that includes wizards, jesters, and all other cards
    deck = create_deck()

    # create a list to keep track of scores
    scores = [0] * num_players

    # determine who starts as dealer
    dealer = random.randint(0, 3)

    # temp game testing bullshit
    for x in range(total_rounds):
        random.shuffle(deck)
        deal_cards(players, deck)
        play_round_random(players, scores, dealer)
        dealer = next_player(dealer)
        clear_hands(players)
        round_num += 1

    print(scores)
