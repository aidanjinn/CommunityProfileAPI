# Community Profile Generation Tool

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-orange)
![Redis](https://img.shields.io/badge/Redis-6.0%2B-red)
![Celery](https://img.shields.io/badge/Celery-5.0%2B-green)

The Community Profile Creation API is a Flask-based application that scrapes demographic data from Wikipedia and energy profile data from the U.S. Energy Information Administration (EIA) to create a comprehensive community profile for a given location. The API leverages Gemini to generate a formatted profile and saves it as a local text file. It also uses **Redis** as a message broker and **Celery** for asynchronous task processing.

## Features

- **Wikipedia Data Scraping**: Retrieves demographic data for a specified community from Wikipedia.
- **EIA Data Integration**: Fetches energy profile data for the state associated with the community.
- **Community Profile Generation**: Combines demographic and energy data to create a detailed community profile.
- **Local File Storage**: Saves the generated profile as a formatted text file locally.
- **Redis & Celery Integration**: Enables asynchronous task processing and status tracking for long-running tasks.

## Running the Application

To start the Redis instance and Celery worker, run the `start_services.sh` script:

```bash
./start_services.sh
```

For running the flask application

```bash
python app.py
```
or use gunicorn
```bash
gunicorn app:app
```

## API Endpoints

### 1. Retrieve Wikipedia Demographic Data
- **Endpoint**: `/wiki`
- **Method**: `GET`
- **Query Parameter**:
  - `area`: The name of the area (e.g., `New_York_City,New_York`).
- **Response**: Returns JSON containing demographic data for the specified area.

### 2. Retrieve EIA Energy Profile Data
- **Endpoint**: `/eia`
- **Method**: `GET`
- **Query Parameter**:
  - `state_code`: The state code (e.g., `NY` for New York).
- **Response**: Returns JSON containing energy profile data for the specified state.

### 3. Generate Complete Community Profile
- **Endpoint**: `/profile`
- **Method**: `GET`
- **Query Parameter**:
  - `location`: The location in the format `city,state` (e.g., `New_York_City,New_York`).
- **Response**: Returns JSON with redis task_id. Also saves the profile as a formatted text file locally.

### 4. Celery Worker Task Status
- **Endpoint** `/status`
- **Method**: `GET`
- **Query Parameter**:
  - `<taskid>`: which is given in profile generation call
- **Response**: Current status of the task and if done the returned data

## Example Usage

### Retrieve Wikipedia Data
```bash
curl -X GET "http://localhost:5000/wiki?area=New_York_City,New_York"
```
### Retrieve EIA Data
```bash
curl -X GET "http://localhost:5000/eia?state_code=NY"
```
### Retrieve Profile Data
```bash
curl -X GET "http://localhost:5000/profile?location=New_York_City,New_York"
```

## Check Worker Status
```bash
curl -X GET "http://localhost5000/status/<taskid>
```
