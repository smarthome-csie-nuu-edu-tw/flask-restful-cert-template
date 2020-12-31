from flask import Flask
from flask_restful import request, reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

TODOS = {
    '1': {'task': 'build an API'},
    '2': {'task': '?????'},
    '3': {'task': 'profit!'},
}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))

parser = reqparse.RequestParser()
parser.add_argument('task')

# Todo
#   show a single todo item and lets you delete them
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return {"id": todo_id, "task": task}, 201


class  GetTodo(Resource):
    def post(self):
        print(reqparse.request.values.to_dict())
        parser.add_argument('id')
        args= parser.parse_args()
        abort_if_todo_doesnt_exist(args['id'])
        return TODOS[args['id']]

# TodoList
#   shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS
    def post(self):
        args = parser.parse_args()
        todo_id = '%d' % (len(TODOS) + 1)
        TODOS[todo_id] = {'task': args['task']}
        return {"id": todo_id, "data": args['task'] }, 201

class ServerInfo(Resource):
    def get(self):
        return {"serverInfo": "flask api v2 is working"}

##
## Actually setup the Api resource routing here
##
api.add_resource(ServerInfo,'/serverinfo')
api.add_resource(TodoList, '/todos')
api.add_resource(GetTodo,'/gettodo')
api.add_resource(Todo, '/todos/<string:todo_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

