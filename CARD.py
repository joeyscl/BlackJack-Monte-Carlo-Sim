__author__ = 'Joey'

import random

class CARD(object):
    def __init__(self,name):
        self.__name = name                            #name value (string)
        self.__val = self.getVal()                    #numeric value (int)

    @staticmethod
    def dealCard():
        num = random.randint(0,12)
        cards_available = 'A23456789TJQK'
        return CARD(cards_available[num])

    #returns card value (int)
    def getVal(self):
        #get card value from name using dictionary
        valuelist = {'A':11 ,
                     'A-':1,
                     '2':2 ,
                     '3':3 ,
                     '4':4 ,
                     '5':5 ,
                     '6':6 ,
                     '7':7 ,
                     '8':8 ,
                     '9':9 ,
                     'T':10,
                     'J':10,
                     'Q':10,
                     'K':10}
        val = valuelist[self.__name]
        return val

    #returns card name (str)
    def getName(self):
        return self.__name

'''
C1 = CARD.dealCard()
print(C1.getVal())
print(C1.getName())
'''