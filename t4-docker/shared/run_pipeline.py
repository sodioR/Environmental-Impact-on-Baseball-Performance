

import subprocess
import psycopg2
import time
import json
import requests

def wait_for_db():

    while True:
        try:
            conn = psycopg2.connect(host = "postgres",
                                    database = "t4db",
                                    user = "t4",
                                    password = "secret",
                                    port = 5432
                                    )
            conn.close()
            break

        except:
            print("Waiting for database...")
            time.sleep(2)

def run_ingestion():

    print("Running data ingestion...")

    subprocess.run(["python3",
                    "/home/t4/data-ingestion.py"
                    ], check = True)


def run_notebook():

    print("Running transformation notebook...")

    subprocess.run(["jupyter",
                    "nbconvert",
                    "--to", "notebook",
                    "--execute",
                    "--ExecutePreprocessor.kernel_name=python3",
                    "/home/t4/data-transformation.ipynb",
                    "--output", "/home/t4/data-transformation.ipynb"
                    ], check = True)


def run_sql():

    print("Running SQL schema...")

    subprocess.run(["psql",
                    "-h", "postgres",
                    "-U", "t4",
                    "-d", "t4db",
                    "-f", "/home/t4/schema-build.sql"
                    ], check = True)


if __name__ == "__main__":

    # Running pipeline 
    print("Starting pipeline...")
    run_ingestion() # data-ingestion
    run_notebook() # transformation
    wait_for_db() # DB ready
    run_sql() # build schema
    print("Pipeline complete.")

    print("Calling API server...")
    url = 'http://fastapi:8000/teams'
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    print(response.status_code)
    print(json.loads(response.content))