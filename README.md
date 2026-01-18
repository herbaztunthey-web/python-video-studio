# 🌍 Global Weather Intelligence Dashboard

A professional data analytics application that fetches, processes, and visualizes real-time weather intelligence for international markets.

## 🚀 Live Demo
[View the Live Dashboard on Render](https://python-video-studio.onrender.com)

## 🛠️ Tech Stack
- **Language:** Python 3.13
- **Data Analysis:** Pandas, NumPy, SciPy (Linear Regression)
- **Visualization:** Matplotlib, Seaborn
- **Web Framework:** Flask & Gunicorn
- **Deployment:** Render (Cloud)
- **Version Control:** Git & GitHub

## 📊 Key Features
- **Multi-City Monitoring:** Real-time data fetching for Lagos, London, New York, Tokyo, and more.
- **Predictive Analytics:** Integrated a trendline (best-fit line) to forecast temperature shifts.
- **Smart UI:** Conditional CSS formatting (Red for Heat >30°C, Blue for Cold <15°C).
- **Production Ready:** Secure API key handling using `os.environ`.

## 📈 Analysis Methodology
The project utilizes a `scipy.stats.linregress` model to calculate the rate of change in local temperatures, allowing for 5-day trend predictions.

## 📦 Installation & Setup
1. Clone the repo: `git clone [YOUR_GITHUB_URL]`
2. Install requirements: `pip install -r requirements.txt`
3. Set your API Key: `export WEATHER_API_KEY='your_key_here'`
4. Run the app: `python app.py`