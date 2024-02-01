from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import datetime as dt
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, ValidationError


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'any secret string'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    due_date = db.Column(db.Date)

# with app.app_context():
#     db.create_all()
#     new_todo = Todo(
#         name = "Nivi Todo",
#         due_date = dt.datetime.now()
#     )
#     db.session.add(new_todo)
#     db.session.commit()


class ToDoForm(FlaskForm):
    name = StringField('To Do Name', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])
    submit = SubmitField('Done')


@app.route('/')
def index():

    todos = db.session.query(Todo).all()
    return render_template('style.html', todos=todos)


@app.route('/add',methods=['GET','POST'])
def add_todo():
    add_form = ToDoForm()
    if add_form.validate_on_submit():
        new_to_do = Todo(
            name=add_form.name.data,
            due_date=add_form.due_date.data

        )
        db.session.add(new_to_do)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html', add_form=add_form)

@app.route("/edit/<id>",methods=['GET','POST'])
def edit_todo(id):
    todo = db.get_or_404(Todo,id)
    edit_todo = ToDoForm(name = todo.name,
                         due_date = todo.due_date)

    if edit_todo.validate_on_submit():
        todo.name = edit_todo.name.data
        todo.due_date = edit_todo.due_date.data
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html', edit_form=edit_todo, is_edit =True)

@app.route("/delete/<id>",methods=['GET','POST'])
def delete_todo(id):
    delete_todo = db.get_or_404(Todo,id)
    db.session.delete(delete_todo)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)