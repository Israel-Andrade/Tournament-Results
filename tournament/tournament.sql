-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

\c tournament;
drop table matches;
drop table players;
drop table copy;



create table players(
		id serial,
		name text,
		wins integer,
		matches integer);

create table matches(
		id serial,
		winner text,
		loser text);

create table copy as select * from players;

