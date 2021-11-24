from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_restful import Api, Resource, abort
from models import db, Todo
import logging

logging.basicConfig(filename='/home/nesren/iti/flask_iti/flask_todo/flask.logs')
app = Flask(__name__)
todo_api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class TodoRUD(Resource):
    def get(self, **kwargs):
        todo_id = kwargs.get('todo_id')
        task = Todo.query.get(todo_id)
        if not task:
            abort(404, message='Not Found')

        data = {
            'id': task.id,
            'name': task.name,
            'priority': task.priority,
            'description': task.description,
            'finished': task.finished
        }

        return data, 200

    def delete(self, *args, **kwargs):

        todo_id = kwargs.get('todo_id')
        todo_obj = Todo.query.get(todo_id)
        db.session.delete(todo_obj)
        db.session.commit()

        return {'message': 'Deleted Successfully'}, 200

    def patch(self, *args, **kwargs):
        id = kwargs.get('todo_id')
        task = Todo.query.get(id)
        if not task:
            abort(404, message='Not Found')
        if request.form.get('name'):
            task.name = request.form.get('name')
        if request.form.get('priority'):
            task.priority = request.form.get('priority')
        if request.form.get('description'):
            task.description = request.form.get('description')
        if request.form.get('finished'):
            task.finished = request.form.get('finished')
        db.session.commit()
        return {'message': 'Updated Successfully'}, 200


class TodoLC(Resource):
    def post(self):
        try:
            data = {
                'name': request.form.get('name'),
                'priority': request.form.get('priority'),
                'description': request.form.get('description'),
                'finished': False
            }

            todo_obj = Todo(**data)
            db.session.add(todo_obj)
            db.session.commit()

            return {'message': 'Task Created Successfully'}, 201
        except Exception as e:
            abort(500, message='Internal Server Error')

    def get(self):
        try:
            todo_objects = Todo.query.filter().all()
            limit = request.args.get('limit')
            my_new_list = []

            for task in todo_objects:
                data = {
                    'id': task.id,
                    'name': task.name,
                    'priority': task.priority,
                    'description': task.description,
                    'finished': task.finished
                }

                my_new_list.append(data)

            if limit:
                print(type(limit))
                my_new_list = my_new_list[:int(limit)]

            return my_new_list

        except Exception as e:
            abort(500, message="Internal Server Error {}".format(e))


todo_api.add_resource(TodoLC, '/todo')

todo_api.add_resource(TodoRUD, '/todo/<int:todo_id>')

db.init_app(app)


@app.before_first_request
def initiate_data_base_tables():
    db.create_all()


app.run(debug=True)
