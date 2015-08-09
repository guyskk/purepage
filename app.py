# coding:utf-8

from flask import Flask, url_for
from flask_restful import reqparse, abort, Api, Resource
from flask_restful import marshal_with, fields
from flask.ext.cors import CORS
from datetime import datetime
import time


app = Flask(__name__)
api = Api(app)
CORS(app)

todo_resp = {
    "task": fields.String,
    "done": fields.Boolean,
    "date": fields.String,
    "url": fields.Url('todo')
}

todo_parser = reqparse.RequestParser()
todo_parser.add_argument(
    name='task',
    required=True
)
todo_parser.add_argument(
    name='done',
    type=bool,
    default=False
)
todo_parser.add_argument(
    name='date',
    default=time.strftime("%x %X", time.localtime())
)

TODOS = [{'task': 'build an API', 'done': False,
          'date': time.strftime("%x %X", time.localtime())}] * 4


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id >= len(TODOS):
        abort(404, message="Todo {} doesn't exist".format(todo_id))


def make_public_task(todo, todo_id):
    todo['todo_id'] = todo_id  # url_for('todo', todo_id=todo_id)
    return todo


class Todo(Resource):

    @marshal_with(todo_resp)
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return make_public_task(TODOS[todo_id], todo_id)
        # return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    @marshal_with(todo_resp)
    def put(self, todo_id):
        args = todo_parser.parse_args()
        task = args
        TODOS[todo_id] = task
        return make_public_task(task, todo_id), 201


class TodoList(Resource):

    def get(self):
        return TODOS

    @marshal_with(todo_resp)
    def post(self):
        args = todo_parser.parse_args()
        todo_id = len(TODOS)
        TODOS.append(args)
        return make_public_task(TODOS[todo_id], todo_id), 201


@app.route("/")
def index():
    return "hello world"

api.add_resource(TodoList, '/todo', endpoint='todolist')
api.add_resource(Todo, '/todo/<int:todo_id>', endpoint='todo')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
