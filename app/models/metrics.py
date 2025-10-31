from .. import db
from datetime import datetime
import pandas as pd
import numpy as np

class Metrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    active_users = db.Column(db.Integer)
    new_users = db.Column(db.Integer)
    churn_rate = db.Column(db.Float)
    revenue = db.Column(db.Float)
    file_path = db.Column(db.String(500))
    analysis_summary = db.Column(db.Text)
    ai_recommendations = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Metrics {self.date}>'
    
    @staticmethod
    def analyze_data(file_path):
        """Analyze uploaded data file using pandas and numpy"""
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            
            # Convert date column to datetime if it exists
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            
            # Validate required columns
            required_columns = ['active_users', 'new_users', 'churn_rate', 'revenue']
            actual_columns = [col.lower() for col in df.columns]  # Convert to lowercase for case-insensitive comparison
            df.columns = actual_columns  # Update column names to lowercase
            
            # Create a mapping of common alternative column names
            column_mapping = {
                'active_users': ['active_users', 'active users', 'active', 'mau', 'monthly active users'],
                'new_users': ['new_users', 'new users', 'new', 'new signups', 'signups'],
                'churn_rate': ['churn_rate', 'churn rate', 'churn', 'churn %', 'churn percentage'],
                'revenue': ['revenue', 'total revenue', 'monthly revenue', 'mrr']
            }
            
            # Try to map columns to required names
            for required_col, alternatives in column_mapping.items():
                if required_col not in actual_columns:
                    # Check if any alternative exists in the dataframe
                    found = False
                    for alt in alternatives:
                        if alt in actual_columns:
                            df = df.rename(columns={alt: required_col})
                            found = True
                            break
            
            # Check for missing columns after mapping
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                error_msg = (
                    f"Missing required columns: {', '.join(missing_columns)}\n"
                    "Your file must contain the following columns:\n"
                    "- active_users: Number of active users\n"
                    "- new_users: Number of new users\n"
                    "- churn_rate: Rate of user churn (as percentage)\n"
                    "- revenue: Revenue amount\n"
                    "\nPlease ensure your file has these columns or similar variations."
                )
                raise ValueError(error_msg)
            
            # Convert numeric columns and handle any non-numeric values
            try:
                df['active_users'] = pd.to_numeric(df['active_users'], errors='coerce')
                df['new_users'] = pd.to_numeric(df['new_users'], errors='coerce')
                df['churn_rate'] = pd.to_numeric(df['churn_rate'], errors='coerce')
                df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
                
                # Check for any NaN values after conversion
                nan_columns = df[required_columns].columns[df[required_columns].isna().any()].tolist()
                if nan_columns:
                    raise ValueError(f"Found non-numeric values in columns: {', '.join(nan_columns)}")
            except Exception as e:
                raise ValueError(f"Error converting data: {str(e)}\nPlease ensure all values are numeric.")
            
            # Calculate basic statistics
            stats = {
                'total_users': int(df['active_users'].iloc[-1]),  # Latest active users count
                'active_users': int(df['active_users'].mean()),
                'new_users': int(df['new_users'].sum()),
                'churn_rate': float(df['churn_rate'].mean()),
                'total_revenue': float(df['revenue'].sum()),
                'avg_revenue_per_user': float(df['revenue'].sum() / df['active_users'].mean()),
                'growth_rate': float(((df['active_users'].iloc[-1] - df['active_users'].iloc[0]) 
                                    / df['active_users'].iloc[0] * 100)),
                'retention_rate': float(100 - df['churn_rate'].mean())
            }
            
            # Calculate trends using numpy's polyfit
            x = np.arange(len(df))
            stats['user_growth_trend'] = float(np.polyfit(x, df['active_users'], 1)[0])
            stats['revenue_growth_trend'] = float(np.polyfit(x, df['revenue'], 1)[0])
            
            # Store the dataframe for visualization
            stats['dataframe'] = df
            
            return stats
        except Exception as e:
            raise ValueError(f"Error analyzing data: {str(e)}")
    
    @staticmethod
    def generate_visualizations(df, file_path):
        """Generate and save visualizations"""
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        # Create time series plots
        plt.figure(figsize=(12, 6))
        plt.plot(df['date'], df['active_users'], label='Active Users')
        plt.plot(df['date'], df['new_users'], label='New Users')
        plt.title('User Growth Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Users')
        plt.legend()
        plt.savefig(f'{file_path}_users.png')
        plt.close()
        
        # Create revenue and churn analysis
        plt.figure(figsize=(12, 6))
        plt.plot(df['date'], df['revenue'], label='Revenue')
        plt.plot(df['date'], df['churn_rate'] * 100, label='Churn Rate (%)')
        plt.title('Revenue and Churn Rate Over Time')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.legend()
        plt.savefig(f'{file_path}_revenue_churn.png')
        plt.close()