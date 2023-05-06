from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TaskModel
from schemas import TaskSchema

blp = Blueprint("tasks", __name__, description="Operations on tasks")

@blp.route("/")
class TaskList(MethodView):
    @blp.response(200, TaskSchema(many=True))
    def get(self):
        return TaskModel.query.all()

    @blp.arguments(TaskSchema)
    @blp.response(201, TaskSchema)
    def post(self, task_data):
        task = TaskModel.query.filter_by(name=task_data["name"]).first()
        if task:
            abort(400, message="A task with that name already exists.")

        task = TaskModel(**task_data)
        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred creating the task.")

        return task

@blp.route("/<int:task_id>")
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
