#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

numberOfPlayers = 0

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    query = "delete from matches"
    c.execute(query)
    c.execute("update players set matches = 0")
    c.execute("update players set wins = 0")
    conn.commit()
    #c.commit()
    c.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    query = "delete from players"
    c.execute(query)
    conn.commit()
    #c.commit()
    c.close()
    global numberOfPlayers
    numberOfPlayers = 0


def countPlayers():
    """Returns the number of players currently registered."""
    global numberOfPlayers;
    return numberOfPlayers



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("insert into players (name, wins, matches) values(%s, 0, 0)", (name,))
    #query = "insert into players  (wins, matches) values ( 0 , 0)"
    #c.execute(query)
    conn.commit()
    global numberOfPlayers;
    numberOfPlayers += 1
    """
    Printing out the inserted names
    
    print "current table"

    newquery = "select * from players"
    c.execute(newquery)
    table = c.fetchall()
    print table
    print "\n"
    """


    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    query = "select * from players order by wins desc"
    c.execute(query)
    conn.commit()
    standing = c.fetchall()
    conn.close()
    return standing


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    query = "insert into matches(winner, loser) values(%s, %s)" % (winner, loser)
    c.execute(query)
    c.execute("update players set matches = 1 where id = %s or id = %s" % (winner, loser))
    c.execute("update players set wins = 1 where id = %s" % winner)
    conn.commit()
    conn.close()
 
 
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
    listOfPairs = []
    conn = connect()
    c = conn.cursor()

    try:
        query = "drop table copy"
        c.execute(query)
        query = "create table copy as select * from players"
    except:
        query = "create table copy as select * from players"
    c.execute(query)
    c.execute("select * from copy")
    players = c.fetchall()
    print "These are the players"
    print players
    while(len(players) != 0):
        #Initialize player one to the first tuple
        player1 = players[0]
        for player2 in players[1:]:
            #Empty tuple to initialize later on when we find a pair
            tupl = ()
            if(player1[2] == player2[2]):
                id1 = (player1[0])
                name1 = (player1[1])
                id2 = (player2[0])
                name2 = (player2[1])
                tupl = (id1, name1, id2, name2)
                listOfPairs.append(tupl)
                #Update the tuple by removing the added players in the list
                c.execute("delete from copy where id = %d or id = %d" % (id1, id2))
                conn.commit()
                c.execute("select * from copy")
                players = c.fetchall()
                break
        print listOfPairs
    conn.close()
    return listOfPairs


