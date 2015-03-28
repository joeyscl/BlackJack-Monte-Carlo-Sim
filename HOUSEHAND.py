__author__ = 'Joey'

import random
from HAND import HAND
from CARD import CARD

class HOUSEHAND(HAND):
    def __init__(self, cards):
        HAND.__init__(self,cards)
        self.housefinalstate = self.__HouseFinalState()

    '''Househand played independent of strategy; Used after playerdecision determined'''

    def __HouseFinalState(self):
        #Case0: house hits BJ
        if (self.getHandValue() == 21) and ( len(self.getNames()) == 2 ):
            return 'BJ'

        #Case1: househand -> hit (soft 17 or lower):
        elif (self.getHandValue() < 17) or (self.getHandValue() <= 17 and 'A' in self.getNames()):

            acecount = self.getNames().count('A')
            handvalue = self.getHandValue()

            while (handvalue < 17) or (handvalue <= 17 and acecount > 0):

                newcard = CARD.dealCard()
                newcardvalue = newcard.getVal()
                handvalue += newcardvalue

                if newcard.getName() == 'A':
                    acecount += 1

                # decision making tree
                if handvalue > 17 and handvalue <= 21:
                    return handvalue
                while handvalue > 21 and acecount > 0:
                    acecount -= 1
                    handvalue -= 10
                    continue

            if handvalue > 21:
                return 'BUST'
            else:
                return handvalue

        #case2: dealer -> stands
        elif self.getHandValue() >= 17 and self.getHandValue() <= 21:
            return self.getHandValue()

        #case3: dealer busts
        elif self.getHandValue() > 21 and 'A' not in self.getNames():
            return 'BUST'

''' for debugging
c1 = CARD('A')
c2 = CARD('A')

H1 = HOUSEHAND([c1,c2])
print(H1.getHandValue())
print(H1.getNames())
print(H1.getVals())
print(H1.housefinalstate)
'''