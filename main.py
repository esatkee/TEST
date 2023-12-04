from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "your DB path"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    complete = db.Column(db.Boolean)


@app.route("/")
def index():
    todos = Todo.query.all()

    return render_template("index.html", todos=todos)

@app.route("/add", methods=["POST"])
def adTodo():
    title = request.form.get("title")
    newTodo = Todo(title=title, complete=False)
    with app.app_context():
        db.session.add(newTodo)
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/complete/<string:id>", methods=["POST"])
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first()

    if request.method == "POST":
        data = request.get_json()
        checkBox_value = data.get('cbData')

        if checkBox_value == True:
            todo.complete = True
            print(checkBox_value, " if ", id)
        elif checkBox_value == False:
            todo.complete = False
            print(checkBox_value, " elif", id)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
