**Automated Weather & Analytics Dashboard
Project Description**
This project is a full-stack web application that automatically fetches live weather data, processes it, and presents it in a user-friendly dashboard. Users can view current weather, 3-day forecasts, and pipeline analytics based on historical data.
Additionally, the project demonstrates data processing, analytics, and recommendations, providing value to end users through features such as clothing suggestions, activity alerts, and health notifications based on weather conditions.
Although the backend API is currently local and available via GitHub, the frontend is fully interactive and visually demonstrates the application's functionality.

**Features**
Weather Dashboard with current conditions and 3-day forecast
Dark Mode toggle for better user experience
Personalized recommendations:
Clothing suggestions
Activity alerts
Health notifications (UV index, pollen, air quality)
Pipeline Analytics (data insights from FastAPI backend)
Interactive charts with time series data
Fully responsive frontend using Next.js + Tailwind CSS

**Tech Stack Backend**
FastAPI – API framework
PostgreSQL – Relational database
SQLAlchemy – ORM for database interactions
Pandas – Data processing and cleaning
APScheduler – Task scheduling for automated data fetching

**Frontend**
Next.js – React-based framework for frontend
Tailwind CSS – Styling and responsive UI
Chart.js / Recharts – Interactive charts and graphs

**Dev Tools**
Python venv – Isolated Python environment
Node.js + npm – Frontend dependency management
Git & GitHub – Version control

**Getting Started**
**Prerequisites**
Python 3.10+
Node.js 18+
PostgreSQL database (if running backend locally)

**Installation**

**Clone the repository:**
git clone https://github.com/Fatimshaikh/automated_data_pipeline.git
cd automated-weather-dashboard


**Backend setup (optional if you want to run locally):**
cd app
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt


**Frontend setup:**
cd weather-dashboard
npm install
npm run dev


Open your browser at http://localhost:3000 to view the dashboard.
