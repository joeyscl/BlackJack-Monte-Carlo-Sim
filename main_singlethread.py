__author__ = 'Joey'

from SINGLEGAME import SingleGame
import time

if __name__ == "__main__":

    while(True):
        
        print("This program calculates the ROI of Blackjack (assume zero deck penetration) using Monte Carlo method")
        print("")
        trials = int(input("How many trials?"))
        games = int(input("How many games per trial?"))
        print("Running Monte Carlo blackjack simulation of %i trials of %i games" %(trials, games))

        start_time = time.time()    
        totalresult = 0
        for oneTrial in range(trials):
            result = 0
            t = time.time()
            for i in range(games):
                result += SingleGame(None,None)
            ROI = 100*result/games
            print("The ROI for trial #", oneTrial, "is", ROI, "%")
            totalresult += ROI
            trialtime = time.time() - t
            print('Trial run time: ', round(trialtime,4), " seconds")
            print('')
            
        print('The overall ROI is', totalresult/trials, '%')

        duration = time.time() - start_time
        if duration < 300: #less than 300 seconds (ie: 5 minutes)
            print("Total time: ", duration, "seconds")

        elif duration < 3600: #less than 1 hour
            duration = duration / 60 #convert to minutes
            print ("Total time: ", duration, "minutes")

        elif duration < 172800: #less than 2 days
            duration = duration / 3600 #convert to hours
            print ("Total time: ", duration, "hours")

        else:
            duration = duration / 86400 #convert to days
            print ("Total time: ", duration, "days")

        tryAgain = input("Try again(Y/N)")
        if tryAgain == 'Y' or tryAgain =='y':
            continue
        else:
            break
