import openai
from dotenv import load_dotenv
import os

load_dotenv()

class AIAgent:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
    
    def generate_insights(self, metrics_data):
        """Generate insights and recommendations using OpenAI"""
        prompt = f"""
        Analyze the following SaaS metrics and provide insights and recommendations:
        
        Metrics:
        - Total Users: {metrics_data['total_users']}
        - Active Users: {metrics_data['active_users']}
        - New Users: {metrics_data['new_users']}
        - Churn Rate: {metrics_data['churn_rate']}%
        - Total Revenue: ${metrics_data['total_revenue']}
        - Average Revenue per User: ${metrics_data['avg_revenue_per_user']}
        - Growth Rate: {metrics_data['growth_rate']}%
        - Retention Rate: {metrics_data['retention_rate']}%
        
        Please provide:
        1. A summary of the main trends
        2. Key insights about user behavior
        3. Specific recommendations for improvement
        """
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a SaaS business analyst expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000
            )
            return {
                'summary': response.choices[0].message.content,
                'status': 'success'
            }
        except Exception as e:
            return {
                'summary': f"Error generating insights: {str(e)}",
                'status': 'error'
            }
    
    def generate_report(self, metrics_data, insights):
        """Generate a formatted PDF report"""
        # This could be implemented as a bonus feature
        pass