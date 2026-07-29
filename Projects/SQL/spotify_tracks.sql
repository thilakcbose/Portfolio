create database spotify_db;

use spotify_db;

CREATE TABLE IF NOT EXISTS spotify_tracks(
	id INT AUTO_INCREMENT PRIMARY KEY,
	track_name VARCHAR(255),
    artist VARCHAR(255),
    album VARCHAR(255),
    track_number INT,
    duration_minutes FLOAT
    );
    
show tables;

describe spotify_tracks;

select * from spotify_tracks;

DROP TABLE spotify_data;

CREATE TABLE IF NOT EXISTS spotify_data(
	id INT AUTO_INCREMENT PRIMARY KEY,
    spotify_id VARCHAR(225), 
	track_name VARCHAR(255),
    artist VARCHAR(255),
    album VARCHAR(255),
    track_number INT,
    type VARCHAR(225),
    duration_minutes FLOAT
    );
    
describe spotify_data;

select * from spotify_data;

select track_name from spotify_data
where duration_minutes > 4;


    
