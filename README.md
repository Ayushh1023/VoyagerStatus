
## Overview
This documentation provides the steps to run a Flask application that scrapes and serves data from the [NASA Voyager Mission Status](https://voyager.jpl.nasa.gov/mission/status/) page.



## Run the Flask App
```python
python app.py
```

## Access the Application
Open your web browser and go to http://127.0.0.1:5000/ to see the welcome message.</br>
To get the Voyager mission status, navigate to http://127.0.0.1:5000/api/voyager-status.

## API Endpoints

### 1. Welcome Message
- **URL:** `/`
- **Method:** `GET`
- **Description:** Returns a welcome message and information about the available API endpoint.

### 2. Voyager Mission Status
- **URL:** `/api/voyager-status`
- **Method:** `GET`
- **Description:** Returns the scraped data from the Voyager mission status page.

## Notes
- Ensure that `chromedriver` is in your system's `PATH` or specify its location in the script.
- The Flask app runs in debug mode, which is not recommended for production environments.
