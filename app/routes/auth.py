from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db,bcrypt
from app.models import User
from flask_login import login_user,logout_user,login_required,current_user

#  the blueprint object here
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# USER_CREDENTIALS = {
#     'username': 'admin',
#     'password': '1234'
# }

@auth_bp.route('/signup', methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        confirm = request.form.get('confirm','').strip()
        email = request.form.get('email').strip()

        if not username or not password or not email:
            flash("All fields are required!", "danger")
            return redirect(url_for("auth.signup"))

        if password != confirm:
            flash("Passwords do not match!",'danger')
            return redirect(url_for('auth.signup'))

        #check if user exist
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Try a different one.",'danger')
            return redirect(url_for('auth.signup'))
        
        #Create new user
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username = username, email=email, password = hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash("Signup succesfull! Please log in.", 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        

        return redirect(url_for('tasks.view_tasks'))
       
    
    if request.method == "POST":
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        user = User.query.filter_by(username=username).first()

        
        if user and bcrypt.check_password_hash(user.password,password):
            
            login_user(user)
           
            flash('Login Successful', 'success')

            next_page = request.args.get('next')

            
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            else:
                return redirect(url_for('tasks.view_tasks'))
            
        else:
            flash('Invalid username or password', 'danger')
        
     
    next_page = request.args.get('next')

    return render_template('login.html', next_page=next_page)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    #session.pop('user', None)
    # session.pop('user_id',None)
    # session.pop('username',None)
    flash('Logged Out Successfully', 'info')
    return redirect(url_for('auth.login'))
