from flask import Blueprint, render_template, redirect,url_for,request, flash,session
from app import db
from app.models import Task,User
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy import func

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/', methods = ["GET"])
@login_required
def view_tasks():

    search_q = request.args.get('search', '').strip()
    filter_priority = request.args.get('filter_priority', '').strip()
    filter_status = request.args.get('filter_status', '').strip()

    q = Task.query.filter_by(user_id = current_user.id)

    if search_q:
        q = q.filter(Task.title.ilike(f"%{search_q}%"))

    if filter_priority:
        q = q.filter(Task.priority == filter_priority)

    if filter_status:
        q = q.filter(Task.status == filter_status)

    tasks = q.order_by(Task.due_date.asc()).all() 
   
    
    # tasks = Task.query.filter_by(user_id = current_user.id).order_by(Task.due_date).all()
   
    return render_template('tasks.html', tasks = tasks)

@tasks_bp.route('/delete/<int:task_id>', methods=["POST"])
@login_required
def delete_task(task_id):
   
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        flash("Task not found or unauthorized",'danger')
        return redirect(url_for('tasks.view_tasks'))
    
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!",'success')
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/add', methods = ["POST"])
@login_required
def add_task():
    
    
    title = request.form.get('title').strip()
    due_date_str= request.form.get('due_date')
    due_time_str = request.form.get('due_time')
    priority = request.form.get('priority')
  

    due_datetime = None
    if due_date_str:
        try:
            if due_time_str:

                due_datetime= datetime.strptime(f"{due_date_str} {due_time_str}", "%Y-%m-%d %H:%M")
            else:
                due_datetime = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            flash("Invalid date format! Please use YYYY-MM-DD and HH:MM", 'danger')
            return redirect(url_for('tasks.view_tasks'))

     

    if title.strip():
        
        new_task = Task(title=title,user_id=current_user.id, 
        status = "Pending",due_date=due_datetime,priority=priority)
        db.session.add(new_task)
        db.session.commit()
        flash("✅ Task added successfully", 'success')
    else:
        flash("⚠️ Task title cannot be empty!", 'warning')

    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/toggle/<int:task_id>', methods = ["POST"])
@login_required
def toggle_status(task_id):
   

    task = Task.query.get_or_404(task_id)
   
    if task.user_id != current_user.id:
        flash("Unauthorized action!", 'danger')
        redirect(url_for("tasks.view_tasks"))

    #if task:
    if task.status == "Pending":
        task.status = "Working"
    elif task.status == "Working":
        task.status = "Done"
    else:
        task.status = "Pending"
    db.session.commit()

    # else:
    # flash("Task Complted",'success')
    flash(f"Task '{task.title}' marked as {task.status}!", 'success')

    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/clear', methods = ["POST"])
@login_required
def clear_tasks():
    

    Task.query.filter_by(user_id=current_user.id).delete()
   
    db.session.commit()
    flash('All tasks cleared', 'info')
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/edit/<int:task_id>', methods=["GET","POST"])
@login_required
def edit_task(task_id):
   
    
    task= Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash("Unauthorized access!",'danger')
        return redirect(url_for('tasks.view_tasks'))
    
    if request.method == "POST":
        new_title = request.form.get('title').strip()
        due_date_str= request.form.get('due_date')

        if not new_title:
            flash('Task title cannot be empty!', 'warning')
            return redirect(url_for('tasks.view_tasks', task_id=task.id))
        
        task.title=new_title

        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                flash("Invalid date format!", 'danger')
                return redirect(url_for('tasks.edit_task', task_id=task.id))
        else:
            task.due_date = None

        db.session.commit()
        flash("Task updated successfully!", 'success')
        return redirect(url_for('tasks.view_tasks'))
    return render_template('edit_task.html', task=task)



@tasks_bp.route('/dashboard')
@login_required
def dashboard():

    total_tasks = Task.query.filter_by(user_id=current_user.id).count()
    done_tasks = Task.query.filter_by(user_id = current_user.id, status = "Done").count()
    working_tasks = Task.query.filter_by(user_id = current_user.id, status = "Working").count()
    pending_tasks = Task.query.filter_by(user_id = current_user.id, status = "Pending").count()

    return render_template('dashboard.html',
                           total_tasks = total_tasks,
                           done_tasks = done_tasks,
                           working_tasks = working_tasks,
                           pending_tasks = pending_tasks)