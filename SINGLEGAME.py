__author__ = 'Joey'

from CARD import CARD
from PLAYERHAND import PLAYERHAND
from HOUSEHAND import HOUSEHAND
import xlrd

workbook = xlrd.open_workbook('basicstrategy.xlsx')
hardtotalsheet = workbook.sheet_by_index(0)
softtotalsheet = workbook.sheet_by_index(1)
pairssheet     = workbook.sheet_by_index(2)

hardtotal = [[hardtotalsheet.cell_value(r,c) for c in range(1,hardtotalsheet.ncols)] \
             for r  in range(1,hardtotalsheet.nrows)]

softtotal = [[softtotalsheet.cell_value(r,c) for c in range(1,softtotalsheet.ncols)] \
             for r  in range(1,softtotalsheet.nrows)]

pairs = [[pairssheet.cell_value(r,c) for c in range(1,pairssheet.ncols)] \
             for r  in range(1,pairssheet.nrows)]

def SingleGame(playerhand,househand):

    '''initializing hands'''
    #initializing playerhand, deal 2 random cards if given None
    if playerhand == None:
        playerhand = PLAYERHAND([CARD.dealCard(),CARD.dealCard()])

    #deal 1 more card if given only 1 (from splitting)
    while len(playerhand.cards) < 2:
        playerhand = PLAYERHAND(playerhand.cards.append(CARD.dealCard()))

    #initializing househand, deal 2 random cards if given None
    if househand == None:
        househand = HOUSEHAND([CARD.dealCard(),CARD.dealCard()])

    #print(playerhand.getNames(), ' ',househand.getNames())

    def Player_Action(playerhand,househand,playerdecision):
    #this function is used for evaluating the result of the
    #player action based on hands and playerdecision (Hit,Stand,etc)

        #Action Functions:
        #for evaluating outcome when player Stands
        def Player_Stand(playerhand,househand):
            if type(househand.housefinalstate) == str:
                #house bust
                if househand.housefinalstate == 'BUST':
                    return 1
                #house BJ
                elif househand.housefinalstate == 'BJ':
                    return -1
            elif type(househand.housefinalstate) == int:
                #playerhand better than dealerhand
                if playerhand.getHandValue() > househand.housefinalstate:
                    return 1
                #playerhand worse than dealerhand (including house BJ)
                elif playerhand.getHandValue() < househand.housefinalstate:
                    return -1
                #push
                elif playerhand.getHandValue() == househand.housefinalstate:
                    return 0

        #for evaluating outcome when player Hits
        def Player_Hit(playerhand,househand):
            newcard = CARD.dealCard()
            playerhand = PLAYERHAND(playerhand.cards + [newcard])
            return SingleGame(playerhand,househand)

        #for evaluating outcome when player Doubles down
        def Player_Double(playerhand,househand):
            newcard = CARD.dealCard()
            playerhand = PLAYERHAND(playerhand.cards + [newcard])
            return 2*Player_Stand(playerhand,househand)

        #for evaluating outcome when player Surrenders if allowed, otherwise Stand
        def Player_Rs(househand):
            if househand.housefinalstate == 'BJ':
                return -1
            else:
                return -0.5

        #for evaluating outcome when player Surrenders if allowed, otherwise Hit
        def Player_Rh(playerhand,househand):
            if househand.housefinalstate == 'BJ':
                return -1
            else:
                return Player_Hit(playerhand,househand)

        #for evaluating outcome when player Split
        def Player_SP(playerhand,househand):

            if 'A-' in playerhand.getNames():
                playerhand1 = PLAYERHAND([CARD('A')] + [CARD.dealCard()])
                playerhand2 = PLAYERHAND([CARD('A')] + [CARD.dealCard()])
                return SingleGame(playerhand1,househand) + SingleGame(playerhand2,househand)
            else:
                playerhand1 = PLAYERHAND([playerhand.cards[0]] + [CARD.dealCard()])
                playerhand2 = PLAYERHAND([playerhand.cards[1]] + [CARD.dealCard()])
                return SingleGame(playerhand1,househand) + SingleGame(playerhand2,househand)

        #for evaluating outcome when player Surrenders if allowed, otherwise split
        def Player_Rsp(playerhand,househand):
            if househand.housefinalstate == 'BJ':
                return -1
            else:
                return Player_SP(playerhand,househand)

        #Decision Tree
        #Case0: player gets 21:
        if playerhand.getHandValue() == 21:
            return Player_Stand(playerhand,househand)

        #CaseA: playerdecision == Stand
        if playerdecision == 'S':
            return Player_Stand(playerhand,househand)

        #CaseB: playerdecision == Hit
        if playerdecision == 'H':
            return Player_Hit(playerhand,househand)

        #CaseC: playerdecision == Double down
        if playerdecision == 'D':
            if len(playerhand.cards) == 2: #note: you can only double down on 2 cards
                return Player_Double(playerhand,househand)
            else:
                return Player_Hit(playerhand,househand)

        #CaseD: playerdecision == Rs (surrender if allowed, otherwise stand)
        if playerdecision == 'Rs':
            return Player_Rs(househand)

        #CaseE: playerdecision == Rh (surrender if allowed, otherwise hit)
        if playerdecision == 'Rh':
            return Player_Rh(playerhand,househand)

        #CaseF: playerdecision == Split
        if playerdecision == 'SP':
            return Player_SP(playerhand,househand)

        #CaseG: playerdecision == Rsp (surrender if allowed, otherwise split)
        if playerdecision == 'Rsp':
            return Player_Rsp(playerhand,househand)

    '''evaluating basic strategy based on playerhand and first of househand'''
    #case0: player hits BJ
    if playerhand.getHandValue() == 21 and  len(playerhand.cards) == 2:

        #dealer also hits BJ -> push
        if househand.housefinalstate == 'BJ':
            return 0
        #1.5x return otherwise
        else:
            return 1.5

    #Case1: player busts
    elif playerhand.getHandValue() > 21:
        return -1

    #Case2: playerhand does not contain Ace(s) and is not a pair
    elif ('A' not in playerhand.getNames()) and \
            (playerhand.getVals()[0] != playerhand.getVals()[1] or len(playerhand.cards) > 2 ):

        #calculate row value for strategy lookup
        row = 20 - playerhand.getHandValue()

        #calculate col value for strategy lookup
        if househand.getNames()[0] == 'A' or househand.getNames()[0] == 'A-':
            col= 9
        else:
            col = househand.getVals()[0] - 2

        #obtain player decision based on hard total strategy
        playerdecision = hardtotal[row][col]

        #player action based on player decision
        return Player_Action(playerhand,househand,playerdecision)

    #Case3: playerhand is a pair (or both face cards)
    elif len(playerhand.cards) == 2 and \
               ( (playerhand.getVals()[0] == playerhand.getVals()[1])
                 or ('A' in playerhand.getNames() and 'A-' in playerhand.getNames()) ):

        #calculate row value for strategy lookup
        if 'A' in playerhand.getNames():
            row = 0
        else:
            row = 11 - playerhand.getHandValue()//2

        #calculate col value for strategy lookup
        if househand.getNames()[0] == 'A' or househand.getNames()[0] == 'A-':
            col= 9
        else:
            col = househand.getVals()[0] - 2

        playerdecision = pairs[row][col]

        #player action based on player decision
        return Player_Action(playerhand,househand,playerdecision)

    #Case4: playerhand contains ace(s) (but does not start with 2 aces)
    elif 'A' in playerhand.getNames() and \
            (playerhand.getNames()[0] != playerhand.getNames()[1] or len(playerhand.cards) > 2):

        #calculate row value for strategy lookup
        row = 9 - (playerhand.getHandValue()- playerhand.getNames().count('A')*11)

        #calculate col value for strategy lookup
        if househand.getNames()[0] == 'A' or househand.getNames()[0] == 'A-':
            col= 9
        else:
            col = househand.getVals()[0] - 2

        #obtain player decision based on hard total strategy
        playerdecision = softtotal[row][col]

        #player action based on player decision
        return Player_Action(playerhand,househand,playerdecision)





''' for debugging
c1= CARD('A')
c2= CARD('A')

c3= CARD('Q')
c4= CARD('T')
c5= CARD('A')

househand = HOUSEHAND([c1,c2])
playerhand = PLAYERHAND([c3,c4])
print(househand.housefinalstate)
print(SingleGame(playerhand,househand))

'''



