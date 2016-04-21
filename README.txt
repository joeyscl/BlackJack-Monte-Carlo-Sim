This is a Python3 program for computing the long run return of the game of black jack.

NOTES ON STRATEGY:
The single player in the simulation makes plays based on "basicstrategy.xlsx" which is the optimal strategy 
without variations in betting pattern (which is only beneficial if card-counting - see below).
Simply put, basicstrategy.xlsx describes the optimal strategy a player can employ.

NOTES ON RUN TIME:
It takes computer about 8 hours to simulate 1 Billion (1E9) individual games running on 4 processes.
You can expect 1 million games to take 30 ~ 90seconds on modern computers depending on how many processes you use.
(I have an i7 930- quad core CPU @ 2.8ghz)

NOTES ON RESULTS:
After running 1 trial of 500 million games, the results I get are comparable to the theoretical results
as per Wikipedia of ~0.6% in the house's favour.
(http://en.wikipedia.org/wiki/Blackjack#Rule_variations_and_their_consequences_for_the_house_edge)

NOTES ON CARD COUNTING:
It doesn't work for games that are played with multiple decks due to poor card penetration. Playing with 
shoes with multiple decks (usually 6+) has become standard practice in most casinos. This program does not
take card counting into account for reasons stated (also see below).

NOTES ON MODELLING:
This program assumes 0 card penetration (ie: The dealer is dealing from a shoe of infinite decks). 
The implication of this is this:
   In the situation one non-face card has already been dealt (ex: 9 of some suit),
   the chance of dealing another card of same value (ie: another 9) is this:
   7.37% for 6 deck shoe (standard in many Casinoes)
   7.69% for a shoe of infinite decks

   In the situation one face card has already been dealt (ex: Q of some suit),
   the chance of dealing another card of same value (10, J, Q, K) is this:
   30.45% for 6 deck shoe
   30.77% for a shoe of infinite decks

I have decided that the difference is minor enough and will implement this simplification in my model
