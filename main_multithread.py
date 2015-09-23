__author__ = 'Joey'

'''
This is a program for computing the long run return of the game of black jack.

You can expect 1 million games to take 30 ~ 90seconds on modern computers
depending on how many processes you use.

Please see README.txt for other notes
'''   

import time
from multiprocessing import Pool
from SINGLEGAME import SingleGame

def trial(games_per_process):

    result = 0
    for i in range(games_per_process):
        result += SingleGame(None,None)
    return result/games_per_process


if __name__ == "__main__":

    while True:

        print("This program calculates the ROI of Blackjack using Monte Carlo method")
        print("")
        trials = int(input("How many trials?"))
        games = int(input("How many games per trial?"))
        proc =  int(input("Number of processes would you like to utilize? (2~4 recommended)"))
        print("Running Monte Carlo blackjack simulation of %i trials of %i games using %i processes." %(trials, games, proc))

        start_time = time.time()
        #Set up list of processes we want to run (divvy up # of games into # of threads to make each trial faster)
        games_per_process = games // proc

        pool = Pool(processes = proc)           # start 'proc' number of processes
        totalresult = 0
        for eachtrial in range(trials):
            t = time.time()
            results = pool.map(trial, [games_per_process]*proc)
            ROI =  100*sum(results)/proc
            trialtime = time.time() - t
            print('The ROI for trial #', eachtrial+1, ' is ', float("{0:.4f}".format(ROI)), '%')
            print('Trial run time: ', round(trialtime,4), " seconds")
            totalresult = totalresult + ROI
            print('')
            
        print('The overall ROI is', totalresult/trials, '%')

        duration = time.time() - start_time
        if duration < 300: #less than 300 seconds (aka 5 minutes)
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
