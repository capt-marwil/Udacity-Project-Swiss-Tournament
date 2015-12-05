#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    cnx = connect()
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM matches;")
    cnx.commit()
    cnx.close()


def deletePlayers():
    """Remove all the player records from the database."""
    cnx = connect()
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM players;")
    cnx.commit()
    cnx.close()


def countPlayers():
    """Returns the number of players currently registered."""
    cnx = connect()
    cursor = cnx.cursor()
    cursor.execute("SELECT COUNT(*) FROM players;")
    r = cursor.fetchone()
    return int(r[0])


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    cnx = connect()
    cursor = cnx.cursor()
    cursor.execute('''
        INSERT INTO players
        (name)
        VALUES
        (%s)''', (name, )
        )
    cnx.commit()
    cnx.close


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    cnx = connect()
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM standings")
    result = cursor.fetchall()
    cnx.close()
    return result


def evenNumberOfPlayers():
    """Returns True if the number of registered Players is
    even, False if not"""
    cnx = connect()
    cursor = cnx.cursor()
    cursor.execute("SELECT COUNT(*) FROM players")
    result = cursor.fetchone()
    cnx.close()
    if result[0] % 2 == 0:
        return True
    else:
        return False


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    cnx = connect()
    cursor = cnx.cursor()
    cursor.execute('''
        INSERT INTO matches (player_one, player_two, winner)
         VALUES (%s, %s, %s)''', (winner, loser, winner))
    cnx.commit()
    cnx.close


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    cnx = connect()
    cursor = cnx.cursor()
    """ Determin whether there had been any matches at all"""
    cursor.execute("SELECT COUNT(*) FROM matches")
    result = cursor.fetchone()
    if result[0] == 0:
        """
        No matches have been played so far.
        Get number of players and devide result by two
        """
        cursor.execute("SELECT id, name FROM players")
        result = cursor.fetchall()
        for i in range(0, len(result)):
            if i + 1 > len(result) / 2:
                """
                break out of the loop
                if no more pairings are possible
                """
                break
            else:
                return [
                            (
                                result[i][0],
                                result[i][1],
                                result[len(result) / 2 + 1 + i][0],
                                result[len(result) / 2 + 1 + i][1]
                            )
                        ]
    else:
        """
        Matches have been played,
        get pairings for next round

        """
        pairings = []
        cursor.execute("SELECT * FROM standings")
        result = cursor.fetchall()
        for i in range(0,   len(result), 2):
            if i + 1 < len(result):
                pairings.append(
                            (
                                result[i][0],
                                result[i][1],
                                result[i+1][0],
                                result[i+1][1]
                                )
                        )
            else:
                break
        return pairings
