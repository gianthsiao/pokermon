from deuces import Card, Deck, Evaluator
from websocket import create_connection
import json
import time


def getCard(card):
    return Card.new(card[0]+card[1].lower())

class PokerBot(object):
    def declareAction(self,hole, board, round, my_Raise_Bet, my_Call_Bet, Table_Bet, number_players, raise_count, bet_count, my_Chips, total_bet):
		err_msg = self.__build_err_msg("declare_action")
		raise NotImplementedError(err_msg)
	def game_over(self, isWin, winChips, data):
		err_msg = self.__build_err_msg("game_over")
		raise NotImplementedError(err_msg)


class PokerSocket(object):
	ws = ""
	board = []
	hole = []
	my_Raise_Bet = 0
	my_Call_Bet = 0
	number_players = 0
	my_Chips = 0
	Table_Bet = 0
	playerGameName = None
	raise_count = 0
	bet_count = 0
	total_bet = 0
	players = []
	def __init__(self, playerName, connect_url, pokerbot):
		self.pokerbot = pokerbot
		self.playerName = playerName
		self.connect_url = connect_url

	def getAction(self,data):
		round = data['game']['roundName']
		# time.sleep(2)
		chips = data['self']['chips']
		hands = data['self']['cards']
		self.players = data['game']['players']
		self.raise_count = data['game']['raiseCount']
		self.bet_count = data['game']['betCount']
		self.my_Chips = chips
		self.playerGameName = data['self']['playerName']

		self.number_players = len(self.players)
		self.my_Call_Bet = data['self']['minBet']
		self.my_Raise_Bet = int(chips / 4)
		self.hole = []
		for card in (hands):
			self.hole.append(getCard(card))

		print 'Round:{}, my_Call_Bet:{}, my_Raise_Bet:{}, total_bet:{}'.format(round, self.my_Call_Bet, self.my_Raise_Bet, self.Table_Bet)

		# aggresive_Tight = PokerBotPlayer(preflop_threshold_Tight, aggresive_threshold)
		# tightAction, tightAmount = aggresive_Tight.declareAction(hole, board, round, my_Raise_Bet, my_Call_Bet,Table_Bet,number_players)
		action, amount= self.pokerbot.declareAction(self.hole, self.board, round, self.my_Raise_Bet, self.my_Call_Bet, self.Table_Bet, self.number_players, self.raise_count, self.bet_count, self.my_Chips, self.total_bet, self.players)
		self.total_bet += amount
		return action, amount

	def takeAction(self, action, data):
		# Get number of players and table info
		if action == "__show_action":
			table = data['table']
			boards = table['board']
			self.players = data['players']
			self.number_players = len(self.players)
			self.Table_Bet = table['totalBet']
			self.board = []
			for card in (boards):
				self.board.append(getCard(card))
			print 'total_bet:{}'.format(self.Table_Bet)
		elif action == "__bet":
			action,amount=self.getAction(data)
			print "action: {}, amount: {}".format(action, amount)
			self.ws.send(json.dumps({
				"eventName": "__action",
				"data": {
					"action": action,
					"playerName": self.playerName,
					"amount": amount
				}}))
		elif action == "__action":
			action,amount=self.getAction(data)
			print "action: {}, amount: {}".format(action, amount)
			self.ws.send(json.dumps({
				"eventName": "__action",
				"data": {
					"action": action,
					"playerName": self.playerName,
					"amount": amount
				}}))
		elif action == "__round_end":
			self.total_bet = 0
			self.players = data['players']
			isWin = False
			winChips = 0
			for player in self.players:
				winMoney = player['winMoney']
				playerid = player['playerName']
				if self.playerGameName == playerid:
					if winMoney == 0:
						isWin = False
					else:
						isWin = True
					winChips=winMoney
			print "winPlayer:{}, winChips:{}".format(isWin, winChips)
			self.pokerbot.game_over(isWin,winChips,data)
		elif action == "__deal":
			boards = data['table']['board']
			self.board = []
			for card in (boards):
				self.board.append(getCard(card))
			#Card.print_pretty_cards(self.board)

	def doListen(self):
		try:
			self.ws = create_connection(self.connect_url)
			self.ws.send(json.dumps({
				"eventName": "__join",
				"data": {
					"playerName": self.playerName
				}
			}))
			while 1:
				result = self.ws.recv()
				msg = json.loads(result)
				event_name = msg["eventName"]
				data = msg["data"]
				#print event_name, data
				self.takeAction(event_name, data)
		except Exception, e:
			print e.message
			self.doListen()

class PokerMon(PokerBot):
	def __init__(self, preflop_tight_loose_threshold, aggresive_passive_threshold, bet_tolerance):
		self.preflop_tight_loose_threshold = preflop_tight_loose_threshold
		self.aggresive_passive_threshold = aggresive_passive_threshold
		self.bet_tolerance = bet_tolerance
		# deuces
		self.evaluator = Evaluator()
		self.deck = Deck()

	def game_over(self, isWin, winChips, data):
		print "Game Over"

	def dealer(self, n, used = []):
		# draw n cards not in used
		cards = []
		for i in range(n):
			while True:
				c = self.deck.draw(1)
				if c not in used:
					break
			cards.append(c)
		return cards

	def combat_power(self, hole, board_input, ppl, max_time = 1):
		Card.print_pretty_cards(hole+board_input)
		count = 0
		count_win = 0
		b_len = len(board_input)
		t_start = time.time()
		while True:
			self.deck.shuffle()
			board = board_input + self.dealer(5-b_len, hole+board_input)
			rank_my = self.evaluator.evaluate(hole, board)

			b_win = True
			player = []
			rank = []
			for i in range(ppl-1):
				player.append(self.dealer(2, hole+board))
				rank.append(self.evaluator.evaluate(player[i], board))
				if rank_my > rank[i]:
					b_win = False

			if b_win:
				count_win += 1

			count += 1
			t_end = time.time()
			if t_end - t_start > max_time:
				break

		return float(count_win)/float(count)

	def declareAction(self, hole, board, round, my_Raise_Bet, my_Call_Bet, Table_Bet, number_players, raise_count, bet_count, my_Chips, total_bet, players):
		out = []
		for i in players:
			if i['folded'] or not i['isSurvive']:
				out.append(i['playerName'])
		o_l = len(out)
		ppl = number_players
		if o_l > 0:
			print "Folders & Deads: {}".format(', '.join(out))
			ppl -= o_l

		if round == 'Deal':
			win_rate = self.combat_power(hole, [], 2)
		else:
			win_rate = self.combat_power(hole, board, ppl)
		print "Round:{}, Players:{}, WinRate:{}".format(round, ppl, win_rate)

		if round == 'Deal':
			if win_rate >= 0.50:
				action = 'check'
				amount = 0
			else:
				action = 'fold'
				amount = 0
		else:
			if win_rate >= 0.90:
				action = 'raise'
				amount = my_Chips
			elif win_rate >= 0.80:
				action = 'raise'
				amount = my_Raise_Bet
			elif win_rate >= 0.70:
				action = 'call'
				amount = my_Call_Bet
			elif win_rate >= 0.50:
				action = 'check'
				amount = 0
			else:
				action = 'fold'
				amount = 0
		return action, amount

if __name__ == '__main__':
	aggresive_threshold = 0.5
	passive_threshold = 0.7
	preflop_threshold_Loose = 0.3
	preflop_threshold_Tight = 0.5

	playerName="PokerMon_Tim"
	connect_url="ws://poker-dev.wrs.club:3001/"
	simulation_number=100
	bet_tolerance=0.1

	myPokerBot=PokerMon(preflop_threshold_Tight,aggresive_threshold,bet_tolerance)
	myPokerSocket=PokerSocket(playerName,connect_url,myPokerBot)
	myPokerSocket.doListen()