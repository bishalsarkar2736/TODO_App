from flask import Blueprint, current_app
from flask_mail import Message
from datetime import datetime, timedelta
from app.models import Task, User
from app import mail, db
from apscheduler.schedulers.background import BackgroundScheduler

reminders_bp = Blueprint('reminders', __name__, url_prefix='/reminders')

def send_due_reminders():
    """Send email reminders for tasks due within the next 24 hours."""
    with current_app.app_context():
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        due_tasks = Task.query.filter(Task.due_date <= tomorrow, Task.status != "Done").all()

        for task in due_tasks:
            user = User.query.get(task.user_id)
            if not user or not user.email:
                continue

            msg = Message(
                subject=f"Reminder: '{task.title}' is due soon!",
                recipients=[user.email],
                body=f"Hello {user.username},\n\nYour task '{task.title}' is due on {task.due_date.strftime('%Y-%m-%d %H:%M')}.\n\nDon’t forget to complete it!\n\n– ToDo App"
            )
            mail.send(msg)
            print(f"Reminder sent to {user.email} for task '{task.title}'")

def start_scheduler(app):
    """Start the background scheduler safely inside Flask context."""
    scheduler = BackgroundScheduler()

    def job_wrapper():
        with app.app_context():
            send_due_reminders()

    scheduler.add_job(job_wrapper, 'interval', hours=1)
    scheduler.start()
    print("✅ Reminder scheduler started (runs every 1 hour)")

@reminders_bp.route('/test')
def test_reminder():
    send_due_reminders()
    return "Reminders sent manually!"
