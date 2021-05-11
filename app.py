# import libraries for the app to run and connect to a database
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import aliased
from sqlalchemy import func
from send_email import send_email

# instantiate flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres1234@localhost/height_collector'
#app.config['SQLALCHEMY_DATABASE_URI']='postgres://ldeopiqriuoupi:b89ff5aa095c7de1be179df408daa2322892a55913343d9ea911bfc7c05079d4@ec2-52-0-114-209.compute-1.amazonaws.com:5432/dj0u6kcqgvhfi'
db = SQLAlchemy(app)

# create a class for creating a database
class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_=email_
        self.height_=height_

# homepage
@app.route("/")
def index():
    return render_template("index.html")

# page for when someone has logged in succesfully
@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        email=request.form["email_name"]
        height=request.form["height_name"]
        # if/else statement to check if user is already in database
        if db.session.query(Data).filter(Data.email_==email).count() ==0:  
            data=Data(email, height)
            db.session.add(data)
            db.session.commit()
            average_height = db.session.query(func.avg(Data.height_)).scalar()
            average_height = round(average_height, 1)
            count = db.session.query(Data.height_).count()
            send_email(email, height, average_height, count)
            return render_template("success.html")
        return render_template("index.html",
         text="Seems like we've got something from that email address already!")
    return render_template("index.html")

if __name__ == '__main__':
    app.debug=True
    app.run()