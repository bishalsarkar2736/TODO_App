from app import db,bcrypt,login_manager
from datetime import datetime,timezone
from datetime import datetime
from flask_login import UserMixin





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    tasks = db.relationship('Task', backref='task_user', lazy=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    




class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100),nullable = False)
    status = db.Column(db.String(200), default = "Pending")
    created_at = db.Column(db.DateTime, default = datetime.now(timezone.utc))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False)
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(20), nullable=False, default='Medium')
    #email = db.Column(db.String(120), unique=True, nullable=False)


    # user = db.relationship("User", backref=db.backref('tasks', lazy=True))

    def __repr__(self):
        return f"<Task {self.title}>"
    