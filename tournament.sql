-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;


CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY UNIQUE ,
    name text
);

CREATE TABLE IF NOT EXISTS matches (
    id SERIAL PRIMARY KEY UNIQUE ,
    player_one integer NOT NULL,
    player_two integer NOT NULL,
    winner integer NOT NULL,
    FOREIGN KEY (player_one) REFERENCES players(id),
    FOREIGN KEY (player_two) REFERENCES players(id),
    FOREIGN KEY (winner) REFERENCES players(id)
);


CREATE VIEW matches_so_far AS
    SELECT players.id,
    COUNT(matches.id) AS matches_played
    FROM players, matches
    WHERE ((players.id = matches.player_one) OR (players.id = matches.player_two))
    GROUP BY players.id
    ORDER BY count(matches.id) DESC;


CREATE VIEW wins_per_player AS
    SELECT players.id, players.name, COUNT(matches.winner) AS wins FROM players
    JOIN matches ON players.id = matches.winner
    GROUP BY players.id, players.name
    ORDER BY players.name;


CREATE VIEW standings AS 
    SELECT DISTINCT(players.id), players.name,
    CASE
        WHEN wins_per_player.wins IS NULL THEN 0
        ELSE wins_per_player.wins
    END AS Number_of_wins,
    CASE
        WHEN matches_so_far.matches_played IS NULL THEN 0
        ELSE matches_so_far.matches_played
    END AS matches_played
    FROM players
    LEFT JOIN matches_so_far ON players.id = matches_so_far.id
    LEFT JOIN wins_per_player ON players.id = wins_per_player.id
    ORDER BY Number_of_wins DESC;




