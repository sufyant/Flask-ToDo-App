from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "todo"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///<todo.db>'
db = SQLAlchemy(app)

class Todo(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    title    = db.Column(db.String(80))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)


@app.route('/add', methods=["POST"])
def addtodo():
    title   = request.form.get("title")
    newTodo = Todo(title=title, complete=False)
    db.session.add(newTodo)
    db.session.commit()
    
    flash("Başarıyla eklendi!", "success")
    return redirect(url_for("index"))


@app.route('/complete/<string:id>')
def complete(id):
    todo = Todo.query.filter_by(id=id).first()

    todo.complete = not todo.complete
    db.session.commit()

    flash("Başarıyla değiştirildi!", "success")
    return redirect(url_for("index"))


@app.route('/delete/<string:id>')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()

    db.session.delete(todo)
    db.session.commit()

    flash("Başarıyla silindi!", "success")
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
