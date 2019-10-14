from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://pwiklybfzdfamj:4b41fdba0e00e498b6b2937746e6c598358c3481b4214c2118e5f318299da93c@ec2-54-235-163-246.compute-1.amazonaws.com:5432/d7cvdd3evl78q1"

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Todo(db.Model):
    __tablename__ ="todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    done = db.Column(db.Boolean)

    def __init__(self, title, done):
        self.title =title
        self.done = done
        

class TodoSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "done")


todo_schema = TodoSchema()
todos_schema=TodoSchema(many=True)

@app.route("/todos", methods=["GET"])
def get_todos():
    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)
    return jsonify(result)

@app.route("/todo", methods=["POST"])
def add_todo():
    title = request.json["title"]
    done = request.json["done"]

    new_todo= Todo(title,done)
    db.session.add(new_todo)
    db.session.commit()

    created_todo = Todo.query.get(new_todo.id)
    return todo_schema.jsonify(created_todo)

if __name__ == "__main__":
    app.debug = True
    app.run()