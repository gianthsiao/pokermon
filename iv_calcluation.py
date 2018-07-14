players = 5
communitry_card = [1,2,3]
small_blind = 10
big_blind = 20
public_card_numbers = len(communitry_card)
init_bet = 3000
combat_threshold = 0.4
aggressive_threshold = 0.5
cofidience_ratio = 0.3333

def iv_calculation_1(win_rate, bet, total_pot, my_all_bet):
    if bet < my_all_bet:
        iv_value = bet / (total_pot + bet)
        return (True, bet, iv_value) if win_rate > iv_value else (False, bet, iv_value)
    else:
        return False,0,0


def iv_calculation_2(win_rate, bet, total_pot, my_all_bet):
    expect_ratio = bet / my_all_bet
    if total_pot <= (players * 20) and my_all_bet >= (init_bet / 6):
        return (True, bet, 0) if win_rate >= combat_threshold and expect_ratio < cofidience_ratio else (False, 0, 0)
    elif total_pot > players * 20 and my_all_bet >= init_bet / 6:
        if bet < total_pot:
            iv_value = (bet / total_pot)
            return (True, bet, iv_value) if win_rate > iv_value else (False, bet, iv_value)
        elif bet >= total_pot:
            if win_rate >= aggressive_threshold:
                return (True, bet, 0) if expect_ratio < cofidience_ratio else (False, 0, 0)
            else:
                return (False, 0, 0)
        else:
            return (False, 0, 0)
    elif total_pot > players * 20 and my_all_bet < init_bet / 6:
        # how to handel my rest bet is low??
        # do something
        return (False,0,0)
    else:
        return (False, 0, 0)


if __name__ == '__main__':
    win_rate_list = [float(x * 0.1) for x in xrange(1, 10)]
    my_all_bet = 600
    opponent_bet = 120
    total_pot = small_blind + big_blind + opponent_bet
    bets_list = [x * 10 for x in xrange(0, (my_all_bet+10)/10)]
    win_rate = win_rate_list[4]
    for bet in bets_list:
        (result, bet, value) = iv_calculation_1(win_rate, float(bet), float(total_pot), my_all_bet)
        # (result, bet, value) = iv_calculation_2(win_rate, float(bet), float(total_pot), my_all_bet)
        if result:
            print "total_pot %d " % total_pot
            print "should raise bet to %d" % bet
            print "Win rate: %f, iv vaule: %f" % (win_rate, value)
