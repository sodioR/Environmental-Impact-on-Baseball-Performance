# Docker Setup Instructions:

These assume that you have this repository cloned. At a minimum you will need to copy the `t4-docker` folder. All commands should be run within this directory.

1. Verify that the `api` folder contains both a `pyproject.toml` and `uv.lock`. If `pyproject.toml` is missing, try recopying the file. If `uv.lock` is missing, run `uv sync` within the `api` folder.

2. Run `docker compose up --build` inside the `t4-docker` folder. You should see containers start to build. Once they are built, they should start automatically. You can also verify that the container built using the Docker Desktop GUI under `t4-docker`.
    - If you get an error saying "failed to connect to the docker API", make sure that Docker Desktop is running.

3. If no errors are produced, you can skip this step. If the above doesn't work, try building the containers first using `docker compose build --no-cache`. Once the containers build, you can run it with `docker compose up`.

4. To stop the containers, you can use the Docker Desktop GUI. Optionally, you can also `Ctrl + c` in your terminal to stop the containers.

5. Optionally, run `docker compose down` to stop and remove this container once you are done.

# Viewing API

After following the above steps, API service should be up and running. To verify this, run `docker ps`. A container named `t4-docker-fastapi` should be running. As a note, this project relies on Python 3.11 but UV should handle this for you!

From here, go to your browser (Chrome, Firefox, etc.) and navigate to `localhost:8000/docs`. This will show automated documentation of our API server. To try out an endpoint, click on the arrow and `Try it out`!

IMPORTANT: Make sure you don't have anything else running at localhost:8000. In other words, if you are running the `jhu_docker` at the same time, this will cause an error.

# Creating PostgreSQL Connection in PGAdmin

Assumes that `t4-docker-postgres` is running and that PGAdmin is installed on your local machine. Can verify this again with `docker ps`.

1. Open PGAdmin. Right click on `Server` and choose to `Register` a server.

2. Use `t4db` for the name, then click the `Connections` tab.

3. Fill in the following credentials:

```
Hostname: localhost
Port: 5432
Username: t4
Password: secret
```

and click `Save`.

4. If the connection fails to start, make sure that the docker service is running with `docker ps` or the Docker Desktop GUI.
