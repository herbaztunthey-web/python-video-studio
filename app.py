import requests
import pandas as pd

# 1. Configuration (The Logic)
CITY = 'Ibadan'
API_KEY = 'aad4cbdae56d6d693c4f99064fe46dcd'
URL = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric'

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
