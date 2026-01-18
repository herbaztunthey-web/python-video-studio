import os
import requests
import pandas as pd

# Use os.environ to get the key from Render's secret settings
API_KEY = os.environ.get('WEATHER_API_KEY')
CITY = 'Lagos'

# The rest of your logic remains the same
URL = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric'
# ... (rest of your fetch and processing code)

# 2. Execution (The Logic)
response = requests.get(URL)
data = response.json()

if response.status_code == 200:
    # 3. Processing (The Logic)
    df = pd.json_normalize(data['list'])
    df['Date'] = pd.to_datetime(df['dt_txt'])

    # Selecting columns for your report
    report = df[['Date', 'main.temp', 'main.humidity']].head()

    print("LOGS: Data successfully processed for Render!")
    print(report)
else:
    print("LOGS: Failed to fetch data.")
