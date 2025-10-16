# NYC Yellow Cab Trip Data Dashboard
This is data dashboard for trips by the yellow cabs of New York City in 2016. It is aimed at showcasing statistical insight obtained from the data. The data is first processed and cleaned of anomalies and duplicates. The discarded trips are logged in excluded_data.csv as well as relevant data as to why is was excluded by the data pipline.

The pipeline excludes trip entries that have the following anomalies:
1. Duplicate IDs
2. Unrealistic Speeds
3. Coordinates that are clearly outside of NYC
4. Trips whose distances could not be calculate or resulted in 0.

The platform's architecture consists of a backend written in fastapi exposing the following endpoints:

1. "/trips/"
 This endpoint takes to query parameters limit and offset in order to support pagination. Limit determines how many entries are return per page and offset controls the starting point / cursor of each request. By carefully controlling these perameters, we are able to fetch data effeciently.

2. "/trip/{trip_id}"
 This endpoint returns all trip details given an ID. It envokes a search algorithm that runs through the dataset to return the entry with the specified ID

3. "/stats"
 This endpoint returns key statistical data points about the dataset as whole.

The frontend is build with the Vue.js framework and uses Chart.js library to plot data with graphs. It also uses the axios library to send API calls to our backend.

The backend uses sqlite as our main database, chosen for it's simplicity and effeciency.

## Prerequisites
 . Python 3.9+
 . Node js

## Setup
1. Clone the repo
 git clone https://github.com
 cd project
 cd api

2. Create a virtual environment, activate it, and install dependencies
 python -m venv .venv
 .venv\Scripts\Activate.ps1
 pip install -r requirements.txt

3. Run the data pipeline. This will clean the data and create the database (command must be run as is)
 cd data
 python parse_and_store.py raw_data.csv data.db excluded_data.csv

## Usage
1. Start the backend
 cd api
 python app.py

2. Start the frontend
 cd web
 npm run dev

## Additional Documentation & Technical Report
1. Video of project walkthrough
 https://

2. Algorithm documentation and evaluation
 https://