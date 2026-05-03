# Main Question

***How does environmental context explain performance variability beyond player skill metrics?***
**Authors:** Jacob Ko, Sadia Rahman, Erin Wright-Vazquez

## General Project Concept

The purpose of this project is to construct a dataset that integrates pitcher performance statistics with stadium location, altitude, and game day weather conditions. By aligning performance metrics with <br>
environmental context, the goal is to evaluate whether altitude and weather variables have a measurable influence on pitching outcomes. Although pitcher success is typically assessed using skill-based metrics, <br>
this study expands that framework by incorporating external environmental factors. Altitude affects air density, which can influence pitch movement and ball trajectory, while weather conditions such as <br>
temperature, humidity, and wind may alter ball flight after contact. These factors may also impact pitcher behavior and physical performance, potentially affecting movement, visibility, and overall effectiveness. <br>
Other questions that would hopefully be also answered through this project: 
- How does altitude affect pitching performance, pitch characteristics, and opposing offensive outcomes, and do home pitchers adapt differently than visiting pitchers?
- How do weather conditions such as temperature, humidity, wind, and precipitation influence pitch velocity, movement, strikeouts, earned runs, and home run rates?
- Do environmental factors interact, such that extreme weather amplifies the effects of altitude on pitching performance?
- Are certain pitchers more sensitive to environmental conditions than others? <br>

Together, these questions frame an analysis designed to determine whether environmental context meaningfully contributes to variation in pitching performance.

## Datasets Overview

**[Sample Datasets](<https://github.com/ewrightvazquez/Data-Engineering-Principles-and-Practices-Final-Project/tree/main/data-sources/sample-data>) : 10 row samples of each of the datasets below.**

| **Dataset** | **Link(s)** | **Descriptions** |
| :--- | :--- | :---: |
| Pybaseball statcast API | pybaseball GitHub Repo: <https://github.com/schorrm/pybaseball> <br> pybaseball 2.0.0 installation guide in python: <https://pypi.org/project/pybaseball/2.0.0/> <br> | Pybaseball serves as the primary performance dataset. It pulls pitch level and game level data from Baseball Savant, Baseball Reference, and FanGraphs. Key variables include pitch velocity, spin rate, pitch type, strikeouts, walks, earned runs, innings pitched, launch angle, and exit velocity. Because the data are timestamped and game specific, they can be aligned with stadium and environmental variables. This supports both pitch level analysis and game level performance evaluation. |
| Seamheads Park | Seamhead Park Dataset: <https://www.seamheads.com/ballparks/> | The Seamheads Ballparks database provides structured information on MLB stadiums, including park name, city, state, years active, latitude, longitude, and altitude. Altitude and geolocation are central to this project, as they allow us to measure elevation differences across stadiums and link performance data to environmental context. The coordinate data also enables integration with weather datasets. |
| Openmeteo weather API | OpenMeteo API: <https://open-meteo.com/> <br> openmeto api installation and overview: <https://pypi.org/project/openmeteo-requests/#description> | The Open-Meteo API provides weather variables such as temperature, humidity, wind speed, wind direction, and precipitation. Weather data will be retrieved using stadium latitude and longitude for specific game dates. Integrating these variables allows us to assess how environmental conditions relate to pitching performance, including potential interactions between weather and elevation. |
| MLB Ballpark (Kaggle) | Kaggle dataset: <https://www.kaggle.com/datasets/paulrjohnson/mlb-ballparks?resource=download_> | The Kaggle MLB Ballparks dataset provides team names associated with each stadium. While Seamheads supplies geographic and structural details, Kaggle connects parks to team identity. Joining the datasets on ballpark name creates a unified table containing team name, park status |

## Cleaning and Transformation
Data cleaning and transformation were performed across both static datasets (Seamheads and MLB/Kaggle) and ingested dynamic datasets to ensure consistency prior to integration. This process included standardizing column names, normalizing park and team naming conventions, and creating shared keys to resolve discrepancies across sources. Team abbreviations were aligned, and relationships such as team to ballpark mappings and park date combinations were
established to support accurate joins. Duplicate and inconsistent records were removed, and key identifiers (including pitch, game, and weather records) were validated for uniqueness. Following cleaning, the data was structured into a relational format consisting of fact and dimension tables. Pitch level, game level, and weather data were organized into fact tables, while descriptive attributes for pitchers, teams, ballparks, and locations were maintained in dimension tables. Additional transformations, such as deriving pitcher team from inning context and enriching game data with weather information, ensured completeness and consistency across datasets. The final transformed tables were validated for referential integrity and prepared for downstream analysis.

## Entity Relationship Diagram
### Final ERD (Our normalization process is explained in the ["ERD and Normalization Process" document](https://github.com/ewrightvazquez/Data-Engineering-Principles-and-Practices-Final-Project/blob/main/ERD%20and%20Normalization.pdf))

<img width="2121" height="859" alt="DE_ Final Project (ERD) - Color" src="https://github.com/user-attachments/assets/329fa49b-a309-49c1-b839-1a96f5d25573" />

## Database and Schema
The database and schema were implemented in SQL by creating separate tables for each entity defined in the ERD, including games, pitchers, teams, ballparks, cities, pitch level data, and weather. Each table was defined with primary keys, and relationships were enforced through foreign keys to connect related data (such as linking pitch data to games and pitchers, and games to teams and ballparks). Dimension tables store descriptive attributes like team and ballpark information, while fact tables store measurable data such as pitch performance and weather observations. Data types were standardized across tables to ensure accurate joins, resulting in a normalized schema that minimizes redundancy and supports efficient querying

## Docker Container/Running Full Pipeline
Our docker-compose.yml file starts three services: a Postgres container to host our SQL database, an Airflow service for our database automation, and an API service that hosts our API application. All of these work together to produce our end-to-end application. To review the steps to start the service please review the ["Docker/Running Full Pipeline"](https://github.com/ewrightvazquez/Data-Engineering-Principles-and-Practices-Final-Project/blob/main/Project%20Overview.pdf) section in our final docummentation file, on page 3.

## API Implementation and Automation
Our Airflow DAG is configured to execute the pipeline on a daily schedule. It runs a more comprehensive version of the pipeline that ingests a larger volume of data from Openmeteo and pybaseball consolidated for June 2023 - August 2023, with an average runtime of approximately 13–17 minutes. The DAG definition is defined in the `dag_run_pipeline.py` file. The version run above is a streamlined implementation that executes faster over a smaller dataset. We chose to do this to demonstrate our pipeline capability in a more efficient manner while still showing its effectiveness. In practice, the full pipeline would run during off-peak hours to refresh the database with the most up-to-date data, enabling users to query it later through the API and thereby minimizing the impact of processing latency. Should the airflow not start on its own, follow the instructions laid out under the ["API Implementation and Automation"](https://github.com/ewrightvazquez/Data-Engineering-Principles-and-Practices-Final-Project/blob/main/Project%20Overview.pdf) section in our final docummentation file, on page 4.

