from flask import jsonify, render_template, jsonify, redirect, request, url_for
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TaskModel
from schemas import TaskSchema

blp = Blueprint("tasks", __name__, description="Operations on tasks")

@blp.route("/task")
class TaskList(MethodView):
    @blp.response(200, TaskSchema)
    def get(self):
        
        return TaskModel.query.all()

    @blp.arguments(TaskSchema)
    @blp.response(201, TaskSchema)
    def post(self, task_data):
        task = TaskModel.query.filter_by(name=task_data["name"]).first()

        task = TaskModel(**task_data)
        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred creating the task.")

        return task

@blp.route("/task/<int:task_id>")
class Task(MethodView):
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        return task

    @blp.response(204)
    def delete(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully."})

@blp.route("/")
def home():
        toDoList = TaskModel.query.all()
        return render_template("index.html", toDoList=toDoList)

@blp.arguments(TaskSchema)
@blp.route("/add", methods=["POST"])
def add(): 
    name = request.form.get("todo_item")
    task = TaskModel(name=name, status="incomplete")
    db.session.add(task)
    db.session.commit()
    
    return redirect(url_for("tasks.home"))

@blp.route("/delete/<int:task_id>")
def delete(task_id):
    task = TaskModel.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    
    return redirect(url_for("tasks.home"))