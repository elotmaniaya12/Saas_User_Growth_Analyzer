# SaaS User Growth Analyzer

A Flask-based web application that analyzes SaaS user data and automatically generates insights using AI.

## Features

- File upload for CSV and Excel data
- Automated data analysis using Pandas and NumPy
- AI-powered insights and recommendations using OpenAI
- Interactive dashboard with visualizations
- User authentication and data privacy
- Responsive design

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/saas-user-growth-analyzer.git
cd saas-user-growth-analyzer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
```

5. Run the application:
```bash
python run.py
```

## Usage

1. Register/Login to your account
2. Navigate to the Upload page
3. Upload your SaaS metrics data (CSV or Excel)
4. View the automated analysis and AI insights on the dashboard

## Data Format

Your input file should contain the following columns:
- date: Date of the metrics
- active_users: Number of active users
- new_users: Number of new users
- churn_rate: Churn rate as a percentage
- revenue: Revenue amount

## Features

- **Data Upload**: Support for CSV and Excel files
- **Automated Analysis**: 
  - User growth metrics
  - Revenue analysis
  - Churn rate calculation
  - Trend detection
- **AI Insights**:
  - Trend explanation
  - Pattern identification
  - Strategic recommendations
- **Visualizations**:
  - User growth charts
  - Revenue trends
  - Churn analysis

## Project Structure

```
saas_user_growth_analyzer/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── user.py
│   │   └── metrics.py
│   ├── controllers/
│   │   └── analytics_controller.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── main.py
│   │   └── analytics.py
│   ├── utils/
│   │   └── ai_agent.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── 404.html
│   │   └── analytics/
│   │       ├── upload.html
│   │       └── dashboard.html
│   └── static/
│       └── css/
│           └── style.css
├── run.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.