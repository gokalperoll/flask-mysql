from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# ADD SECRET KEY
app.config['SECRET_KEY'] = "supersecretkey"
# ADD DATABASE
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# NEW MYSQL DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/flask_db'
db = SQLAlchemy(app)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    title = "Update Page"
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User updated successfuly ! ")
            return render_template("update.html", form=form, name_to_update=name_to_update, title=title)
        except:
            flash("Error ! try again. ")
            return render_template("update.html", form=form, name_to_update=name_to_update, title=title)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update, title=title)


def create_app():
    app = Flask(__name__)

    with app.app_context():
        db.create_all()

    return app


# CREATE DB MODEL

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_add2 = db.Column(db.DateTime, default=datetime.utcnow)

    # CREATE A STRING
    def __repr__(self):
        return '<Name> %r' % self.name


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/')
def index():
    title = "Main Page"
    return render_template("index.html", title=title)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    title = "Add User"
    form = UserForm()
    name = None
    if form.validate_on_submit():
        user = Users(name=form.name.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash("User added succseffuly")
    our_users = Users.query.order_by(Users.date_add2)
    return render_template('add_user.html', form=form, title=title, name=name, our_users=our_users)


@app.route('/user/delete', methods=['GET', 'POST'])
def delete_user():
    title = "Delete User"
    form = UserForm()
    name = None
    if form.validate_on_submit():
        user = Users.query.filter_by(name=form.name.data).first()
        db.session.delete(user)
        db.session.commit()
        flash("User delete succseffuly")
    our_users = Users.query.order_by()
    return render_template('delete_user.html', form=form, title=title, our_users=our_users)


if __name__ == '__main__':
    app.run(debug=True, port=1337)
