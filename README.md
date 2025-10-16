# NYC Yellow Cab Trip Data Dashboard 🚕

This is a data dashboard for trips by yellow cabs in New York City in 2016. It aims to showcase statistical insights obtained from the data. The data is first processed and cleaned of anomalies and duplicates. The discarded trips are logged in `excluded_data.csv`, along with relevant data as to why they were excluded by the data pipeline.

## Data Pipeline Exclusions

The pipeline excludes trip entries that have the following anomalies:

1.  **Duplicate IDs**
2.  **Unrealistic Speeds**
3.  **Coordinates** that are clearly outside of NYC
4.  **Trips** whose distances could not be calculated or resulted in 0.

## Platform Architecture 🏗️

The platform's architecture consists of a backend written in **FastAPI** exposing the following endpoints:

1.  **`/trips/`**
    This endpoint takes `limit` and `offset` as query parameters to support pagination. `Limit` determines how many entries are returned per page, and `offset` controls the starting point/cursor of each request. By carefully controlling these parameters, data can be fetched efficiently.

2.  **`/trip/{trip_id}`**
    This endpoint returns all trip details given an ID. It invokes a search algorithm that runs through the dataset to return the entry with the specified ID.

3.  **`/stats`**
    This endpoint returns key statistical data points about the dataset as a whole.

The frontend is built with the **Vue.js** framework and uses the **Chart.js** library to plot data with graphs. It also uses the **Axios** library to send API calls to the backend.

The backend uses **SQLite** as the main database, chosen for its simplicity and efficiency.

-----

## Prerequisites

  * Python 3.9+
  * Node.js

-----

## Setup ⚙️

1.  **Clone the repo:**

    ```bash
    git clone https://github.com/Ptuyizere/nyc_cab_dashboard.git
    cd nyc_cab_dashboard
    cd api
    ```

2.  **Create a virtual environment, activate it, and install dependencies:**

    ```bash
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

3.  **Run the data pipeline:** This will clean the data and create the database (ensure that the database is named `data.db`).

    ```bash
    cd data
    python parse_and_store.py raw_data.csv data.db excluded_data.csv
    ```

-----

## Usage ▶️

1.  **Start the backend:**

    ```bash
    cd api
    python app.py
    ```

2.  **Start the frontend:**

    ```bash
    cd web
    npm run dev
    ```

-----

## Additional Documentation & Technical Report 📄

1.  **Video of project walkthrough:**
    [https://youtu.be/GDjMFB0E26c](https://youtu.be/GDjMFB0E26c)

2.  **Algorithm documentation and evaluation:**
    [https://www.dropbox.com/scl/fi/bbw7jm33unzsnvbc12v6b/Project-Technical-Report-Patrick-Tuyizere.pdf?rlkey=tu9nemizm8srx6d8w81d91pj2\&st=w6yxjxeu\&dl=0](https://www.dropbox.com/scl/fi/bbw7jm33unzsnvbc12v6b/Project-Technical-Report-Patrick-Tuyizere.pdf?rlkey=tu9nemizm8srx6d8w81d91pj2&st=w6yxjxeu&dl=0)