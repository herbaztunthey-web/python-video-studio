import os
import requests
import pandas as pd
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    API_KEY = os.environ.get('WEATHER_API_KEY')
    # Starting list of cities
    cities_to_track = ['Lagos', 'London', 'New York', 'Tokyo']

    # If user searches, add that city to the top of the list
    if request.method == 'POST':
        user_search = request.form.get('city')
        if user_search and user_search not in cities_to_track:
            cities_to_track.insert(0, user_search)

    all_city_data = []

    for city in cities_to_track:
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                df = pd.json_normalize(data['list'])
                # Select the first forecast entry for this city
                city_row = df.head(1).copy()
                city_row['City Name'] = city.title()
                all_city_data.append(city_row)
        except Exception as e:
            print(f"Error fetching {city}: {e}")

    # Combine all city rows into one vertical table
    if all_city_data:
        final_df = pd.concat(all_city_data, ignore_index=True)
        # Clean the columns for the final display
        report = final_df[['City Name', 'dt_txt',
                           'main.temp', 'main.humidity']]
        report.columns = ['Market Location',
                          'Forecast Time', 'Temp (°C)', 'Humidity (%)']
    else:
        return "<h1>Analysis Error: No data found. Check your API Key.</h1>"

    # Styling and Layout
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_style = f"""
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; margin: 40px; background-color: #f8f9fa; }}
        .dashboard-card {{ background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }}
        h1 {{ color: #1f3b64; border-bottom: 3px solid #1f3b64; padding-bottom: 10px; }}
        input {{ padding: 12px; width: 300px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; }}
        button {{ padding: 12px 25px; background: #1f3b64; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 30px; }}
        th {{ background-color: #1f3b64; color: white; padding: 15px; text-align: left; }}
        td {{ padding: 15px; border-bottom: 1px solid #eee; font-weight: 500; }}
        tr:hover {{ background-color: #f1f1f1; }}
        .timestamp {{ margin-top: 20px; font-size: 0.8em; color: #7f8c8d; text-align: right; }}
    </style>
    <div class="dashboard-card">
        <h1>Economic Weather Intelligence Monitor</h1>
        <form method="POST">
            <input type="text" name="city" placeholder="Enter city (e.g. Paris, Abuja)..." required>
            <button type="submit">Analyze Market</button>
        </form>
        {report.to_html(index=False)}
        <div class="timestamp">Last Intelligence Sync: {now} (UTC)</div>
    </div>
    """
    return html_style


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
