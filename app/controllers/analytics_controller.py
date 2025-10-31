import os
from werkzeug.utils import secure_filename
from ..models.metrics import Metrics
from ..utils.ai_agent import AIAgent
from .. import db
import pandas as pd

class AnalyticsController:
    ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
    
    @staticmethod
    def generate_sample_data():
        """Generate sample data file for users to use as template"""
        import pandas as pd
        import os
        
        sample_data = pd.DataFrame({
            'date': pd.date_range(start='2025-01-01', periods=12, freq='M'),
            'active_users': [1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3200],
            'new_users': [200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750],
            'churn_rate': [5.0, 4.8, 4.5, 4.2, 4.0, 3.8, 3.5, 3.2, 3.0, 2.8, 2.5, 2.2],
            'revenue': [10000, 12000, 14000, 16000, 18000, 20000, 22000, 24000, 26000, 28000, 30000, 32000]
        })
        
        # Create uploads directory if it doesn't exist
        os.makedirs('uploads', exist_ok=True)
        
        # Save as both CSV and Excel for user convenience
        csv_path = os.path.join('uploads', 'sample_data.csv')
        excel_path = os.path.join('uploads', 'sample_data.xlsx')
        
        sample_data.to_csv(csv_path, index=False)
        sample_data.to_excel(excel_path, index=False)
        
        return {'csv_path': csv_path, 'excel_path': excel_path}
    
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in AnalyticsController.ALLOWED_EXTENSIONS
    
    @staticmethod
    def process_upload(file, user_id):
        try:
            if not file:
                return {'status': 'error', 'message': 'No file provided'}
            
            if not AnalyticsController.allowed_file(file.filename):
                return {
                    'status': 'error',
                    'message': 'Invalid file format. Please upload a CSV or Excel file (.csv or .xlsx)'
                }
            
            filename = secure_filename(file.filename)
            upload_path = os.path.join('uploads', filename)
            os.makedirs('uploads', exist_ok=True)
            file.save(upload_path)
            
            # Create sample data template if needed
            sample_path = os.path.join('uploads', 'sample_data.csv')
            if not os.path.exists(sample_path):
                sample_data = pd.DataFrame({
                    'date': pd.date_range(start='2025-01-01', periods=12, freq='M'),
                    'active_users': [1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3200],
                    'new_users': [200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750],
                    'churn_rate': [5.0, 4.8, 4.5, 4.2, 4.0, 3.8, 3.5, 3.2, 3.0, 2.8, 2.5, 2.2],
                    'revenue': [10000, 12000, 14000, 16000, 18000, 20000, 22000, 24000, 26000, 28000, 30000, 32000]
                })
                sample_data.to_csv(sample_path, index=False)
            
            # Analyze data
            try:
                stats = Metrics.analyze_data(upload_path)
            except ValueError as e:
                return {'status': 'error', 'message': str(e)}
            except Exception as e:
                return {'status': 'error', 'message': f'Error analyzing data: {str(e)}'}
            
            # Generate AI insights
            try:
                ai_agent = AIAgent()
                insights = ai_agent.generate_insights(stats)
            except Exception as e:
                insights = {'summary': f'Error generating insights: {str(e)}', 'status': 'error'}
            
            # Create new metrics record
            try:
                new_metrics = Metrics(
                    active_users=stats['active_users'],
                    new_users=stats['new_users'],
                    churn_rate=stats['churn_rate'],
                    revenue=stats['total_revenue'],
                    file_path=upload_path,
                    analysis_summary=str(stats),
                    ai_recommendations=insights['summary'],
                    user_id=user_id
                )
                
                db.session.add(new_metrics)
                db.session.commit()
                
                # Generate visualizations
                if 'dataframe' in stats:
                    Metrics.generate_visualizations(stats['dataframe'], upload_path)
                
                return {
                    'status': 'success',
                    'stats': stats,
                    'insights': insights['summary']
                }
            except Exception as e:
                db.session.rollback()
                return {'status': 'error', 'message': f'Error saving metrics: {str(e)}'}
                
        except Exception as e:
            return {'status': 'error', 'message': f'Error processing file: {str(e)}'}
    
    @staticmethod
    def get_user_metrics(user_id):
        return Metrics.query.filter_by(user_id=user_id).order_by(Metrics.date.desc()).all()