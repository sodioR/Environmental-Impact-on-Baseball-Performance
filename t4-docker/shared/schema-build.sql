-- Final Project: Schema Build
-- Date: 04/14/2026
-- Group 4: Erin Wright-Vazquez | Jacob Ko | Sadia Rahman

-- Schema

CREATE SCHEMA IF NOT EXISTS baseball;
SET search_path TO baseball;

-- Dimensional Tables

CREATE TABLE IF NOT EXISTS dim_city (
    location_id TEXT PRIMARY KEY,
    city TEXT,
    state TEXT
);

CREATE TABLE IF NOT EXISTS dim_ballpark (
    park_id TEXT PRIMARY KEY,
    park_name TEXT,
    latitude DECIMAL,
    longitude DECIMAL,
    location_id TEXT,
    FOREIGN KEY (location_id) REFERENCES dim_city(location_id)
);

CREATE TABLE IF NOT EXISTS dim_team (
    team_key VARCHAR(3) PRIMARY KEY,
    team_name TEXT
);

CREATE TABLE IF NOT EXISTS dim_pitcher (
    pitcher_id INT PRIMARY KEY,
    player_name TEXT
);

-- Core Tables

CREATE TABLE IF NOT EXISTS games (
    game_pk INT PRIMARY KEY,
    game_date DATE,
    home_team TEXT,
    away_team TEXT,
    park_id TEXT,
    FOREIGN KEY (park_id) REFERENCES dim_ballpark(park_id)
);

CREATE TABLE IF NOT EXISTS fact_weather (
    weather_id INT PRIMARY KEY,
    park_id TEXT,
    date DATE,
    temperature_2m_max DECIMAL,
    temperature_2m_min DECIMAL,
    precipitation_sum DECIMAL,
    windspeed_10m_max DECIMAL,
    relative_humidity_2m_mean DECIMAL,
    FOREIGN KEY (park_id) REFERENCES dim_ballpark(park_id)
);

CREATE TABLE IF NOT EXISTS fact_statcast_pitch (
    pitch_key TEXT PRIMARY KEY,
    game_pk INT,
    pitcher_id INT,
    events TEXT,
    description TEXT,
    release_speed DECIMAL,
    release_spin_rate DECIMAL,
    launch_speed DECIMAL,
    FOREIGN KEY (game_pk) REFERENCES games(game_pk),
    FOREIGN KEY (pitcher_id) REFERENCES dim_pitcher(pitcher_id)
);

-- Load CSV final tables

COPY dim_city
FROM '/home/team4/cleaned-tables/dim_city.csv'
DELIMITER ',' CSV HEADER;

COPY dim_ballpark
FROM '/home/team4/cleaned-tables/dim_ballpark.csv'
DELIMITER ',' CSV HEADER;

COPY dim_team
FROM '/home/team4/cleaned-tables/dim_teams.csv'
DELIMITER ',' CSV HEADER;

COPY dim_pitcher
FROM '/home/team4/cleaned-tables/dim_pitcher.csv'
DELIMITER ',' CSV HEADER;

COPY games
FROM '/home/team4/cleaned-tables/games.csv'
DELIMITER ',' CSV HEADER;

COPY fact_weather
FROM '/home/team4/cleaned-tables/fact_weather.csv'
DELIMITER ',' CSV HEADER;

COPY fact_statcast_pitch
FROM '/home/team4/cleaned-tables/fact_statcast_pitch.csv'
DELIMITER ',' CSV HEADER;