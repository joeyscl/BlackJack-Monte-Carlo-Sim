__author__ = 'Joey'

from SINGLEGAME import SingleGame

if __name__ == "__main__":

    trials = int(input("How many trials?"))
    games = int(input("How many games per trial?"))
    print("Running Monte Carlo blackjack simulation of %i trials of %i games" %(trials, games))

    totalresult = 0
    for t in range(trials):
        result = 0
        for i in range(games):
            result += SingleGame(None,None)
        ROI = 100*result/games
        print('The ROI for this trial is', ROI, '%')
        totalresult += ROI
    print('\n The overall ROI is', totalresult/trials, '%')