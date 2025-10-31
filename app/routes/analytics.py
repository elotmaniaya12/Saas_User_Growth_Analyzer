from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from ..controllers.analytics_controller import AnalyticsController
from .. import db

analytics = Blueprint('analytics', __name__)

@analytics.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_data():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file uploaded', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        result = AnalyticsController.process_upload(file, current_user.id)
        if result['status'] == 'success':
            flash('File uploaded and analyzed successfully', 'success')
            return redirect(url_for('analytics.dashboard'))
        else:
            flash(result['message'], 'error')
            return redirect(request.url)
    
    return render_template('analytics/upload.html')

@analytics.route('/dashboard')
@login_required
def dashboard():
    try:
        metrics = AnalyticsController.get_user_metrics(current_user.id)
        if metrics:
            latest_metric = metrics[0]
            return render_template('analytics/dashboard.html', 
                                metrics=metrics,
                                latest_metric=latest_metric)
        else:
            flash('No analytics data available. Please upload your data first.', 'info')
            return render_template('analytics/dashboard.html', metrics=None)
    except Exception as e:
        flash(f'Error loading analytics: {str(e)}', 'error')
        return redirect(url_for('analytics.upload_data'))