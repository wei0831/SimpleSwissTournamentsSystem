# Authoer: Jack Chang
# Date: 10/30/2015
# tournament.py -- implementation of a Swiss-system tournament
# Interact with Postgres DB for the tournament results

import psycopg2


def connect(database_name="tournament"):
    """
    Connect to the PostgreSQL database.
    Returns a database connection and cursor
    """
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")

def deleteMatches():
    """
    Remove all the match records from the database.
    Database is being modified.
    """
    db, cursor = connect();

    query = "DELETE FROM matches"
    cursor.execute(query)

    # Commit the changes
    db.commit()
    db.close()

def deletePlayers():
    """
    Remove all the player records from the database.
    Database is being modified.
    """
    db, cursor = connect()

    query = "DELETE FROM players"
    cursor.execute(query)

    # Commit the changes
    db.commit()
    db.close()

def countPlayers():
    """
    Returns the number of players currently registered.
    """
    db, cursor = connect()

    query = "SELECT * FROM playersCount"
    cursor.execute(query)

    # The playerscount is gurantee to be one row result
    result = cursor.fetchone()

    db.close()

    return result[0]


def registerPlayer(name):
    """
    Adds a player to the tournament database with given name.

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()

    query = "INSERT INTO players(name) VALUES(%s)"
    parameter = (name, )
    cursor.execute(query, parameter)

    db.commit()
    db.close()

def playerStandings():
    """
    Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cursor = connect();

    query = "SELECT id, name, wins, matches FROM playersStandings"
    cursor.execute(query)

    result = cursor.fetchall()
    db.close()

    return result

def reportMatch(winner, loser):
    """
    Records the outcome of a single match between two players.
    The database is being modified.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect();

    query = "INSERT INTO matches(winner, loser) VALUES(%s, %s)"
    parameter = (winner, loser)

    cursor.execute(query, parameter)
    # Commit the changes
    db.commit()
    db.close()

def swissPairings():
    """
    Returns a list of pairs of players for the next round of a match.

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
    # Getting Result From DB
    db, cursor = connect();

    query = "SELECT id, name FROM playersStandings"
    cursor.execute(query)

    result = cursor.fetchall()
    db.close()

    # Create pairing from result
    pairings = []
    playersCount = len(result)

    # Make sure there are an even number of players registered
    if playersCount % 2 != 0:
        raise ValueError("We do not have even number of players registered.")
    # We pair each 2 players together
    # Result is ordered by the wins,
    # hence we are gurantee to pair nearly-equal win/loss players together
    for i in range(0, playersCount, 2):
        pairings.append((result[i][0], result[i][1], result[i+1][0], result[i+1][1]))

    return pairings
