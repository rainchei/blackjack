from random import shuffle, randint
from os import system


class Card(object):
    """ Class for card with a symbol and a rank. """

    def __init__(self, symbol, rank):
        self.symbol = symbol
        self.rank = rank

    def __str__(self):
        return '{0} - {1}'.format(self.symbol, self.rank)


class Player(object):
    """ Class for blackjack player. """

    def __init__(self, name, bankroll=0, dealer=False):
        self.name = name
        self.bankroll = bankroll
        self.dealer = dealer
        self.placed_bet = 0
        self.points = 0
        # if a list has been declared as the Class Object Attribute, any changes to the list
        # will affect all instances, causing all players having the same hand.
        self.hand = list()

    def deposit(self, amount):
        self.bankroll += amount

    def withdraw(self, amount):
        self.bankroll -= amount

    def deal(self, card, folding=False):
        self.hand.append(
            {'card': card,
             'folding': folding})

    def lose(self):
        print('{0} loses!'.format(self.name))
        self.placed_bet = 0

    def win(self, natural):
        if natural:
            print('{0} wins with blackjack! Pays 3 to 2'.format(self.name))
            self.bankroll += 2.5 * self.placed_bet
            self.placed_bet = 0
        else:
            print('{0} wins! '.format(self.name))
            self.bankroll += 2 * self.placed_bet
            self.placed_bet = 0

    def push(self):
        print('{0} Push! '.format(self.name))
        self.bankroll += self.placed_bet
        self.placed_bet = 0


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

    # plastic_card = " "
    shuffle(deck)
    # deck.insert(-randint(60, 75), plastic_card)  # minus to count from the last card

    return deck


def player_sign_up():
    """ Create a dealer and other players with names and initial bankrolls. """

    dealer = Player('dealer', dealer=True)

    while True:
        try:
            n = int(input('How many players do we have here? '))
            m = int(input('How much the initial bankroll does each player have? '))
        except ValueError:
            print('Please input an integer! ')
            continue
        else:
            print('Welcome! We have {0} player(s) joined the blackjack, and each has {1} dollars'.format(n, m))
            break

    p = list()
    p.append(dealer)  # the dealer is player[0]

    for num in range(1, n+1):
        name = input('Player {0} - please input your name: '.format(num))
        p.append(Player(name, m))

    return p


def place_bet(players, min_bet=2, max_bet=500):
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
                    print('Your bankroll is too small to cover this bet ')
                    continue
                elif b < min_bet or b > max_bet:
                    print('Wager is ranged from ${0} to ${1} '.format(min_bet, max_bet))
                else:
                    p.withdraw(b)
                    p.placed_bet = b
                    print('{0} has placed ${1}, remaining {2} dollars.'.format(p.name, p.placed_bet, p.bankroll))
                    break


def deal_cards(players, shoe):
    """ Gives one card face up to each player, and then one card to the dealer.
        Next, gives another card face up to each player, but one face down to the dealer """

    print('Dealing cards to each member ...')
    deal_order = list()
    for i in players:
        deal_order.append(i)

    deal_order.append(deal_order.pop(0))  # move the dealer to the last

    for r in range(2):
        for p in deal_order:
            if r == 1 and p.dealer:  # the second card of the dealer should be folded. (default unfolded.)
                p.deal(shoe.pop(0), folding=True)
            else:
                p.deal(shoe.pop(0))


def print_table(players):
    """ Print the current status (cards and points of each player and the dealer) on the table. """

    system('clear')
    for p in players:

        p.points = 0
        if not p.dealer:
            print("{0} | Bankroll Remains ${1} | Wager ${2} ".format(p.name, p.bankroll, p.placed_bet))
            ranks = list()
            for card in p.hand:
                print(card['card'])
                ranks.append(card['card'].rank)

            p.points += count_points(ranks)
            # special treatment for rank A (for player)
            if 'A' in ranks:
                for i in range(len(ranks)):
                    if ranks[i] == 'A' and p.points + 10 < 22:
                        p.points += 10
            # checks for bust
            if p.points > 21:
                p.points = 'bust'

            print('\nTotal: {0}'.format(p.points))
        else:
            print('Banker')
            ranks = list()
            for card in p.hand:
                if card['folding']:
                    print('hole card (face down)')
                else:
                    print(card['card'])
                    ranks.append(card['card'].rank)

            p.points += count_points(ranks)
            # special treatment for rank A (for dealer)
            if 'A' in ranks:
                for i in range(len(ranks)):
                    if ranks[i] == 'A' and p.points + 10 < 22:
                        p.points += 10
            # checks for bust
            if p.points > 21:
                p.points = 'bust'

            print('\nTotal: {0}'.format(p.points))

        print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')


def count_points(ranks):
    """ Input a list of ranks to get the total points of hand """

    points = 0
    for rank in ranks:
        if rank not in ['A', 'J', 'Q', 'K']:
            points += int(rank)
        elif rank in ['A']:
            points += 1
        else:
            points += 10

    return points


def dealer_natural(players):
    """ Check if the dealer gets the natural (reach 21 without hitting) """

    for p in players:
        if p.dealer and p.points >= 10:
            print('Dealer checks for blackjack ...')
            ranks = list()
            for card in p.hand:
                ranks.append(card['card'].rank)
            if count_points(ranks) == 21:
                print('Dealer has blackjack! ')
                for card in p.hand:
                    card['folding'] = False
                return True
            else:
                print('Dealer does not have blackjack')
                return False


def player_natural(p):
    """ Check if any of the players gets the natural (reach 21 without hitting) """

    if not p.dealer and p.points == 21:
        print('{0} has blackjack! '.format(p.name))
        return True
    elif not p.dealer and p.points < 21:
        return False


def player_options(p, shoe):

    while True:
        ans = input('{0}, do you wanna (a) hit or (b) stand? '.format(p.name)).lower()
        if ans not in ['a', 'b']:
            print('Please input letter "a" or "b"')
            continue
        else:
            if ans == 'a':
                return p.deal(shoe.pop(0))
            elif ans == 'b':
                return 'stand'


def dealer_play(players, shoe):

    for p in players:
        if p.dealer:
            ranks = list()
            for card in p.hand:
                card['folding'] = False
                ranks.append(card['card'].rank)
            # dealer must hit if total if less than 17, otherwise, stand
            if count_points(ranks) < 17:
                return p.deal(shoe.pop(0))
            else:
                return 'stand'


def status_reset(players):

    for p in players:
        p.placed_bet = 0
        p.hand = list()
        p.points = 0


if __name__ == '__main__':

    all_players = player_sign_up()

    game_on = 'y'
    while game_on == 'y':

        shoe_box = build_deck()
        place_bet(all_players)
        # Each player is dealt two cards face up, then dealer receives one up card and one hole card.
        deal_cards(all_players, shoe_box)
        print_table(all_players)
        # If the dealer has an ace showing, the insurance bet is offered to each player in turn.

        # (working on it ...)

        # If early surrender is allowed, each player has the option to surrender, taking back half his bet
        # and forfeiting the rest.

        # (working on it ...)

        # If dealer has an ace, 10, or face card, the dealer checks for blackjack. If the dealer has blackjack,
        # any insurance bets are paid, and all other bets are settled. If the dealer does not have blackjack,
        # any insurance bets are collected, player who have blackjack are paid 3:2 and the game continues.
        if dealer_natural(all_players):
            for player in all_players:
                if player_natural(player):
                    player.push()
                    player.points = 'push'
                    print_table(all_players)
                else:
                    player.lose()
                    print_table(all_players)
        else:
            for player in all_players:
                if not player.dealer:
                    if player_natural(player):
                        player.win(natural=True)
                        print_table(all_players)
                    else:
                        while True:
                            if player_options(player, shoe_box) == 'stand':
                                break
                            else:  # hit
                                print_table(all_players)  # print_table checks for bust
                                if player.points == 'bust':
                                    player.lose()
                                    break
                                else:
                                    continue
            while True:
                if dealer_play(all_players, shoe_box) == 'stand':
                    break
                else:  # hit
                    print_table(all_players)
                    for player in all_players:
                        if player.dealer and player.points == 'bust':
                            for rest in all_players:
                                if rest.points != 'bust':
                                    rest.win(natural=False)
                            break
                        else:
                            continue

            for player in all_players:
                if player.dealer and player.points != 'bust':
                    print_table(all_players)
                    for other in all_players:
                        if not other.dealer and other.points != 'bust':
                            if player.points > other.points:
                                other.lose()
                            elif player.points == other.points:
                                other.push()
                            else:
                                other.win(natural=False)

        while True:
            game_on = input('Continue to play? (y/n) ').lower()
            if game_on not in ['y', 'n']:
                continue
            else:
                status_reset(all_players)
                break
