from flask import Blueprint, redirect, url_for, session

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('tasks.view_tasks'))
    else:
        return redirect(url_for('auth.login'))
