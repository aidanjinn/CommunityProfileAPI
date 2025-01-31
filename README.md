
# Community Profile Creation API

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-orange)

The Community Profile Creation API is a Flask-based application that scrapes demographic data from Wikipedia and energy profile data from the U.S. Energy Information Administration (EIA) to create a comprehensive community profile for a given location. The API leverages Gemini to generate a formatted profile and saves it as a local text file.

## Features

- **Wikipedia Data Scraping**: Retrieves demographic data for a specified community from Wikipedia.
- **EIA Data Integration**: Fetches energy profile data for the state associated with the community.
- **Community Profile Generation**: Combines demographic and energy data to create a detailed community profile.
- **Local File Storage**: Saves the generated profile as a formatted text file locally.

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
