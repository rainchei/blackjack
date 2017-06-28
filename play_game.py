from random import shuffle, randint


class Card(object):
    """ Class for card with a symbol and a rank. """

    def __init__(self, symbol, rank):
        self.symbol = symbol
        self.rank = rank

    def __str__(self):
        return '{0}-{1}'.format(self.symbol, self.rank)


class Player(object):
    """ Class for blackjack player. """

    dealer = False
    # placed_bet = 0
    # points = 0

    def __init__(self, name, bankroll=0):
        self.name = name
        self.bankroll = bankroll
        self.placed_bet = 0
        self.points = 0
        # (problem) if this has been assigned as the Class Object Attribute, the method of append to the list
        # will affect all instances, causing all players have the same hand.
        self.hand = list()

    def deposit(self, amount):
        self.bankroll += amount

    def withdraw(self, amount):
        self.bankroll -= amount

    def deal(self, card, folding=False):
        self.hand.append(
            {'card': card,
             'folding': folding})


def build_deck():
    """ Build a shuffled deck from six standard 52-card packs, and insert one plastic card toward the bottom of the pack
     to indicate when to reshuffle the deck, so that the last 60 to 75 cards or so will not be used. """

    deck = []
    suits = ['clubs', 'diamonds', 'hearts', 'spades']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    for times in range(6):
        for s in suits:
            for r in ranks:
                deck.append(Card(s, r))

    plastic_card = " "
    shuffle(deck)
    deck.insert(-randint(60, 75), plastic_card)  # minus to count from the last card

    return deck


def player_sign_up():
    """ Create a dealer and other players with names and initial bankrolls. """

    dealer = Player('dealer')
    dealer.dealer = True

    while True:
        try:
            n = int(input('How many players do we have here? '))
            m = int(input('How much the initial bankroll does each player have? '))
        except ValueError:
            print('Please input an integer! ')
            continue
        else:
            print('Welcome! We have {0} player(s) joined the blackjack, and each has {1} dollars. '.format(n, m))
            break

    p = list()
    p.append(dealer)  # the dealer is player[0]

    for num in range(1, n+1):
        name = input('Player {0} - please input your name: '.format(num))
        p.append(Player(name, m))

    return p


def place_bet(players):
    """ Ask all players to place a bet in front of him in the designated area, limits are from $2 to $500 """

    for p in players:
        while not p.dealer:
            try:
                b = int(input('{0}, you currently have ${1}, please place your bet: $'.format(p.name, p.bankroll)))
            except ValueError:
                print('Please input an integer! ')
                continue
            else:
                if b > p.bankroll:
                    print('Your bankroll is too small to cover this bet. ')
                    continue
                else:
                    p.withdraw(b)
                    p.placed_bet = b
                    print('{0} has placed ${1}, remaining {2} dollars.'.format(p.name, p.placed_bet, p.bankroll))
                    break


def deal_cards(players, shoe):
    """ Gives one card face up to each player, and then one card to the dealer.
        Next, gives another card face up to each player, but one face down to the dealer """

    players.append(players.pop(0))  # move the dealer to the last
    deal_order = players

    print('Dealing cards ...')
    for r in range(2):
        for p in deal_order:
            if r == 1 and p.dealer:  # the second card of the dealer should be folded. (default unfolded.)
                p.deal(shoe.pop(0), folding=True)
            else:
                p.deal(shoe.pop(0))


def print_table(players):
    """ Print the current status (cards and points of each player and the dealer) on the table. """

    for p in players:
        print('*-*-*-*-*-*-*-*-*-*')

        if not p.dealer:
            print("{0} wagered ${1} on ".format(p.name, p.placed_bet))
            ranks = list()
            for card in p.hand:
                print(card['card'])
                ranks.append(card['card'].rank)
            p.points += count_points(ranks)
            print('\nTotal: {0}'.format(p.points))
        else:
            print('Dealer')
            ranks = list()
            for card in p.hand:
                if card['folding']:
                    print('Card - face down')
                else:
                    print(card['card'])
                    ranks.append(card['card'].rank)
            p.points += count_points(ranks)
            print('\nTotal: {0}'.format(p.points))


def count_points(ranks):

    points = 0
    for rank in ranks:
        if rank not in ['A', 'J', 'Q', 'K']:
            points += int(rank)
        elif rank in ['J', 'Q', 'K']:
            points += 10
        else:
            points += 11

    return points


if __name__ == '__main__':

    all_players = player_sign_up()
    shoe_box = build_deck()
    place_bet(all_players)
    # Each player is dealt two cards face up, then dealer receives one upcard and one hole card.
    deal_cards(all_players, shoe_box)
    print_table(all_players)
    # If the dealer has an ace showing, the insurance bet is offered to each player in turn.

    # If early surrander is allowed, each player has the option to surrender, taking back half his bet 
    # and forfeiting the rest.

    # If dealer has an ace, 10, or face card, the dealer checks for blackjack. If the dealer has blackjack, 
    # any insurance bets are paid, and all other bets are settled. If the dealer does not have blackjack,
    # any insuraces bets are collected, player who have blackjack are paid 3:2 and the game continues.
