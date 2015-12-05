#Project: Swiss Pairings#
A python application to connect to a database and store information on players 
performance during a tournament that uses the swiss pairings model.

##Requirements##
Requires Python 2.7.x, Postgres 4.x 

##Installation##
* Unzip tournament.zip into a directory using your favorite unzipper
 e.g. on the commandline use `unzip tournament.zip`
* Alternatively clone the repo from [github](https://github.com/capt-marwil/tournament) by typing `git clone https://github.com/capt-marwil/tournament/`
* Open a console and navigate to the Projects Root Directory 'tournament'
* Fire up your postgress database server and create the database from the commandline with:  
    `psql -f tournament.sql`
* After creating the database run the provide unittests with `python tournament_test.py` to 
make sure you can access the database an everything works just fine

##Additional Features##
* Added support for an odd number of players
* Added def countPlayers() 
* Added a unit test in tournament_test.py 
"testReportMatchesOddNumberOfPlayers()" to make sure 

##Related Links:##
* [Swiss Pairing Rules in Chess](https://www.fide.com/fide/handbook.html?id=83&view=article)
* [Applying Swiss Tournament rules](http://senseis.xmp.net/?SwissPairing)
