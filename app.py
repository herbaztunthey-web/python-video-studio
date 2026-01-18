import os
from flask import Flask
import requests
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    # Security: Fetching the key from Render Environment Variables
    API_KEY = os.environ.get('WEATHER_API_KEY')
    CITY = 'Lagos'
    URL = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric'

    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        df = pd.json_normalize(data['list'])

        # Data Cleaning: Extracting specific columns for your report
        report = df[['dt_txt', 'main.temp', 'main.humidity']].head(15)
        report.columns = ['Date & Time', 'Temperature (°C)', 'Humidity (%)']

        # Professional CSS Styling
        html_style = """
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 50px; background-color: #f0f2f5; }
            .container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h1 { color: #1f3b64; border-bottom: 2px solid #1f3b64; padding-bottom: 10px; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th { background-color: #1f3b64; color: white; padding: 12px; text-align: left; }
            td { padding: 12px; border-bottom: 1px solid #eee; }
            tr:hover { background-color: #f9f9f9; }
        </style>
        <div class="container">
            <h1>Economic Weather Intelligence Report</h1>
            <p>Location: <b>Lagos</b> | Source: OpenWeather API</p>
        """
        return html_style + report.to_html(index=False) + "</div>"

    return "<h2>Error: Could not fetch weather data. Check your API Key in Render.</h2>"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
