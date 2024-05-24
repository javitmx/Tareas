from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import jsonify
import json

app = Flask(__name__)
# Clave secreta para proteger los formularios
app.config['SECRET_KEY'] = 'clave_secreta'
bootstrap = Bootstrap(app)

# Clase para el formulario de agregar tarea


class AddTaskForm(FlaskForm):
    task = StringField('Tarea', validators=[DataRequired()])
    submit = SubmitField('Agregar')

# Clase para el modelo de lista de tareas


class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append({"name": task, "completed": False})

    def remove_task(self, task):
        for t in self.tasks:
            if t["name"] == task:
                self.tasks.remove(t)
                return

    def display_tasks(self):
        return self.tasks

    def mark_task_completed(self, task):
        for t in self.tasks:
            if t["name"] == task:
                t["completed"] = True
                return

    def display_completed_tasks(self):
        completed_tasks = [task['name']
                           for task in self.tasks if task['completed']]
        return completed_tasks

    def display_incomplete_tasks(self):
        incomplete_tasks = [task['name']
                            for task in self.tasks if not task['completed']]
        return incomplete_tasks

    def save_tasks(self, filename="tasks.json"):
        with open(filename, "w") as file:
            json.dump(self.tasks, file)

    def load_tasks(self, filename="tasks.json"):
        try:
            with open(filename, "r") as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass


todo_list = TodoList()
todo_list.load_tasks()  # Cargar tareas al iniciar la aplicación

# Rutas de la aplicación Flask


@app.route('/', methods=['GET', 'POST'])
def index():
    form = AddTaskForm()
    if form.validate_on_submit():
        task = form.task.data
        todo_list.add_task(task)
        todo_list.save_tasks()
        return redirect(url_for('index'))
    return render_template('index.html', form=form, tasks=todo_list.display_tasks())


@app.route('/complete/<task>', methods=['POST'])
def complete(task):
    todo_list.mark_task_completed(task)
    todo_list.save_tasks()
    return redirect(url_for('index'))


@app.route('/delete/<task>', methods=['POST'])
def delete(task):
    todo_list.remove_task(task)
    todo_list.save_tasks()
    return redirect(url_for('index'))


@app.route('/completed_tasks')
def completed_tasks():
    return jsonify(todo_list.display_completed_tasks())


@app.route('/incomplete_tasks')
def incomplete_tasks():
    return jsonify(todo_list.display_incomplete_tasks())


if __name__ == '__main__':
    app.run(debug=True)
