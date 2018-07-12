import time
import numpy
from deuces import Card
from deuces import Deck
from deuces import Evaluator

evaluator = Evaluator()
deck = Deck()


def validator(l1, l2):
    # the intersection of inputs must be empty
    b_ret = False
    for i in l1:
        if i in l2:
            b_ret = True
    return b_ret


def safe_draw(n, list=[]):
    # draw(n) not in list
    b_invalid = True
    while b_invalid:
        b_invalid = False
        deck.shuffle()
        d = deck.draw(n)
        if type(d) == int:
            d = [d]
        b_invalid = validator(d, list)
    return d


def combat_power(hole, board, deal_num, max_time=1):
    t_start = time.time()
    count = 0
    rank_list = []
    rank_list_fake = []
    while True:
        board_ext = safe_draw(deal_num, hole + board)
        hole_fake = safe_draw(2, hole + board + board_ext)
        merge = board + board_ext

        rank = evaluator.evaluate(merge, hole)
        rank_fake = evaluator.evaluate(merge, hole_fake)

        rank_list.append(rank)
        rank_list_fake.append(rank_fake)

        count += 1
        t_end = time.time()
        if t_end - t_start > max_time:
            break

    sum_rank = 0
    sum_rank_fake = 0

    for i in rank_list:
        sum_rank += i
    for i in rank_list_fake:
        sum_rank_fake += i

    # print info
    my_pretty_cards = ''
    if len(hole) == 0:
        if len(board) != 0:
            my_pretty_cards += ' [ ? ? ]  [ ? ? ] '
    else:
        for i in hole:
            my_pretty_cards += Card.int_to_pretty_str(i)
    for i in board:
        my_pretty_cards += Card.int_to_pretty_str(i)
    for i in range(deal_num):
        if len(hole) == 0 and len(board) > 0 and i < 2:
            continue
        my_pretty_cards += ' [ ? ? ] '
    print my_pretty_cards + ', ' + str(sum_rank / count) + ', ' + str(
        int(numpy.std(numpy.array(rank_list), axis=0))) + ', ' + str(sum_rank_fake / count) + ', ' + str(
        int(numpy.std(numpy.array(rank_list_fake), axis=0)))  # +', '+str(count)


# combat_power(deck.draw(2), [], 3)


for i in range(100):
    hole = safe_draw(2)
    flop = safe_draw(3, hole)
    turn = safe_draw(1, hole + flop)
    river = safe_draw(1, hole + flop + turn)

    combat_power(hole, [], 3 + 2)
    combat_power(hole, flop, 1 + 1)
    combat_power(hole, flop + turn, 1)
    combat_power(hole, flop + turn + river, 0)

    print '==='
'''
combat_power([], [], 5)
combat_power([], [], 6)
combat_power([], [], 7)
hand_2 = [
	[Card.new('As'), Card.new('Ks')],
	[Card.new('As'), Card.new('Qs')],
	[Card.new('As'), Card.new('Js')],
	[Card.new('As'), Card.new('Ts')],
	[Card.new('As'), Card.new('9s')],
	[Card.new('As'), Card.new('8s')],
	[Card.new('As'), Card.new('7s')],
	[Card.new('As'), Card.new('6s')],
	[Card.new('As'), Card.new('5s')],
	[Card.new('As'), Card.new('4s')],
	[Card.new('As'), Card.new('3s')],
	[Card.new('As'), Card.new('2s')],
	[Card.new('Ks'), Card.new('Qs')],
	[Card.new('Ks'), Card.new('Js')],
	[Card.new('Ks'), Card.new('Ts')],
	[Card.new('Ks'), Card.new('9s')],
	[Card.new('Ks'), Card.new('8s')],
	[Card.new('Ks'), Card.new('7s')],
	[Card.new('Ks'), Card.new('6s')],
	[Card.new('Ks'), Card.new('5s')],
	[Card.new('Ks'), Card.new('4s')],
	[Card.new('Ks'), Card.new('3s')],
	[Card.new('Ks'), Card.new('2s')],
	[Card.new('Qs'), Card.new('Js')],
	[Card.new('Qs'), Card.new('Ts')],
	[Card.new('Qs'), Card.new('9s')],
	[Card.new('Qs'), Card.new('8s')],
	[Card.new('Qs'), Card.new('7s')],
	[Card.new('Qs'), Card.new('6s')],
	[Card.new('Qs'), Card.new('5s')],
	[Card.new('Qs'), Card.new('4s')],
	[Card.new('Qs'), Card.new('3s')],
	[Card.new('Qs'), Card.new('2s')],
	[Card.new('Js'), Card.new('Ts')],
	[Card.new('Js'), Card.new('9s')],
	[Card.new('Js'), Card.new('8s')],
	[Card.new('Js'), Card.new('7s')],
	[Card.new('Js'), Card.new('6s')],
	[Card.new('Js'), Card.new('5s')],
	[Card.new('Js'), Card.new('4s')],
	[Card.new('Js'), Card.new('3s')],
	[Card.new('Js'), Card.new('2s')],
	[Card.new('Ts'), Card.new('9s')],
	[Card.new('Ts'), Card.new('8s')],
	[Card.new('Ts'), Card.new('7s')],
	[Card.new('Ts'), Card.new('6s')],
	[Card.new('Ts'), Card.new('5s')],
	[Card.new('Ts'), Card.new('4s')],
	[Card.new('Ts'), Card.new('3s')],
	[Card.new('Ts'), Card.new('2s')],
	[Card.new('9s'), Card.new('8s')],
	[Card.new('9s'), Card.new('7s')],
	[Card.new('9s'), Card.new('6s')],
	[Card.new('9s'), Card.new('5s')],
	[Card.new('9s'), Card.new('4s')],
	[Card.new('9s'), Card.new('3s')],
	[Card.new('9s'), Card.new('2s')],
	[Card.new('8s'), Card.new('7s')],
	[Card.new('8s'), Card.new('6s')],
	[Card.new('8s'), Card.new('5s')],
	[Card.new('8s'), Card.new('4s')],
	[Card.new('8s'), Card.new('3s')],
	[Card.new('8s'), Card.new('2s')],
	[Card.new('7s'), Card.new('6s')],
	[Card.new('7s'), Card.new('5s')],
	[Card.new('7s'), Card.new('4s')],
	[Card.new('7s'), Card.new('3s')],
	[Card.new('7s'), Card.new('2s')],
	[Card.new('6s'), Card.new('5s')],
	[Card.new('6s'), Card.new('4s')],
	[Card.new('6s'), Card.new('3s')],
	[Card.new('6s'), Card.new('2s')],
	[Card.new('5s'), Card.new('4s')],
	[Card.new('5s'), Card.new('3s')],
	[Card.new('5s'), Card.new('2s')],
	[Card.new('4s'), Card.new('3s')],
	[Card.new('4s'), Card.new('2s')],
	[Card.new('3s'), Card.new('2s')],
	[Card.new('As'), Card.new('Ah')],
	[Card.new('As'), Card.new('Kh')],
	[Card.new('As'), Card.new('Qh')],
	[Card.new('As'), Card.new('Jh')],
	[Card.new('As'), Card.new('Th')],
	[Card.new('As'), Card.new('9h')],
	[Card.new('As'), Card.new('8h')],
	[Card.new('As'), Card.new('7h')],
	[Card.new('As'), Card.new('6h')],
	[Card.new('As'), Card.new('5h')],
	[Card.new('As'), Card.new('4h')],
	[Card.new('As'), Card.new('3h')],
	[Card.new('As'), Card.new('2h')],
	[Card.new('Ks'), Card.new('Kh')],
	[Card.new('Ks'), Card.new('Qh')],
	[Card.new('Ks'), Card.new('Jh')],
	[Card.new('Ks'), Card.new('Th')],
	[Card.new('Ks'), Card.new('9h')],
	[Card.new('Ks'), Card.new('8h')],
	[Card.new('Ks'), Card.new('7h')],
	[Card.new('Ks'), Card.new('6h')],
	[Card.new('Ks'), Card.new('5h')],
	[Card.new('Ks'), Card.new('4h')],
	[Card.new('Ks'), Card.new('3h')],
	[Card.new('Ks'), Card.new('2h')],
	[Card.new('Qs'), Card.new('Qh')],
	[Card.new('Qs'), Card.new('Jh')],
	[Card.new('Qs'), Card.new('Th')],
	[Card.new('Qs'), Card.new('9h')],
	[Card.new('Qs'), Card.new('8h')],
	[Card.new('Qs'), Card.new('7h')],
	[Card.new('Qs'), Card.new('6h')],
	[Card.new('Qs'), Card.new('5h')],
	[Card.new('Qs'), Card.new('4h')],
	[Card.new('Qs'), Card.new('3h')],
	[Card.new('Qs'), Card.new('2h')],
	[Card.new('Js'), Card.new('Jh')],
	[Card.new('Js'), Card.new('Th')],
	[Card.new('Js'), Card.new('9h')],
	[Card.new('Js'), Card.new('8h')],
	[Card.new('Js'), Card.new('7h')],
	[Card.new('Js'), Card.new('6h')],
	[Card.new('Js'), Card.new('5h')],
	[Card.new('Js'), Card.new('4h')],
	[Card.new('Js'), Card.new('3h')],
	[Card.new('Js'), Card.new('2h')],
	[Card.new('Ts'), Card.new('Th')],
	[Card.new('Ts'), Card.new('9h')],
	[Card.new('Ts'), Card.new('8h')],
	[Card.new('Ts'), Card.new('7h')],
	[Card.new('Ts'), Card.new('6h')],
	[Card.new('Ts'), Card.new('5h')],
	[Card.new('Ts'), Card.new('4h')],
	[Card.new('Ts'), Card.new('3h')],
	[Card.new('Ts'), Card.new('2h')],
	[Card.new('9s'), Card.new('9h')],
	[Card.new('9s'), Card.new('8h')],
	[Card.new('9s'), Card.new('7h')],
	[Card.new('9s'), Card.new('6h')],
	[Card.new('9s'), Card.new('5h')],
	[Card.new('9s'), Card.new('4h')],
	[Card.new('9s'), Card.new('3h')],
	[Card.new('9s'), Card.new('2h')],
	[Card.new('8s'), Card.new('8h')],
	[Card.new('8s'), Card.new('7h')],
	[Card.new('8s'), Card.new('6h')],
	[Card.new('8s'), Card.new('5h')],
	[Card.new('8s'), Card.new('4h')],
	[Card.new('8s'), Card.new('3h')],
	[Card.new('8s'), Card.new('2h')],
	[Card.new('7s'), Card.new('7h')],
	[Card.new('7s'), Card.new('6h')],
	[Card.new('7s'), Card.new('5h')],
	[Card.new('7s'), Card.new('4h')],
	[Card.new('7s'), Card.new('3h')],
	[Card.new('7s'), Card.new('2h')],
	[Card.new('6s'), Card.new('6h')],
	[Card.new('6s'), Card.new('5h')],
	[Card.new('6s'), Card.new('4h')],
	[Card.new('6s'), Card.new('3h')],
	[Card.new('6s'), Card.new('2h')],
	[Card.new('5s'), Card.new('5h')],
	[Card.new('5s'), Card.new('4h')],
	[Card.new('5s'), Card.new('3h')],
	[Card.new('5s'), Card.new('2h')],
	[Card.new('4s'), Card.new('4h')],
	[Card.new('4s'), Card.new('3h')],
	[Card.new('4s'), Card.new('2h')],
	[Card.new('3s'), Card.new('3h')],
	[Card.new('3s'), Card.new('2h')],
	[Card.new('2s'), Card.new('2h')]
]
for i in hand_2:
	combat_power(i, [], 5)
'''