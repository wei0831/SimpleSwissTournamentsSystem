-- Author: Jack Chang
-- Date: 10/30/2015
-- PostgresSQL Table definitions for the swiss tournament system.

-- Discount any exisiting connections to the databse
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'tournament'
  AND pid <> pg_backend_pid();

-- Recreate database if exists
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

-- Connect to the newly created database
\c tournament

CREATE TABLE players (
  id            SERIAL      PRIMARY KEY,
  name          varchar(40) NOT NULL,
  date_created  timestamptz DEFAULT current_timestamp,
  date_updated  timestamptz DEFAULT current_timestamp
);

CREATE TABLE matches (
  id            SERIAL      PRIMARY KEY,
  winner        INT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  loser         INT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  date_created  timestamptz DEFAULT current_timestamp,
  date_updated  timestamptz DEFAULT current_timestamp,
  CONSTRAINT no_self_matches CHECK (winner != loser)
);

-- | PlayersCount |
CREATE VIEW playersCount AS
  SELECT COUNT(players.id) AS PlayersCount FROM players;

-- | PlayerID | PlayerName | WinCount | LoseCount | MatchCount |
CREATE VIEW playersStandings AS
  SELECT players.id AS id,
         players.name AS name,
         COUNT(CASE WHEN matches.winner = players.id THEN TRUE END) AS wins,
         COUNT(CASE WHEN matches.loser = players.id THEN TRUE END) AS loses,
         COUNT(matches.id) AS matches
  FROM players LEFT JOIN matches
  ON players.id = matches.winner OR players.id = matches.loser
  GROUP BY players.id
  ORDER BY wins DESC;
