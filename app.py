import os
from flask import Flask
import requests
import pandas as pd

app = Flask(__name__)


def get_color(temp):
    if temp > 30:
        return "#e74c3c"  # Red for Heat
    if temp < 15:
        return "#3498db"  # Blue for Cold
    return "#2ecc71"  # Green for Moderate


@app.route('/')
def home():
    API_KEY = os.environ.get('WEATHER_API_KEY')
    # Add as many cities as you like here
    CITIES = ['Lagos', 'London', 'New York', 'Tokyo', 'Dubai', 'Accra']
    all_data = []

    for city in CITIES:
        URL = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
        try:
            response = requests.get(URL)
            if response.status_code == 200:
                data = response.json()
                df = pd.json_normalize(data['list'])
                latest = df.head(1).copy()
                latest['City'] = city
                # Apply the color logic
                temp = latest['main.temp'].values[0]
                latest['Color'] = get_color(temp)
                all_data.append(latest)
        except Exception as e:
            print(f"Error fetching {city}: {e}")

    final_df = pd.concat(all_data)

    # Building the HTML with the features
    html = """
    <html>
    <head>
        <style>
            body { font-family: 'Segoe UI', sans-serif; margin: 40px; background-color: #f4f7f6; }
            .card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
            h1 { color: #1f3b64; margin-bottom: 5px; }
            .timestamp { color: #7f8c8d; margin-bottom: 25px; font-size: 0.9em; }
            table { width: 100%; border-collapse: collapse; }
            th { text-align: left; padding: 15px; background: #1f3b64; color: white; text-transform: uppercase; }
            td { padding: 15px; border-bottom: 1px solid #eee; font-weight: bold; }
            .temp-badge { padding: 5px 10px; border-radius: 5px; color: white; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Global Economic Weather Monitor</h1>
            <div class="timestamp">Live Market Data Sync: Successful</div>
            <table>
                <tr>
                    <th>City</th>
                    <th>Local Time (UTC)</th>
                    <th>Temperature</th>
                    <th>Humidity</th>
                </tr>
    """

    for _, row in final_df.iterrows():
        html += f"""
        <tr>
            <td>{row['City']}</td>
            <td>{row['dt_txt']}</td>
            <td><span class="temp-badge" style="background-color: {row['Color']}">{row['main.temp']}°C</span></td>
            <td>{row['main.humidity']}%</td>
        </tr>
        """

    html += "</table></div></body></html>"
    return html


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
