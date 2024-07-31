from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

import awsgi

app = Flask(__name__)

# Initializing those tiresome global variables....duhhhhh!

url = "https://voyager.jpl.nasa.gov/mission/status/"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service("chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(3)


def scrape_voyager_status(url, driver):
    start_time = time.time()
    driver.get(url)

    data1 = {}
    data2 = {}

    ids1 = ['display_time_v1', 'voy1_km', 'voy1_au', 'voy1_kms', 'voy1_aus', 'voy1_speed', 'voy1_lt']
    ids2 = ['display_time_v2', 'voy2_km', 'voy2_au', 'voy2_kms', 'voy2_aus', 'voy2_speed', 'voy2_lt']

    for id in ids1:
        div_finder = driver.find_element(By.ID, id)
        div_data = div_finder.text.strip() if div_finder else 'Not found'
        data1[id] = div_data

    for id in ids2:
        div_finder = driver.find_element(By.ID, id)
        div_data = div_finder.text.strip() if div_finder else 'Not found'
        data2[id] = div_data

    time_ids = ['time_years', 'time_months', 'time_days', 'time_hours', 'time_minutes', 'time_seconds']

    countdown_data_v1 = {}
    countdown_data_v2 = {}

    for id in time_ids:
        element = driver.find_element(By.CSS_SELECTOR, f"#countdown_time_v1 .{id}")
        text = element.text.strip().split('\n')[0] if element else 'Not found'
        countdown_data_v1[id] = text

    data1['countdown_timer'] = countdown_data_v1

    for id in time_ids:
        element = driver.find_element(By.CSS_SELECTOR, f"#countdown_time_v2 .{id}")
        text = element.text.strip().split('\n')[0] if element else 'Not found'
        countdown_data_v2[id] = text

    data2['countdown_timer'] = countdown_data_v2

    end_time = time.time()
    encap_data = {
        "voyager_1": data1,
        "voyager_2": data2,
    }

    # peripheral devices

    encap_data['voyager_1']['Instrument_Status'] = {
        "Cosmic Ray Subsystem (CRS)": "ON",
        "Low-Energy Charged Particles (LECP)": "ON",
        "Magnetometer (MAG)": "ON",
        "Plasma Wave Subsystem (PWS)": "ON",
        "Plasma Science (PLS)": "OFF",
        "Imagine Science Subsystem (ISS)": "OFF",
        "Infrared Interferometer Spectrometer and Radiometer (IRIS)": "OFF",
        "Photopolarimeter Subsystem (PPS)": "OFF",
        "Planetary Radio Astronomy (PRA)": "OFF",
        "Ultraviolet Spectrometer (UVS)	": "OFF",

    }

    encap_data['voyager_2']['Instrument_Status'] = {
        "Cosmic Ray Subsystem (CRS)": "ON",
        "Low-Energy Charged Particles (LECP)": "ON",
        "Magnetometer (MAG)": "ON",
        "Plasma Wave Subsystem (PWS)": "ON",
        "Plasma Science (PLS)": "ON",
        "Imagine Science Subsystem (ISS)": "OFF",
        "Infrared Interferometer Spectrometer and Radiometer (IRIS)": "OFF",
        "Photopolarimeter Subsystem (PPS)": "OFF",
        "Planetary Radio Astronomy (PRA)": "OFF",
        "Ultraviolet Spectrometer (UVS)	": "OFF",

    }
    print(time.time() - start_time)

    return encap_data


@app.route('/api/voyager-status', methods=['GET'])
def get_voyager_status():
    status = scrape_voyager_status(url, driver)
    return jsonify(status)

@app.route('/', methods=['GET'])
def working_fine():
    return """
    Hello World!<br>
    <hr>
    - Voyager Mission Status : <span style="color:green;">Working Fine!!</span><br>
    --  /api/voyager-status : GET request for Voyager Mission Status<br>
    """

if __name__ == '__main__':
    app.run(debug=True)