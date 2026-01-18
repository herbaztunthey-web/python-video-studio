from flask import Flask, request
import os
import requests
import pandas as pd

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    API_KEY = os.environ.get('WEATHER_API_KEY')
    # Default static cities for the landing page
    cities = ['Lagos', 'London', 'New York']

    # DYNAMIC LOGIC: If user types a city in the search bar
    if request.method == 'POST':
        user_city = request.form.get('city')
        if user_city:
            cities = [user_city]

    all_data = []
    for city in cities:
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
        res = requests.get(url)
        if res.status_code == 200:
            df = pd.json_normalize(res.json()['list'])
            latest = df.head(1).copy()
            latest['City'] = city
            all_data.append(latest)

    # UI with Search Bar
    html = """
    <style>
        body { font-family: sans-serif; margin: 50px; background: #f4f7f6; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        input { padding: 10px; width: 200px; border-radius: 5px; border: 1px solid #ddd; }
        button { padding: 10px; background: #1f3b64; color: white; border: none; border-radius: 5px; cursor: pointer; }
        table { width: 100%; margin-top: 20px; border-collapse: collapse; }
        th { background: #1f3b64; color: white; padding: 10px; text-align: left; }
        td { padding: 10px; border-bottom: 1px solid #eee; }
    </style>
    <div class="card">
        <h1>Global Weather Search</h1>
        <form method="POST">
            <input type="text" name="city" placeholder="Enter city name...">
            <button type="submit">Analyze City</button>
        </form>
        <table>
            <tr><th>City</th><th>Temp</th><th>Humidity</th></tr>
    """
    for _, row in pd.concat(all_data).iterrows():
        html += f"<tr><td>{row['City']}</td><td>{row['main.temp']}°C</td><td>{row['main.humidity']}%</td></tr>"

    return html + "</table></div>"
