from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models.metrics import Metrics

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('main/home.html')

@main.route('/dashboard')
@login_required
def dashboard():
    try:
        metrics = Metrics.query.filter_by(user_id=current_user.id).all()
        if metrics:
            return render_template('main/dashboard.html', metrics=metrics)
        return redirect(url_for('analytics.upload_data'))
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        return redirect(url_for('analytics.upload_data'))