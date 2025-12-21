
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

# Black Jack:
# -----------
# -----------

# Rules:
# ------
# Played against the dealer


# Ways to win / lose:
#   If you get 21 before the dealer you win
#   Otherwise, get as close to 21 without going over, while having a hand total > dealer total
#   Golden rule: If you manage to get 7 cards IN A SINGLE HAND without going over 21, you 
#                automatically win
#   At the end of the round, the person closer to 21 wins
#   Automatic win: if the cards delt are ANY 10 value card + an Ace, BLACK JACK!
#   Automatic lose: if dealer gets black jack


# Decisions:
#   Hit             : Get another card
#   Stay            : Don't get another card - > player round ends, moves on to dealer round
#   Double down     : Player doubles the bet to get one more card, but can't get any more cards after
#   Split           : If player gets 2 of the same cards, they have the option to split it to 2 
#                       different hands
#                     To split, a separate bet has to be made
#                     If split, one hand gets another card, and decisions are made for this hand 
#                       till stay, bust, or BJ
#                     Once first hand round is complete, second hand gets the second card (repeate 
#                       directions for first hand)
#                     For any hand that has 2 of the same cards in the first round, a split 
#                       decision can be made ONLY ON THE FIRST ROUND
#   Surrender       : round ends, player loses half their bet


# Game logic:
# -----------
#   Everyone gets 2 cards:
#       - ALL player cards face up
#       - One dealer card face up and one face down
#       - If the dealer has a 10 value card face up, dealer "checks" hidden card for a black jack
#   Player plays first
#   Players keep making decisions until decision = "stay" or double down, or player busts or 21 / black jacks
#   If player has an ACE in his hand, value = 11 until total score > 21, in which case value = 1
#   Once all hands stay, dealer deals to self till dealer score >= 17


# Betting:
# --------
# Player initial pot: $1,000,000 --> Can't keep playing if you have no money
# Dealer initial pot: $10,000,000 --> Can't keep playing if you broke the casino

# Bet options: (Should only display bet options that are <= player pot)
#   $10,000 (minimum)
#   $25,000
#   $50,000
#   $75,000
#   $100,000

#   For every hand won, you player gets back bet x 2 (in a split hand, if one hand loses and one 
#       hand wins, player loses the chips in the lost hand and gets back bet x 2 on the hand that
#       won)
#   If you win by blackjack, you get 150% of your bet back


# Results:
# --------
#   Win         : player winnings = bet x 2
#   Gold win    : player winnings = bet x 2 (happens when a player has 7 cards in one hand)
#   Lose        : player winnings = bet - bet
#   Bust        : player winnings = bet - bet
#   Black Jack  : player winnings = bet + (bet x 1.5)
#   Push        : player winnings = bet
#   Surrender   : player winnings = bet / 2

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

import random

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

# Creating card deck:
# -------------------

card_base = ['2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '10' , 'J' , 'Q' , 'K' , 'A']
card_face = ['♠' , '♥' , '♦', '♣']

card_deck = []
for card in card_base: # --------------------------------------------------------------------------- Appends each card value to a face to create a 52 card deck
    for face in card_face:
        c  = card + face
        card_deck.append(c)

card_values = []
for card in card_deck:

    if len(card) == 2: # --------------------------------------------------------------------------- If the card is not a 10 of any face
        val = card[0]
        try:
            val = int(val) # ----------------------------------------------------------------------- Checking if it's a face card or not
            val_list = [val , val]
            card_values.append(val_list) # --------------------------------------------------------- If not a face card, append the value of the card
        except ValueError:
            if card[0] == 'A': # ------------------------------------------------------------------- If card is an ACE, initial value of card is 11, otherwise 1
                card_values.append([11 , 1])
            else:    
                card_values.append([10 , 10]) # ---------------------------------------------------- If card is a face card, value is 10
    else:
        card_values.append([10 , 10]) # ------------------------------------------------------------ if the card is a 10, value is 10

card_dict = dict(zip(card_deck , card_values))

# ACE COMPENSATION: -- the reason why every card has 2 values
# Each card has 2 values: (x , y)
# x = uncompensated ; y = compensated
# For all cards except ACE, x = y
# For ACE: if hand total < 21, then x; else y

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

# Creating pots:
player_initial_pot = 1_000_000
dealer_initial_pot = 10_000_000

pots = (player_initial_pot , dealer_initial_pot)

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def money(amount):
    '''Converts money integer into a proper string display'''
    return f"${amount:,}"

# ----------------------------

def bet_display(player_pot , dealer_pot):
    '''Creates the display for bet options available, and receives and returns valid bet input'''
    
    bet_options = {1 : 10_000  ,
                   2 : 25_000  , 
                   3 : 50_000  , 
                   4 : 75_000  , 
                   5 : 100_000 , 
                   6 : 250_000 ,
                   }
    
    print()
    print("Bet options:")
    print()
    
    bet_choices = ['']
    for bet in bet_options:
        if bet_options[bet] < player_pot and bet_options[bet] < dealer_pot:
            bet_choices.append(str(bet))
            bet_value = bet_options[bet]
            if bet == 1:
                print(f"{bet} : {money(bet_value)}  (minimum)")
            else:
                print(f"{bet} : {money(bet_value)}")
    
    print()
    bet_choice = input(f"Choose your bet amount (1 - {bet_choices[-1]} or 'Enter' to bet minimum) :    ")
    while bet_choice not in bet_choices:
        bet_choice = input(f"Invalid input... Choose your bet amount (1 - {bet_choices[-1]} or 'Enter' to bet minimum) :    ")
    
    if bet_choice == '':
        bet_amount = bet_options[1] # bet the minimum
    else:
        bet_amount = bet_options[int(bet_choice)]
    
    return bet_amount

# ----------------------------

def bet(pots):
    '''Prompts player for bet amount'''
    
    player_pot = pots[0]
    dealer_pot = pots[1]
    
    bet_amount = bet_display(player_pot , dealer_pot)
    
    player_pot -= bet_amount
    
    pots = [player_pot , dealer_pot]
    
    return_bet = {"Bet" : bet_amount , "Pots" : pots}
    
    return return_bet

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def check_balance(pots):
    
    player_pot = pots[0]
    dealer_pot = pots[1]
    
    if player_pot >= 10_000 and dealer_pot >= 10_000:
        return [True , '']
    else:
        if player_pot < 10_000:
            return [False , 'Player']
        else:
            return [False , 'Dealer']

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def space_formatter(lst):
    '''Formats display outputs by equalizing spacing such that results line up in a column'''
    
    max_len = 0
    for e in lst:
        if len(e) > max_len:
            max_len = len(e)
    spaces_list = []
    for o in (lst):
        spaces = max_len - len(o) # ---------------------------------------------------------------- Calculates number of whitespaces required 
#                                                                                                    for each list element for all elements to line up
#                                                                                                    in the display when systematically printed in a loop
        spaces_list.append(spaces)
        
    return spaces_list

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def deck_shuffle(card_deck):
    '''Thoroughly shuffles a deck of cards'''
    
    dec_len = int(len(card_deck) / 2)
    
    random.shuffle(card_deck)
    
    deck_1 = card_deck[0:dec_len]
    deck_2 = card_deck[dec_len:]
    random.shuffle(deck_1)
    random.shuffle(deck_2)
    
    shuffled_deck = []
    
    for i, card in enumerate(deck_1):
        shuffled_deck.append(deck_1[i])
        shuffled_deck.append(deck_2[i])
    
    random.shuffle(shuffled_deck)
    
    return shuffled_deck

# --------------------------------
    
def deck_reset(card_deck = card_deck , card_dict = card_dict):
    '''Shuffles deck'''
    
    card_base = ['2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '10' , 'J' , 'Q' , 'K' , 'A']
    card_face = ['♠' , '♥' , '♦', '♣']

    card_deck = []
    for card in card_base:
        for face in card_face:
            c  = card + face
            c2 = card + face # --------------------------------------------------------------------- Using 2 decks to reduce the odds of a black jack
            card_deck.append(c)
            card_deck.append(c2)
    
    deck = deck_shuffle(card_deck)
    
    return deck

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def seven_counter(player_hand): # ------------------------------------------------------------------ Checks to see if at any point the playere has 7 cards in hand
    '''Checks to see if player has 7 cards in their hand'''
    
    count = 0
    for card in player_hand:
        count += 1
    
    if count >= 7:
        return True
    
    return False

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def ace_finder(hand):
    '''Captures the index of every ace in the hand if any'''
    
    aces = []
    for i , card in enumerate(hand): # ------------------------------------------------------------- finding all indexes where an ace exists
        if card != "" and card[0] == 'A':
            aces.append(i)
    
    if len(aces) > 0:
        has_ace = True
    else:
        has_ace = False
    
    aces.reverse() # ------------------------------------------------------------------------------- reversing index list so it can work from the end, not beginning
    
    return [aces , has_ace]

# ----------------------------

def value_finder(hand , card_dict = card_dict):
    '''Gets the value for each card in the hand'''
    
    hand_values = []
    
    for card in hand:
        if card == "":
            hand_values.append(0)
        else:
            hand_values.append(card_dict[card][0])
    
    return hand_values

# ----------------------------

def value_calc(hand , card_dict = card_dict): # ---------------------------------------------------- Calculates final value of hand
    '''Calculates the total value of the player/dealer hand'''
    
    a = ace_finder(hand)
    aces = a[0]
    has_ace = a[1]
    
    values = value_finder(hand)
    tot_value = sum(values)
    
    ace_comp_idx = [] # ---------------------------------------------------------------------------- Holds the indeces of the aces where the value got compensated
    
    index = 0
    if has_ace and tot_value > 21: # --------------------------------------------------------------- Checks to see if ace should compensate with low value
        while tot_value > 21 and index < len(aces):
            tot_value -= 10
            ace_comp_idx.append(aces[index])
            index += 1
        return [tot_value , ace_comp_idx]
    else:
        return [tot_value , ace_comp_idx]

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def status(move):
    '''Check to see whether player is still in the game'''
    
    stop_decisions = ['Stay' , 'Double Down' , 'Surrender']
    
    if move in stop_decisions:
        return True
    else:
        return False

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def assess_score(player_hand , player_total , dealer_total):
    '''Compares the player score to dealer's'''
    
    golden_rule = seven_counter(player_hand) # ----------------------------------------------------- Checks to see if player has 7 cards in hand
    
    if not golden_rule: # -------------------------------------------------------------------------- Player doesn't have 7 cards in hand
        if player_total == dealer_total: # --------------------------------------------------------- Tie
            
            player_loss , player_won = False , False
            
            if player_total == 21 and dealer_total == 21: # ---------------------------------------- Player and dealer both have black jack
                message = "Fuckin' hell, what were the odds of THAT?!"
            else:
                message = "It's a push!"
                
            return [player_loss , player_won , message]
        
        else: # ------------------------------------------------------------------------------------ Not a tie
            if dealer_total == 21 or player_total > 21 or player_total < dealer_total: # ----------- Dealer wins
                
                player_loss , player_won = True , False
                
                if dealer_total == 21:
                    message = "... well FUCK!"
                elif player_total > 21:
                    message = "DAMN! You went over..."
                else:
                    message = "Aw, you fell short!"
                    
                return [player_loss , player_won , message]
            
            elif player_total == 21 or player_total > dealer_total or dealer_total > 21: # --------- Player wins
                
                player_loss , player_won = False , True
                
                if player_total == 21:
                    message = "HOLY SHIT!! YOU JUST GOT BLACK JACK!!!!"
                elif player_total > dealer_total:
                    message = "Nice! You outplayed the dealer!!"
                else:
                    message = "Woohoo!! Dealer busts!"
                    
                return [player_loss , player_won , message]
            
            else:
                
                player_loss , player_won = False , False
                message = "On to next round!"
                
                return [player_loss , player_won , message]
            
    else: # ---------------------------------------------------------------------------------------- Player has 7 cards in hand
        player_loss , player_won = False , True
        message_1 = "Damn... you literally just won with sheer dumb luck.."
        message_2 = "Can't decide if it's impressive or if you have a problem..."
        message = message_1 + "\n" + message_2

        return [player_loss , player_won , message]

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def create_display_header():
    
    print()
    print()
    
    display_title   = "     PLAYER          DEALER     "
    border          = "-" * len(display_title)
    
    header = [display_title , border]
    
    return header

# ------------------------

def create_display_tail(totals):
    '''Creates the display for tail border and "Totals"'''
    
    player_total = totals[0]
    dealer_total = totals[1]
    
    total_display_masked = "Total:" + (" " * 4) + f"{player_total}"
    
    if len(total_display_masked) == 12:
        value_spaces  = ' ' * 14
        total_display = "Total:" + (" " * 4) + f"{player_total}{value_spaces}{dealer_total}"
    else:
        value_spaces  = ' ' * 15
        total_display = "Total:" + (" " * 4) + f"{player_total}{value_spaces}{dealer_total}"
    
    return [total_display , total_display_masked]

# ------------------------

def ace_compensation_display(card, card_idx , ace_comp_idx , card_dict = card_dict):
    '''Captures true value of card based on ace compensation'''
    
    if card != "":    
        if card_idx in ace_comp_idx:
            card_value = card_dict[card][1]
        else:
            card_value = card_dict[card][0]
    else:
        card_value = ""

    return card_value

# ------------------------

def build_display_body(hands                    , 
                       totals                   , 
                       ace_comps_idx            , 
                       pots                     ,
                       total_bet                ,
                       card_dict = card_dict    ,
                       ):
    '''Constructs the body for all displays'''
    
    player_hand  = hands[0].copy()
    dealer_hand  = hands[1].copy()
    
    # player_total = totals[0]
    # dealer_total = totals[1]
    
    player_pot = pots[0]
    dealer_pot = pots[1]
    
    len_player_hand = len(player_hand)
    len_dealer_hand = len(dealer_hand)
    len_diff = abs(len_player_hand - len_dealer_hand)
    
    for i in range(len_diff):
        if len_player_hand < len_dealer_hand:
            player_hand.append("")
        else:
            dealer_hand.append("")
    
    ace_comp_idx_player = ace_comps_idx[0]
    ace_comp_idx_dealer = ace_comps_idx[1]
    
    player_spaces = space_formatter(player_hand)
    dealer_spaces = space_formatter(dealer_hand)
    
    player_list = []
    dealer_list = []
    dealer_list_masked = []
    
    body = []
    body_masked = []
    
    underline = "----------"
    
    print('\n' * 2)
    print('-' * 65)
    print('-' * 65)
    print('\n' * 2)
    
    print(f"Player stake : {money(total_bet)}")
    print("------------")
    print()
    
    player_pot_display = f"Player pot : {money(player_pot)}"
    dealer_pot_display = f"Dealer pot : {money(dealer_pot)}"
    spaces_after_player_pot_display = ' ' * (60 - (len(player_pot_display) + len(dealer_pot_display)))
    spaces_after_underline = ' ' * (len(spaces_after_player_pot_display) + len(money(player_pot)) + 3)
    pots_display = f"{player_pot_display}{spaces_after_player_pot_display}{dealer_pot_display}"
    underline_display = f"{underline}{spaces_after_underline}{underline}"
    
    print(pots_display)
    print(underline_display)
    print('\n' * 2)
    
    for i, e in enumerate(player_hand):
        
        # Player:
        # -------
        player_card_value = ace_compensation_display(e, i, ace_comp_idx_player)
        
        player_stats              = f"{player_hand[i]} {' ' * player_spaces[i]}: {player_card_value}"
        spaces_after_player_stats = ' ' * (21 - (5 + len(player_stats)))
        
        player_line = f"     {player_stats}{spaces_after_player_stats}"
        player_list.append(player_line)
        
        # ----------------------------
        
        # Dealer:
        # -------
        dealer_card_hand_true = ace_compensation_display(dealer_hand[i], i, ace_comp_idx_dealer)
                
        dealer_stats_true   = f"{dealer_hand[i]} {' ' * dealer_spaces[i]}: {dealer_card_hand_true}"
        dealer_list.append(dealer_stats_true)
        
        if i == 0:
            dealer_card_hand_masked = card_dict[dealer_hand[i]][0]
            dealer_stats_masked     = f"{dealer_hand[i]} {' ' * dealer_spaces[i]}: {dealer_card_hand_masked}"
        elif i == 1:
            dealer_stats_masked       = "   X"
        else:
            dealer_stats_masked       = ""
        
        dealer_list_masked.append(dealer_stats_masked)
    
    for i , stat in enumerate(player_list):
        line        = player_list[i] + dealer_list[i]
        line_masked = player_list[i] + dealer_list_masked[i]
        
        body.append(line)
        body_masked.append(line_masked)
    
    return [body , body_masked]

# ------------------------
    
def create_initial_display(display_package , card_dict = card_dict):
    
    # hands           = [player_hand , dealer_hand]
    # totals          = [player_total , dealer_total]
    # ace_comps_idx   = [ace_comp_idx_player , ace_comp_idx_dealer]
    
    # display_package = {
    #     "Hands"     : hands         ,
    #     "Totals"    : totals        ,
    #     "AC_id"     : ace_comps_idx ,
    #     "Pots"      : pots          ,
    #     "Bet"       : bet_amount    ,
    #     }
    
    hands           = display_package["Hands"].copy()
    totals          = display_package["Totals"].copy()
    ace_comps_idx   = display_package["AC_id"].copy()
    pots            = display_package["Pots"].copy()
    bet_amount      = display_package["Bet"]

    header             = create_display_header()
    # display_title      = header[0]
    border             = header[1]
    
    stat_lines         = header
    stat_lines_masked  = stat_lines.copy()
    
    display_tail         = create_display_tail(totals) # ------------------------------------------- returns [total_display , total_display_masked]
    total_display_masked = display_tail[1]
    total_display        = display_tail[0]
    
    body_constructs = build_display_body(hands          = hands             ,
                                         totals         = totals            ,
                                         ace_comps_idx  = ace_comps_idx     ,
                                         pots           = pots              ,
                                         total_bet      = bet_amount        ,
                                         )
    
    body        = body_constructs[0]
    body_masked = body_constructs[1]
    
    for i , e in enumerate(body):
        stat_lines.append(body[i])
        stat_lines_masked.append(body_masked[i])    
    
    stat_lines.append(border)
    stat_lines.append(total_display)
    
    stat_lines_masked.append(border)
    stat_lines_masked.append(total_display_masked)
    
    all_stats = [stat_lines , stat_lines_masked]
    
    return all_stats

# ------------------------

def print_display(lines):
    
    for line in lines:
        print(line)
    print('\n' * 2)
    
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def split_display(player_hand1 , player_hand2 , dealer_hand , card_dict = card_dict):
    '''Special display if played move = "Split"'''

# ------------------------

def pad_display_update(body , totals , masked = True):
    '''Constructs the "Hit" display update'''
    
    header             = create_display_header()
    # display_title      = header[0]
    border             = header[1]
    
    stat_lines = header # -------------------------------------------------------------------------- Reinitializing stat_lines
    
    for e in body:
        stat_lines.append(e)
    stat_lines.append(border)
    
    tail = create_display_tail(totals) # [total_display , total_display_masked]
    
    total_display        = tail[0]
    total_display_masked = tail[1]
    
    if masked:
        stat_lines.append(total_display_masked)
    else:
        stat_lines.append(total_display)
    
    return stat_lines

# ------------------------

def construct_display(hands , totals , ace_comps_idx , pots , bet_amount):
    '''Constructs the full display'''
    
    body = build_display_body(hands         = hands         ,
                              totals        = totals        ,
                              ace_comps_idx = ace_comps_idx ,
                              pots          = pots          ,
                              total_bet     = bet_amount    ,
                              )
    
    body_unmasked = body[0]
    body_masked   = body[1]
    
    stat_lines        = pad_display_update(body_unmasked , totals , masked = False)
    stat_lines_masked = pad_display_update(body_masked , totals)
    
    return [stat_lines , stat_lines_masked]


# ------------------------

def update_display(display_package , card_dict = card_dict):
    '''Updates the display based on the move made by either player or dealer'''
    
    # display_package = {
    #     "Hands"     : hands             ,
    #     "Totals"    : totals            ,
    #     "AC_id"     : ace_comps_idx     ,
    #     "Display"   : stats             ,
    #     "Move"      : move              ,
    #     "Player"    : player            ,
    #     "Pots"      : pots              ,
    #     "Bet"       : bet_amount        ,
    #     }
        
    hands           = display_package["Hands"].copy()
    totals          = display_package["Totals"].copy()
    ace_comps_idx   = display_package["AC_id"].copy()
    pots            = display_package["Pots"].copy()
    bet_amount      = display_package["Bet"]
    
    return construct_display(hands , totals , ace_comps_idx , pots , bet_amount)


    # split_display()
    
# ------------------------

def deal(pots , bet_amount):
    '''Deals the first hand in Black Jack'''
        
    deck = deck_reset()
    
    player_hand = []
    dealer_hand = []
    
    for deal in range(2):
        player_hand.append(deck.pop())
        dealer_hand.append(deck.pop())
    
    player_calc             = value_calc(player_hand) # [tot_value , ace_comp_idx , ace_compensated]
    player_total            = player_calc[0]
    ace_comp_idx_player     = player_calc[1]
    
    dealer_calc             = value_calc(dealer_hand)
    dealer_total            = dealer_calc[0]
    ace_comp_idx_dealer     = dealer_calc[1]
    
    hands           = [player_hand , dealer_hand]
    totals          = [player_total , dealer_total]
    ace_comps_idx   = [ace_comp_idx_player , ace_comp_idx_dealer]
    
    display_package = {
        "Hands"     : hands         ,
        "Totals"    : totals        ,
        "AC_id"     : ace_comps_idx ,
        "Pots"      : pots          ,
        "Bet"       : bet_amount    ,
        }
    
    display = create_initial_display(display_package)
    
    # display_result_masked = display[1] # ----------------------------------------------------------- 1 = masked , 0 = unmasked --> Printing masked stats 
    # display_result_true   = display[0]
    
    assessment = assess_score(player_hand = player_hand , 
                              player_total = player_total , 
                              dealer_total = dealer_total , 
                              )
    
    player_status   = assessment[:2] # ------------------------------------------------------------- [player_loss , player_won] (Boolean)
    message         = assessment[-1]
    
    # print()
    # print_display(display_result_true)
    
    return_dict = {
        "Hands"     : hands                 ,
        "Totals"    : totals                ,
        "AC_id"     : ace_comps_idx         ,
        "Deck"      : deck                  ,
        "Display"   : display               ,
        "Pots"      : pots                  ,
        "Bet"       : bet_amount            ,
        "Status"    : player_status         ,
        "Message"   : message               ,
        }

    return return_dict

# return_bet = bet(pots)
# bet_amount = return_bet["Bet"]
# pots = return_bet["Pots"]
# start = deal(pots , bet_amount)

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def display_moves(player_hand):
    '''Provides a list of valid decisions'''    
    dec_vals = [1 , 2 , 3 , 4 , 5]
    decisions = ['Hit' , 'Stay' , 'Double Down' , 'Surrender'  , 'Split']
    dec_dict = dict(zip(dec_vals , decisions))
    
    lines = []
        
    for key in dec_dict:
        lines.append(f"Type {key} to {dec_dict[key]}")
        
    if player_hand[0] == player_hand[1]:
        for line in lines:
            print(line)
        return [dec_vals , dec_dict]
    else:
        for line in lines[:4]:
            print(line)
        return [dec_vals[:4] , dec_dict]

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def capture_decision(player_hand):
    '''Captures the correct decision input'''
    
    disp_moves = display_moves(player_hand)
    dec = disp_moves[0]
    dec_dict = disp_moves[1]
    
    error = True
    while error:
        move = input("Select your move:    ")
        try:
            move = int(move)
            if move not in dec:
                print("Invalid input. Please enter move from options provided...")
                error = True
            else:
                error = False
        except ValueError:
            print("Invalid input. Please enter move from options provided...")
            error = True
    
    return [move , dec_dict[move]]

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def hit_values_update(hands , totals , ace_comp_idx , deck , player):
    '''Performs a hit to the player / dealer hand and recalculates all values'''
    
    player_hand         = hands[0]
    dealer_hand         = hands[1]
    player_total        = totals[0]
    dealer_total        = totals[1]
    ace_comp_idx_player = ace_comp_idx[0]
    ace_comp_idx_dealer = ace_comp_idx[1]
    
    if player:
        
        player_hand.append(deck.pop()) # ----------------------------------------------------------- Player is dealt another card from the deck
        player_calc             = value_calc(player_hand)
        player_total            = player_calc[0]
        ace_comp_idx_player     = player_calc[1]
        
        assessment = assess_score(player_hand = player_hand , 
                                  player_total = player_total , 
                                  dealer_total = dealer_total , 
                                  )
        
        player_status   = assessment[:2] # --------------------------------------------------------- [player_loss , player_won] (Boolean)
        message         = assessment[-1]
        
        # if len(ace_comp_idx_player) == 0:
        #     ace_comp_idx_player = [" "]
        # if len(ace_comp_idx_dealer) == 0:
        #     ace_comp_idx_dealer = [" "]
        
        
        hands           = [player_hand , dealer_hand]
        totals          = [player_total , dealer_total]
        ace_comps_idx   = [ace_comp_idx_player , ace_comp_idx_dealer]
        
        return [hands , totals , ace_comps_idx , player_status , message]
        
    else:
        dealer_hand.append(deck.pop()) # ----------------------------------------------------------- Dealer is dealt another card from the deck
        dealer_calc             = value_calc(dealer_hand)
        dealer_total            = dealer_calc[0]
        ace_comp_idx_dealer     = dealer_calc[1]
        
        assessment = assess_score(player_hand = player_hand , 
                                  player_total = player_total , 
                                  dealer_total = dealer_total , 
                                  )
        
        player_status   = assessment[:2] # --------------------------------------------------------- [player_loss , player_won] (Boolean)
        message         = assessment[-1]
        
        # if len(ace_comp_idx_player) == 0:
        #     ace_comp_idx_player = [" "]
        # if len(ace_comp_idx_dealer) == 0:
        #     ace_comp_idx_dealer = [" "]
            
        hands           = [player_hand , dealer_hand]
        totals          = [player_total , dealer_total]
        ace_comps_idx   = [ace_comp_idx_player , ace_comp_idx_dealer]

        return [hands , totals , ace_comps_idx , player_status , message]

# ------------------------------------------

def hit(return_dict , player = True):
    '''Player / dealer receives another card'''
    
    # return_dict = {
    #     "Hands"     : hands             ,
    #     "Totals"    : totals            ,
    #     "AC_id"     : ace_comps_idx     ,
    #     "Deck"      : deck              ,
    #     "Display"   : display           ,
    #     "Pots"      : pots              ,
    #     "Bet"       : bet_amount        ,
    #     }
    
    hands           = return_dict["Hands"]
    totals          = return_dict["Totals"]
    ace_comps_idx   = return_dict["AC_id"]
    deck            = return_dict["Deck"]
    stats           = return_dict["Display"]
    pots            = return_dict["Pots"]
    bet_amount      = return_dict["Bet"]
    
    move = "Hit"
    
    # hit_values_update(player_hand , dealer_hand , deck , player_tag = True):
    
    if player:
        
        print()
        print("Player receives another card")
        print()
        
        hit_value = hit_values_update(hands , totals , ace_comps_idx , deck, player) # ----------------------------- Player is dealt another card and all values recalculated / [hands , totals , ace_comps_idx , player_status , message]
        
        hands           = hit_value[0]
        totals          = hit_value[1]
        ace_comps_idx   = hit_value[2]
        player_status   = hit_value[3]
        message         = hit_value[4]
        
        display_package = {
            "Hands"     : hands             ,
            "Totals"    : totals            ,
            "AC_id"     : ace_comps_idx     ,
            "Display"   : stats             ,
            "Move"      : move              ,
            "Player"    : player            ,
            "Pots"      : pots              ,
            "Bet"       : bet_amount        ,
            }
        
        display = update_display(display_package)
        
        display_result_masked = display[1] # ----------------------------------------------------------- 1 = masked , 0 = unmasked --> Printing masked stats 
        display_result_true   = display[0]
        
        print_display(display_result_masked)
        # print_display(display_result_true)
        
        return_dict = {
            "Hands"   : hands         ,
            "Totals"  : totals        ,
            "AC_id"   : ace_comps_idx ,
            "Deck"    : deck          ,
            "Display" : display       ,
            "Status"  : player_status ,
            "Move"    : move          ,
            "Message" : message       , # Message needs to be displayed at the correct segment in player_playthrough() / dealer_playthrough()
            "Pots"    : pots          ,
            "Bet"     : bet_amount    ,
            }
        
        return return_dict
    
    else:
        
        print()
        print("Dealer receives another card")
        print()
        
        hit_value = hit_values_update(hands , totals , ace_comps_idx , deck, player) # ----------------------------- Dealer is dealt another card and all values recalculated
        
        hands           = hit_value[0]
        totals          = hit_value[1]
        ace_comps_idx   = hit_value[2]
        player_status   = hit_value[3]
        message         = hit_value[4]
        
        display_package = {
            "Hands"     : hands             ,
            "Totals"    : totals            ,
            "AC_id"     : ace_comps_idx     ,
            "Display"   : stats             ,
            "Move"      : move              ,
            "Player"    : player            ,
            "Pots"      : pots              ,
            "Bet"       : bet_amount        ,
            }
        
        display = update_display(display_package)
        
        display_result_masked = display[1] # ----------------------------------------------------------- 1 = masked , 0 = unmasked --> Printing masked stats 
        display_result_true   = display[0]
        
        # print_display(display_result_masked)
        print_display(display_result_true)
        
        return_dict = {
            "Hands"   : hands         ,
            "Totals"  : totals        ,
            "AC_id"   : ace_comps_idx ,
            "Deck"    : deck          ,
            "Display" : display       ,
            "Status"  : player_status ,
            "Move"    : move          ,
            "Message" : message       , # Message needs to be displayed at the correct segment in player_playthrough() / dealer_playthrough()
            "Pots"    : pots          ,
            "Bet"     : bet_amount    ,
            }
        
        return return_dict

return_bet = bet(pots)
bet_amount = return_bet["Bet"]
pots = return_bet["Pots"]
start = deal(pots , bet_amount)
test = hit(start)

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def stay(deck , player_hand , move = 'Stay'):
    '''Round ends and results are displayed'''
    
    print()
    print("This round has ended...")
    print()
    
    #stat = status(hand=player_hand , decision=move)
    
    # Progresses to dealer_playthrough()
    
    return [player_hand , deck]

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def double_down(deck, player_hand , move = "Double Down"):
    '''Round ends after played doubles bet and receives one last card'''
    
    print()
    print("Player doubles bet and receives one final card..")
    print("This round has ended..")
    print
    
    player_hand.append(deck.pop())
    
    # Bet doubles
    # Progresses to dealer_playthrough()
    
    return [player_hand , deck , move]

# ------------------------

def surrender(deck , player_hand , move = "Surrender"):
    '''Round ends. Player loses half their bet'''

    print()
    print("Player loses only half their bet..")
    print("This round has ended..")
    print
    
    # pot -= bet/2
    
    return [player_hand , deck , move]

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def split():
    '''If in the first round player has identical cards, player can split them into two hands'''
    
    # If the cards in the hand on deal are the same and there's enough money in the pot to add
    #   a matching bet to the second hand, player will have the option to split
    
    # If a player decides to split, hand will be divided into hand 1 and hand 2
    # Hand 1 will get a new card for a new 2 card hand, return_dict[hand1] is reconstructed and processed
    #   through assess score and displayed accordingly.
    # Once player round comes to an end (win, bust, or stop) return_dict[hand2] is constructed
    #   based on the values of the return_dict[hand1]
    # If hands either win or bust, logic is easy
    # if hand stays, a return_dict[3] needs to be created based off return_dict[hand2] before
    #   proceeding to dealer_playthrough()
    # Split will have it's own custom display function so previous functions wont be used

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def game_start(pots):
    
    initial_bet = bet(pots)
    
    bet_amount = initial_bet["Bet"]
    pots = initial_bet["Pots"]
    
    start = deal(pots , bet_amount)
    
    return start

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def player_playthrough(return_dict):
    '''Plays through player options till player hits a stop option'''
    
    pots = return_dict['Pots']
    
    display = return_dict["Display"]
    
    display_result_true   = display[0]
    display_result_masked = display[1] # ----------------------------------------------------------- 1 = masked , 0 = unmasked --> Printing masked stats 
    
    status  = return_dict['Status']
    message = return_dict['Message']
    
    player_lost     = status[0]
    player_won      = status[1]
    
    if not player_lost and not player_won:
        player_still_in_game = True
    else:
        player_still_in_game = False
    
    if not player_still_in_game:
        
        print()
        print_display(display_result_true)
        print()
        print(message)
        print()
        
        balance         = check_balance(pots)
        balance_exists  = balance[0]
        balance_account = balance[1]
        
        if balance_exists:
            
            play_prompt_ops = ['Y' , 'N']
            
            print()
            
            invalid = True
            next_round = input("Want to go another round? [Y/N]:    ").upper()
            while invalid:
                try:
                    next_round = input("Want to go another round? [Y/N]:    ").upper()
                    if next_round not in play_prompt_ops:
                        print("Enter 'y' or 'n' only...")
                        print()
                        invalid = True
                    else:
                        invalid = False
                except SyntaxError:
                    print("Enter 'y' or 'n' only...")
                    print()
                    invalid = True
                    
            if next_round == 'Y':
                
                print()
                print('-' * 65)
                print('-' * 65)
                print()
                
                start = game_start(pots)
                message = start["Message"]
                print(message)
                print()
                
                player_playthrough(start)
                
            else:
                print()
                print("GG, let's play again another time!")
                print('\n' * 3)
                
                return
            
        else:
            if balance_account == "Player":
                print()
                print(f"{balance_account} pot doesn't have enough funds to keep playing...")
                print()
                print("You were utterly depleated and royally defeated! You might have a gambling problem....")
                print('\n' * 3)
            else:
                print()
                print(f"{balance_account} pot doesn't have enough funds to keep playing...")
                print()
                print("Yo we got Ocean's Eleven over here, you cleaned out the casino!!!")
                print("GG")
                print('\n' * 3)
            
            return
    
    else:
        
        print()
        print_display(display_result_masked)
        print()
        print(message)
        print()
    
        # decision_actions = {
        #     "Hit"  : hit,
        #     "Stay" : stay,
        #     "Double Down" : double_down,
        #     "Surrender" : surrender,
        #     "Split" : split,
        #     }
        
        
        # Player makes a decision
        # If decision in stop decisions:
            # assess_score()
            # if player_still_in_game --> dealer_playthrough(return_dict)
            # else --> player_playthrough(return_dict) --> (should trigger base case)
        # else --> return_dict = decision_actions[action] --> player_playthrough(return_dict)
        
        
        
        

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

# Game play debugging:
# --------------------

# return_dict = {
#     "Hands"     : hands                 ,
#     "Totals"    : totals                ,
#     "AC_id"     : ace_comps_idx         ,
#     "Deck"      : deck                  ,
#     "Display"   : display               ,
#     "Pots"      : pots                  ,
#     "Bet"       : bet_amount            ,
#     "Status"    : player_status         ,
#     "Message"   : message               ,
#     }

def black_jack():
    
    play_prompt_ops = ['Y' , 'N']
    
    print('\n' * 3)
    print("Welcome!")
    print()
    
    invalid = True
    while invalid:
        try:
            play_prompt = input("Are you ready to play some Black Jack?! [Y/N]:    ").upper()
            if play_prompt not in play_prompt_ops:
                print("Enter 'y' or 'n' only...")
                print()
                invalid = True
            else:
                invalid = False
        except SyntaxError:
            print("Enter 'y' or 'n' only...")
            print()
            invalid = True
    
    if play_prompt != 'N':
        
        print('\n' * 2)
        print("Let's GOOOOO then!")
        print('\n' * 2)
        
        player_initial_pot = 1_000_000
        dealer_initial_pot = 10_000_000
        
        initial_pots = (player_initial_pot , dealer_initial_pot)
        
        start = game_start(initial_pots)
        
        player_playthrough(start)
        
    
black_jack()





# **** Add bet_amount in assess score
# **** Modify the display such that the pot does not update till AFTER the round is finished and
#           money is either gained or lost
# New pot should be reflected AFTER the round is finished via assess score










