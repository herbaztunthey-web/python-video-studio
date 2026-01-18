import os
from flask import Flask
import requests
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    API_KEY = os.environ.get('WEATHER_API_KEY')
    CITY = 'Lagos'
    URL = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric'

    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        df = pd.json_normalize(data['list'])
        # Return the data as a simple HTML table for the browser
        return df[['dt_txt', 'main.temp', 'main.humidity']].head().to_html()
    return "Error fetching data"


if __name__ == "__main__":
    # Render requires the app to listen on port 10000 by default
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
