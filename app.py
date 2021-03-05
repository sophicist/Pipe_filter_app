from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
from Model import Iterable
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


app = Flask(__name__)


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

db = SQLAlchemy(app)
con = db.engine.connect().connection
df = pd.read_sql_query("select * from User", con)
print(df.head())

# add the data as an iterator class
iterable = Iterable([df])

# get the next data in the pipe and clean it
data = iterable.next()
clean_data = data[["age", "marks", "gender"]]
iterable.add(clean_data)

# visualize the data

data = iterable.next()

plt.figure()
fig = sns.scatterplot(data=data, x="age", y="marks", hue="gender")
plt.title("Scatter Plot")
#plt.title("Marks Vs Age scatter plot")
fig = fig.get_figure()
fig.savefig("static/edge.png")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    gender = db.Column(db.String)
    age = db.Column(db.Integer)
    marks = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.now())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/collect", methods=["POST", "GET"])
def collect():
    data = request.form

    user = User(
        name=data["name"],
        email=data["email"],
        gender=data["gender"],
        age=data["age"],
        marks=data["marks"],
    )

    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.route("/results")
def results():
    users = User.query.order_by(User.created).all()

    print(users)
    return render_template("results.html", users=users)


if __name__ == "__main__":
    app.run(port="5000", debug=True, use_reloader=True)
