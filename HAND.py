__author__ = 'Joey'

from CARD import CARD

class HAND(object):
    def __init__(self,cards): #cards is a list of CARD
        self.cards = cards        #list of CARD
        self.__cardnames = self.getNames()            #list of card names (strings)
        self.__cardvals = self.getVals()              #list of card values (int)
        self.__handvalue = self.getHandValue()        #total hand value (int)

    '''
    @staticmethod
    #returns list of CARDs as sorted
    def __sortCards(cards):
        return sorted(cards, key = lambda CARD: CARD.getName())
    '''

    #returns list of CARD.name (string)
    def getNames(self):
        listofnames = []
        for i in range(len(self.cards)):
            listofnames.append(self.cards[i].getName())
        return listofnames

    #returns list of CARD.val (int)
    def getVals(self):
        listofvals = []
        for i in range(len(self.cards)):
            listofvals.append(self.cards[i].getVal())
        return listofvals

    #returns new HAND, replacing first pop with push (used for evaluation of Aces)
    def __replace(self, push, pop):
        for i in range(len(self.cards)):
            if self.cards[i].getName() == pop:
                self.cards[i] = CARD(push)
                self.__init__(self.cards)
                break

    #returns numeric value of hand
    def getHandValue(self):
        if 'A' not in self.__cardnames or sum(self.__cardvals) <= 21:
            return sum(self.__cardvals)
        else:
            newsum = sum(self.__cardvals)
            aceCount = self.__cardnames.count('A')
            while (newsum > 21) and (aceCount > 0):
                self.__replace('A-', 'A')
                newsum = sum(self.__cardvals)
            return newsum

''' for debugging
c1 = CARD('A')
c2 = CARD('9')

H1 = HAND([c1,c2])
print(H1.getHandValue())
print(H1.getNames())
print(H1.getVals())
'''