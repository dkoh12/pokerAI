import random, sys

suit = ['Club', 'Diamond', 'Heart', 'Spade']
rank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

toInt = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
toString = {2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13:  'K', 14: 'A'}


class pokerdeck:
	def __init__(self):
		self.count = 52
		self.deck = [(i, j) for i in rank for j in suit]
		self.board = []

	def shuffle(self):
		random.shuffle(self.deck)
		return self.deck

	def draw(self):
		card = self.deck[0]
		self.deck = self.deck[1:]
		self.count -= 1
		return card

	def drawFirstBid(self):
		self.board.extend(self.deck[1:4])
		self.deck = self.deck[4:]
		self.count -= 4

	def drawNextBid(self):
		self.board.append(self.deck[1])
		self.deck = self.deck[2:]
		self.count -= 2


def greeting():
	while True:
		print("Welcome to Texas Hold'em.")
		num = input("How many people would like to play? (or 'q' to quit) ")
		
		if num.lower().startswith('q'):
			sys.exit()
		if not num.isdigit():
			print("invalid number.")
			continue
		if int(num) <= 0:
			print("invalid number.")
			continue
		return int(num)

def distributeHand(people):
	players = dict()
	for i in range(1, 2*people+1):
		if i <= people:
			players['player %d' % i] = [deck.draw()]
		else:
			players['player %d' % (i%people+1)].append(deck.draw())

	return players

# maps players to the amount they bid and whether they decided to fold or not
def distributeMoney(players):
	return dict((i, (0, False)) for i in players)


def displayBoard(deck):
	print()
	print("board")
	print(deck.board)
	print()

def convert(card):
	newcard = []
	for i in card:
		newcard.append(toInt[i])
	return newcard

def convert_back(card):
	newcard = []
	for i in card:
		newcard.append(toString[i])
	return newcard
	

combination = {1: 'straight_flush', 2: 'four_of_a_kind', 3: 'full_house',
				4: 'flush', 5: 'straight', 6: 'three_of_a_kind',
				7: 'two_pair', 8: 'one_pair', 9: 'high_card', 0: 'royal_flush'}


def hand_value(hand):
	print("hand", hand)
	print()

	if royal_flush(hand):
		# (0, ('Heart', ['10', 'J', 'Q', 'K', 'A']))
		return (0, royal_flush(hand))
	elif straight_flush(hand):
		# (1, ('Heart', ['4', '5', '6', '7', '8']))
		return (1, straight_flush(hand))
	elif four_of_a_kind(hand):
		# (2, '7')
		return (2, four_of_a_kind(hand))
	elif full_house(hand):
		# (3, (('5', ['Heart', 'Club']), ('7', ['Spade', 'Club', 'Diamond'])))
		return (3, full_house(hand))
	elif flush(hand):
		# (4, ('Club', ['7', '10', 'K', '9', '4']))
		return (4, flush(hand))
	elif straight(hand):
		# (5, ['4', '5', '6', '7', '8'])
		return (5, straight(hand))
	elif three_of_a_kind(hand):
		# (6, '7')
		return (6, three_of_a_kind(hand))
	elif two_pair(hand):
		# (7, [('K', ['Spade', 'Club']), ('7', ['Club', 'Diamond'])])
		return (7, two_pair(hand))
	elif one_pair(hand):
		# (8, ('K', ['Spade', 'Club']))
		return (8, one_pair(hand))
	else:
		# (9, ('K', 'Spade'))
		return (9, high_card(hand)) 

def royal_flush(hand):
	val = straight_flush(hand)
	if val:
		print("royal flush???")
		rank = val[0]
		card = val[1]

		print(val)

		card.sort()

		royalFlush = ['10', 'J', 'Q', 'K', 'A']
		royalFlush.sort()
		
		print(card)
		print(royalFlush)

		if card == royalFlush:
			return (rank, card)

	return False

# all 5 cards are straight and same suite
def straight_flush(hand):
	val = flush(hand)
	if val:
		rank = val[0]
		number = val[1]

		flushed_hand = [(i, rank) for i in number]
		
		check = straight(flushed_hand)
		if check:
			return (rank, check)
		else:
			return False

	return False

def four_of_a_kind(hand):
	number = dict((j[0], [i[1] for i in hand if i[0] == j[0]]) for j in hand)

	for i, j in number.items():
		if len(j) == 4:
			# print(i, j)
			return i

	return False

# 3 of 1 kind, 2 of another kind
def full_house(hand):
	number = dict((j[0], [i[1] for i in hand if i[0] == j[0]]) for j in hand)

	three = (False, "")
	two = (False, "")
	for i, j in number.items():
		if len(j) == 2:
			two = (True, (i, j))
		if len(j) == 3:
			three = (True, (i, j))

	if two[0] and three[0]:
		return (two[1], three[1])
	
	return False

# all 5 cards same suite
def flush(hand):
	rank = dict((j[1], [i[0] for i in hand if i[1] == j[1]]) for j in hand)
	
	for i, j in rank.items():
		if len(j) >= 5:
			return (i, j[0:5]) #hacky fix

	return False

def straight(hand):
	number = [i[0] for i in hand] # make sure hand is a tuple

	cards = convert(number)
	cards.sort()

	for k in range(len(hand)-4):
		match = True
		window = cards[k:k+5]

		for i in range(4):
			if window[i] + 1 != window[i+1]:
				match = False
				break

		if match:
			window = convert_back(window)
			return window

	return False

def three_of_a_kind(hand):
	number = dict((j[0], [i[1] for i in hand if i[0] == j[0]]) for j in hand)

	for i, j in number.items():
		if len(j) == 3:
			# print(i, j)
			return i

	return False

def two_pair(hand):
	number = dict((j[0], [i[1] for i in hand if i[0] == j[0]]) for j in hand)

	cards = []
	for i, j in number.items():
		if len(j) == 2:
			# cards.append((i, j))
			cards.append(i)

	if len(cards) == 2:
		return cards

	return False

def one_pair(hand):
	number = dict((j[0], [i[1] for i in hand if i[0] == j[0]]) for j in hand)

	for i, j in number.items():
		if len(j) == 2:
			# return (i, j)
			return i

	return False

def high_card(hand):
	return max([i for i in hand])

def playAgain():
	return input("Would you like to play again? (yes or no) ").lower().startswith('y')

def bid(money):
	print()

	for i, j in money.items():
		if j[1]:
			continue

		while True:
			bid = input("%s bid: (enter amount or 'f' for fold) " % i)
			if bid.lower().startswith('f'):
				print("%s folded" % i)
				money[i] = (j[0], True)
				break
			if bid.isdigit() and float(bid) > 0:
				print("You bid %s amount" % bid)
				money[i] = (float(bid) + j[0], False)
				break

	return money
	

def bidding(deck, i, money):
	print()
	if i == 0:
		print("Initial round of bidding blind")
	elif i == 1:
		deck.drawFirstBid()
		displayBoard(deck)
		print("Second round of bidding")
	elif i == 2:
		deck.drawNextBid()
		displayBoard(deck)
		print("Third round of bidding")
	else:
		deck.drawNextBid()
		displayBoard(deck)
		print("Final round of bidding")
	
	bid_money = bid(money)

	print()
	print("current bid")
	return bid_money


def break_by_high_card(players):
	val = list(players.values())
	print(val)

	i = len(val[0])-1

	while not (len(val) == 1 or i < 0):

		currmax = max([j[i] for j in val])
		val = [j for j in val if j[i] == currmax]

		i-=1 

	print(val)




def tiebreaker(score, winner):
	print()
	print(winner)
	print(score)

	#straight flush
	if score == 1:
		# double check this comparator

		name = max(winner.items(), key=lambda k: toInt[k[1]])
		return name[0]
	# four of a kind
	elif score == 2:
		name = max(winner.items(), key=lambda k: toInt[k[1]])
		return name[0]
	# full house
	elif score == 3:

		name = max(winner.items(), key=lambda k: toInt[k[1]])
		return name[0]
	# flush
	elif score == 4:
		
		name = max(winner.items(), key=lambda k: toInt[k[1]])
		return name[0]
	# straight
	elif score == 5:
		
		name = max(winner.items(), key=lambda k: toInt[k[1]])
		return name[0]
	# three of a kind
	elif score == 6:
		
		name = max(winner.items(), key=lambda k: toInt[k[1]])
		return name[0]
	# two pair
	elif score == 7:
		print("LOLOL")

		name = break_by_high_card(winner)
		# name = max(winner.items(), key=lambda k: toInt[k[1]])
		return name[0]
	# one pair
	elif score == 8:
		# [('player 3', (8, ('3', ['Club', 'Spade']))), ('player 2', (8, ('10', ['Heart', 'Diamond'])))]
		name = max(winner.items(), key=lambda k: toInt[k[1]])
		return name[0]

		# mmax = max([j[1][0] for i, j in winner])
		# print("max", mmax)
		# lst = [(i, j[1]) for i, j in winner if j[1][0] == mmax]
		# if len(lst) == 1:
		# 	print("lst", lst[0])
		# 	return lst[0]
		# return lst
	

def payout(name, player_bids):
	total = sum([j[0] for i, j in player_bids.items()])
	print("%s won %d" % (name, total))


def test():
	# more_players = {'player 1': [('5', 'Diamond'), ('5', 'Club')], 
	# 'player 3': [('7', 'Heart'), ('8', 'Heart')], 
	# 'player 2': [('A', 'Diamond'), ('A', 'Club')]}

	# table = [('A', 'Heart'), ('A', 'Spade'), ('10', 'Heart'), ('5', 'Spade'), ('5', 'Heart')]

	more_players = {'player 1': [('10', 'Heart'), ('2', 'Club')], 
	'player 3': [('7', 'Club'), ('3', 'Diamond')], 
	'player 2': [('3', 'Club'), ('K', 'Diamond')]}

	table = [('J', 'Diamond'), ('A', 'Club'), ('J', 'Club'), ('10', 'Club'), ('7', 'Heart')]


	points = {}
	for i in more_players:
		hand = more_players[i] + table
		print(i)
		points[i] = hand_value(hand)
		print()

	for i, j in points.items():
		print(i, j)
		print()
	

	score = min([i[0] for i in list(points.values())])
	winner = dict((i, j[1]) for i, j in points.items() if j[0] == score)

	print()
	print(winner)

	if len(winner) == 1:
		print(winner)
		print(winner[0])
		print(winner[1])

		print("The Winner is %s with %s" % (winner, combination[score]))
		# payout(winner[0], money)
	else:
		print("It's a Tie")
		name = tiebreaker(score, winner)
		print("Winner is %s with %s" % (name, combination[score]))

	print()
	print(table)
	print("players' hands")
	print(more_players)


if __name__=="__main__":
	test()

	# while True:
	# 	while True:
	# 		people = greeting()
	# 		deck = pokerdeck()

	# 		deck.shuffle()

	# 		players = distributeHand(people)
	# 		money = distributeMoney(players)

	# 		print("players hands")
	# 		print(players)

	# 		for i in range(4):
	# 			money = bidding(deck, i, money)

	# 		points = {}
	# 		for i in players:
	# 			hand = players[i] + deck.board
	# 			print(i)
	# 			points[i] = hand_value(hand)
	# 			print()

	# 		for i, j in points.items():
	# 			print(i, j)
	# 			print()

	# 		score = min([i[0] for i in list(points.values())])
	# 		winner = dict((i, j[1]) for i, j in points.items() if j[0] == score)

	# 		print("@@@")
	# 		print(money)

	# 		if len(winner) == 1:
	# 			# print(winner)
	# 			print("The Winner is %s with %s" % (list(winner)[0], combination[score]))
	# 		else:
	# 			print("It's a Tie")
	# 			name = tiebreaker(score, winner)
	# 			print("Winner is %s with %s" % (name, combination[score]))

	# 		print()
	# 		displayBoard(deck)
	# 		print("players' hands")
	# 		print(players)

	# 		print()
	# 		break

	# 	if not playAgain():
	# 		break


