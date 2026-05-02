from fastapi import FastAPI, HTTPException, status
from typing import Literal
import pandas as pd
import psycopg2
from io import StringIO

# Create FastAPI app
app = FastAPI()

# Get all teams in database
@app.get(
    "/teams",
    description="Endpoint to get all teams in the database. Returns the team code to use to query other endpoints with."
)
def get_teams():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            dbname="t4db",
            user="t4",
            password="secret",
            host="postgres",
            port=5432
        )
        cur = conn.cursor()

        cur.execute("""
            SELECT team_name
            FROM baseball.dim_team;
        """)

        rows = cur.fetchall()

        # Convert rows to a list of dictionaries for better readability
        rows = [
            {
                "team_name": row[0],
            }
            for row in rows
        ]

        return rows

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {str(e)}"
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Get all pitchers in database
@app.get(
    "/pitchers",
    description="Endpoint to get all pitchers in the database. Returns pitcher names used to query other endpoints with."
)
def get_pitchers():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            dbname="t4db",
            user="t4",
            password="secret",
            host="postgres",
            port=5432
        )
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM baseball.dim_pitcher;
        """)

        rows = cur.fetchall()

        # Convert rows to a list of dictionaries for better readability
        rows = [
            {
                "player_id": row[0],
                "pitcher_name": row[1],
            }
            for row in rows
        ]

        return rows

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {str(e)}"
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Get all ballparks in database
@app.get(
    "/ballparks",
    description="Endpoint to get all ballparks in the database. Returns ballpark names used to query other endpoints with."
)
def get_ballparks():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            dbname="t4db",
            user="t4",
            password="secret",
            host="postgres",
            port=5432
        )
        cur = conn.cursor()

        cur.execute("""
            SELECT park_name
            FROM baseball.dim_ballpark;
        """)

        rows = cur.fetchall()

        # Convert rows to a list of dictionaries for better readability
        rows = [
            {
                "park_name": row[0],
            }
            for row in rows
        ]
        
        return rows

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {str(e)}"
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Get the id of a player to retrieve their stats
@app.get(
    "/pitcher_stats/{player_name}/{n}/",
    description="""Endpoint to get player relevent stats. Retrieves the first `n` rows. Currently gets all pitcher related stats as well
    as well as the games they played in.
    """
)
def get_pitcher(player_name: str, n: int):
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            dbname="t4db",
            user="t4",
            password="secret",
            host="postgres",
            port=5432
        )
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM baseball.dim_pitcher pitcher LEFT JOIN baseball.fact_statcast_pitch stats ON
            pitcher.pitcher_id = stats.pitcher_id
            LEFT JOIN baseball.games games ON stats.game_pk = games.game_pk
            LEFT JOIN baseball.dim_ballpark ballparks ON ballparks.park_id = games.park_id
            WHERE player_name = %s
            LIMIT %s;
        """, (player_name,n,))

        rows = cur.fetchall()

        # Convert rows to a list of dictionaries for better readability
        rows = [
            {
                "player_id": row[0],
                "pitcher_name": row[1],
                "pitch_key": row[2],
                "game_pk": row[3],
                "pitcher": row[4],
                "pitch_type": row[5],
                "events": row[6],
                "description": row[7],
                "release_speed": row[8],
                "release_spin_rate": row[9],
                "launch_angle": row[10],
                "game_date": row[12],
                "home_team": row[13],
                "away_team": row[14],
                "park_id": row[15],
                "park_name": row[17],
                "longitude": row[18],
                "latitude": row[19],
                "location_id": row[20]
            }
            for row in rows
        ]

        return rows

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {str(e)}"
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Get average weather data for a particular ballpark
@app.get(
    "/weather/ballpark/",
    description="""Endpoint that returns the average weather conditions for each ballpark. This can
    be used to see if certain ballparks have more severe weather conditions on average than others.
    Then, further analysis can be done to see if there is a correlation between weather conditions and
    pitching performance.
    """
)
def get_weather_ballpark_avg():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            dbname="t4db",
            user="t4",
            password="secret",
            host="postgres",
            port=5432
        )
        cur = conn.cursor()

        cur.execute("""
            SELECT park_name,
                AVG(temperature_2m_max) AS avg_temp_max,
                AVG(temperature_2m_min) AS avg_temp_min,
                AVG(precipitation_sum) AS avg_precipitation,
                AVG(windspeed_10m_max) AS avg_wind_speed,
                AVG(relative_humidity_2m_mean) AS avg_humidity
            FROM baseball.dim_ballpark ballparks
            FULL JOIN baseball.dim_city city ON ballparks.location_id = city.location_id
            FULL JOIN baseball.fact_weather weather ON weather.park_id = ballparks.park_id
            GROUP BY park_name;
        """)

        rows = cur.fetchall()

        # Convert rows to a list of dictionaries for better readability
        rows = [
            {
                "park_name": row[0],
                "avg_temp_max": row[1],
                "avg_temp_min": row[2],
                "avg_precipitation": row[3],
                "avg_wind_speed": row[4],
                "avg_humidity": row[5]
            }
            for row in rows
        ]

        return rows

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {str(e)}"
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Get average weather conditions for based on pitching performance. For example, get the average weather conditions for games where the release speed was above a certain threshold. This can be used to see if there are certain weather conditions which are associated with good pitching performance.
@app.get(
    "/weather/pitching_performance/{release_speed_threshold}/",
    description="""Get average weather conditions for based on pitching performance. For example, get the average weather
    conditions for games where the release speed was above a certain threshold. Since pitch speed if often associated with
    good pitching, this can be used to see if weather conditions differ based on how fast pitchers are able to throw. An
    assumption may be that if the weather is worse, then pitchers may not be able to throw as fast.
    """
)
def get_weather_pitching_performance(release_speed_threshold: float):
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            dbname="t4db",
            user="t4",
            password="secret",
            host="postgres",
            port=5432
        )
        cur = conn.cursor()

        cur.execute("""
            SELECT AVG(temperature_2m_max), AVG(temperature_2m_min), AVG(precipitation_sum), AVG(windspeed_10m_max), AVG(relative_humidity_2m_mean)
            FROM baseball.dim_ballpark ballparks
            LEFT JOIN baseball.dim_city city ON ballparks.location_id = city.location_id
            LEFT JOIN baseball.fact_weather weather ON weather.park_id = ballparks.park_id
            LEFT JOIN baseball.games games ON games.park_id = ballparks.park_id
            LEFT JOIN baseball.fact_statcast_pitch pitcher ON pitcher.game_pk = games.game_pk
            WHERE release_speed > %s;
        """, (release_speed_threshold,))

        rows = cur.fetchall()

        # Convert rows to a list of dictionaries for better readability
        rows = [
            {
                "avg_temperature_2m_max": row[0],
                "avg_temperature_2m_min": row[1],
                "avg_precipitation_sum": row[2],
                "avg_windspeed_10m_max": row[3],
                "avg_relative_humidity_2m_mean": row[4]
            }
            for row in rows
        ]

        return rows

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {str(e)}"
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Get weather and location data for a particular date
@app.get(
    "/weather/{ballpark_name}/{date}/",
    description="""Endpoint to get weather data for a ballpark on a particular date. Can be used to get the weather
    for a particular game. This can be used to see if a bad pitching performance can be associated to
    particular weather conditions. Dates should be formatted as YYYY-MM-DD. For example, 2023-04-05.
    """
)
def get_weather_ballpark_date(ballpark_name: str, date: str):
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            dbname="t4db",
            user="t4",
            password="secret",
            host="postgres",
            port=5432
        )
        cur = conn.cursor()

        cur.execute("""
            SELECT park_name, city, state, temperature_2m_max, temperature_2m_min, precipitation_sum, windspeed_10m_max, relative_humidity_2m_mean
            FROM baseball.dim_ballpark ballparks
            LEFT JOIN baseball.dim_city city ON ballparks.location_id = city.location_id
            LEFT JOIN baseball.fact_weather weather ON weather.park_id= ballparks.park_id
            WHERE park_name = %s AND date = %s;
        """, (ballpark_name, date,))

        rows = cur.fetchall()

        # Convert rows to a list of dictionaries for better readability
        rows = [
            {
                "park_name": row[0],
                "city": row[1],
                "state": row[2],
                "temperature_2m_max": row[3],
                "temperature_2m_min": row[4],
                "precipitation_sum": row[5],
                "windspeed_10m_max": row[6],
                "relative_humidity_2m_mean": row[7]
            }
            for row in rows
        ]

        return rows

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {str(e)}"
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Get average pitching stats for a particular team.
@app.get(
    "/team_stats/{team_name}/",
    description="""Get average pitching stats for a particular team. This aggregates numeric pitching stats
    for all games which the chosen team was the home team. This can be used to see if a certain ballpark has
    an effect on pitching performance. Then, this can be compared with weather data to see if weather conditions
    have an effect on pitching performance giving teams a home ballpark advantage. Team names are formatted using
    the three letter abbreviations. For example, the Baltimore Orioles are represented as BAL. These can be found
    online.
    """
)
def get_team_stats(team_name: str):
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            dbname="t4db",
            user="t4",
            password="secret",
            host="postgres",
            port=5432
        )
        cur = conn.cursor()

        cur.execute("""
            SELECT home_team, AVG(release_speed), AVG(release_spin_rate), AVG(launch_speed)
            FROM baseball.fact_statcast_pitch pitcher
            LEFT JOIN baseball.games games ON games.game_pk = pitcher.game_pk
            LEFT JOIN baseball.dim_team teams ON teams.team_name = games.home_team
            WHERE team_name = %s
            GROUP BY home_team;
        """, (team_name,))

        rows = cur.fetchall()

        # Convert rows to a list of dictionaries for better readability
        rows = [
            {
                "home_team": row[0],
                "avg_release_speed": row[1],
                "avg_release_spin_rate": row[2],
                "avg_launch_speed": row[3]
            }
            for row in rows
        ]

        return rows

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {str(e)}"
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Get the N top pitchers by release speed.
@app.get(
    "/pitchers_ranked/{n}/{direction}/",
    description="""Get the N best or worst pitchers by release speed. This can be used to see if there are certain weather conditions
    which are associated with good pitching performance. For example, if the top pitchers all pitch in ballparks with typically
    good weather conditions, then it may imply that weather conditions are associated with pitching performance. To find the best
    pitchers, set direction to best, 
    """
)
def get_top_pitchers(n: int, direction: Literal["best", "worst"] = "best"):
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            dbname="t4db",
            user="t4",
            password="secret",
            host="postgres",
            port=5432
        )
        cur = conn.cursor()

        dir = "DESC" if direction == "best" else "ASC"

        cur.execute(f"""
            SELECT player_name, AVG(release_speed), AVG(release_spin_rate), AVG(launch_speed)
            FROM baseball.dim_pitcher pitcher LEFT JOIN baseball.fact_statcast_pitch stats ON
            pitcher.pitcher_id = stats.pitcher_id
            LEFT JOIN baseball.games games ON games.game_pk = stats.game_pk
            GROUP BY player_name
            ORDER BY AVG(release_speed) {dir}
            LIMIT %s;
        """, (n,))

        rows = cur.fetchall()

        # Convert rows to a list of dictionaries for better readability
        rows = [
            {
                "player_name": row[0],
                "avg_release_speed": row[1],
                "avg_release_spin_rate": row[2],
                "avg_launch_speed": row[3]
            }
            for row in rows
        ]

        return rows

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {str(e)}"
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Get the N cities with the highest average precipitation during games. This can be used to see if certain cities have more severe weather conditions which can affect pitching performance.
@app.get(
    "/top_cities_precipitation/{n}/",
    description="""Get the N cities with the highest average precipitation during games. This can be used to compare weather
    conditions across different cities and see if certain cities have more severe weather conditions which can affect pitching performance.
    """
)
def get_top_cities_precipitation(n: int):
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            dbname="t4db",
            user="t4",
            password="secret",
            host="postgres",
            port=5432
        )
        cur = conn.cursor()

        cur.execute("""
            SELECT city, state, AVG(precipitation_sum) AS avg_precipitation
            FROM baseball.dim_ballpark ballparks
            LEFT JOIN baseball.dim_city city ON ballparks.location_id = city.location_id
            LEFT JOIN baseball.fact_weather weather ON weather.park_id = ballparks.park_id
            GROUP BY city, state
            ORDER BY avg_precipitation DESC
            LIMIT %s;
        """, (n,))

        rows = cur.fetchall()

        # Convert rows to a list of dictionaries for better readability
        rows = [
            {
                "city": row[0],
                "state": row[1],
                "avg_precipitation": row[2]
            }
            for row in rows
        ]

        return rows

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {str(e)}"
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
