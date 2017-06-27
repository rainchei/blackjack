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

    # (0) The standard 52-card pack is used, but in most casinos several decks of cards are shuffled together. The
    # six-deck game (312 cards) is the most popular. In addition, the dealer uses a blank plastic card, which is never
    # dealt, but is placed toward the bottom of the pack to indicate when it will be time for cards to be reshuffled.
    # When four or more decks are used, they are dealt from a shoe (a box that allows the dealer to remove card one at
    # a time, face down, without actually holding one or more packs).

    # (1) The dealer thoroughly shuffles portions of the pack until all the cards have been mixed and combined. He
    # designated one of the players to cut, and the plastic insert card is placed so that the last 60 to 75 cards or so
    # will not be used. (Not dealing to the bottom of all the cards makes it more difficult for professional counter to
    # operate efficiently.)

    shoe_box = build_deck()

    # (2) Each player places a bet, in front of him in the designated area, general limits are from $2 to $500.

    place_bet(all_players)

    # (3) The dealer gives one card face up to each player in rotation clockwise, and then one card face up to himself.
    # Another round of cards is then dealt face up to each player, but the dealer takes his second card face down.

    deal_cards(all_players, shoe_box)
    print_table(all_players)

    # (4) If any player has a natural and the dealer does not, the dealer immediately pays that player one and a half
    # times the amount of his bet.
    # If the dealer has a natural, he immediately collects the bets of all players who do not have naturals, (but no
    # additional amount).
    # If the dealer and another player both have naturals, the bet of that player is a stand-off (a tie), and the player
    # takes back his chips.
    # If the dealer's face-up card is a ten-card or an ace, he looks at his face-down card to see if the two cards make
    # a natural. If the face-up card is not a ten-card or an ace, he does not look at the face-down card until it is
    # the dealer's turn to play.

    # (5) The player to the left goes first and must decide whether to "stand" (not ask for another card) or "hit"
    # (ask for another card in an attempt to get closer to a count of 21, or even hit 21 exactly). When asking for
    # additional cards, one at a time, he may go "bust" (if it is over 21). Then, the player loses and the dealer
    # collects the bet wagered.

    # (6) The combination of an ace with a card other than a ten-card is known as a "soft hand", because the player can
    # count the ace as a 1 or 11, and either draw cards or not. For example, if the draw creates a bust hand by counting
    # the aces as an 11, the player simply counts the aces as 1 and continues playing by standing or hitting.

    # (7) When the dealer has served every player, his face-down card is turned up. If the total is 17 or more, he must
    # stand. If the total is 16 or under, he must take a card. He must continue to take cards until the total is 17 or
    # more, at which point the dealer must stand. If the dealer has an ace, and counting it as 11 would bring his total
    # to 17 or more (but not over 21), he must count the ace as 11 and stand. The dealer's decisions, then, are
    # automatic on all plays, whereas the player always has the option of taking one or more cards.

    # (8) If a players's first two cards are of the same denomination, such as two jacks or two sixes, he may choose to
    # treat them as two separate hands when his turn comes around. The amount of his original bet then goes on one of
    # cards, and an equal amount must be placed as a bet on the other card. The player first plays the hand to his left
    # by standing or hitting one or more times; only then is the hand to the right played. The two hands are thus
    # treated separately, and the dealer settles with each on its own merits. With a pair of aces, the player is given
    # one card for each ace and may not draw again. Also, if a ten-card is dealt to one of these aces, the payoff is
    # equal to the bet (not one and one-half to one, as with a blackjack at any other time).

    # (9) Another option open to the player is doubling his bet when the original two cards dealt total 9, 10, or 11.
    # When the player's turn comes, he places a bet equal to the original bet, and the dealer gives him just one card,
    # which is placed face down and is not turned up until the bets are settled at the end of the hand. With two fives,
    # the player may split a pair, double down, or just play the hand in the regular way. Note that the dealer does not
    # have the option of splitting or doubling down.

    # (10) When the dealer's face-up card is an ace, any of the players may make a side bet of up to half the original
    # bet that the dealer's face-down card is a ten-card, and thus a blackjack for the house.
    # Once all such side bets are placed, the dealer looks at his hole card. If it is a ten-card, it is turned up, and
    # those players who have made the insurance bet win and are paid double the amount of their half-bet
    # - a 2 to 1 payoff.

    # (11) A bet once paid and collected is never returned. Thus, one key advantage to the dealer is that the player
    # goes first. If the player goes bust, he has already lost his wager, even if the dealer goes bust as well. If the
    # dealer goes over 21, he pays each player who has stood the amount of that player's bet. If the dealer stands at 21
    # or less, he pays the bet of any player having a higher total (not exceeding 21) and collects the bet of any player
    # having a lower total. If there's a stand-off (a player having the same total as the dealer), no chips are paid out
    # or collected.

    # (12) When each player's bet is settled, the dealer gathers in that player's card and places them face up at the
    # side against a clear plastic L-shaped shield. The dealer continues to deal from the shoe until he comes to the
    # plastic insert card, which indicates that it is time to reshuffle. Once that round of play is over, the dealer
    # reshuffles all the cards, prepares them for the cut, places the cards in the shoe, and the game continues.
