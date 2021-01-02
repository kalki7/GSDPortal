from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key= "AkilaHariSittingAtBoardRoom"

db = SQLAlchemy(app)

class Users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(25))
    datecreated = db.Column(db.DateTime, default=datetime.now)
    p11 = db.Column(db.String(200), default="")
    p12 = db.Column(db.String(200), default="")
    p13 = db.Column(db.String(200), default="")
    p14 = db.Column(db.String(200), default="")
    p21 = db.Column(db.String(200), default="")
    p22 = db.Column(db.String(200), default="")
    p23 = db.Column(db.String(200), default="")
    p24 = db.Column(db.String(200), default="")
    p31 = db.Column(db.String(200), default="")
    p32 = db.Column(db.String(200), default="")
    don = db.Column(db.Integer, default=0)


#new user registration, shit
@app.route("/rodin/<email>/<passw>")
def newuser(email,passw):
    user = Users(mail=email, password=passw)
    db.session.add(user)
    db.session.commit()
    return '<h1>New added</h1>'



#login stuff
@app.route("/", methods=["POST","GET"])
def login():
    if request.method=="POST":
        user = request.form["id"]
        password = request.form["pwd"]
        #login check here
        data = Users()
        data = Users.query.filter_by(mail=user).first()
        if (data and data.password==password):
            session["user"]=user
            return redirect(url_for("phase1"))
        else:
            return render_template("login.html", rem="Invalid Email ID or Password. Please contact Aki")
    else: 
        if "user" in session:
            return redirect(url_for("phase1"))
        return render_template("login.html")



#phase 1 stuff
@app.route("/phase1", methods=["POST", "GET"])
def phase1():
    if "user" in session:
        data = Users()
        data = Users.query.filter_by(mail=session["user"]).first()
        if request.method=="POST":
            data.p11=request.form["p11"]
            data.p12=request.form["p12"]
            data.p13=request.form["p13"]
            data.p14=request.form["p14"]
            db.session.commit()
            return redirect(url_for("phase2"))
        else:
            return render_template("phase1.html", pp1=data.p11, pp2=data.p12, pp3=data.p13, pp4=data.p14)
    else:
        return redirect(url_for("login"))


#phase 2 stuff
@app.route("/phase2", methods=["POST", "GET"])
def phase2():
    if "user" in session:
        data = Users()
        data = Users.query.filter_by(mail=session["user"]).first()
        if request.method=="POST":
            data.p21=request.form["p21"]
            data.p22=request.form["p22"]
            data.p23=request.form["p23"]
            data.p24=request.form["p24"]
            db.session.commit()
            return redirect(url_for("phase3"))
        else:
            return render_template("phase2.html", pp1=data.p21, pp2=data.p22, pp3=data.p23, pp4=data.p24)
    else:
        return redirect(url_for("login"))
    

#phase3 stuff
@app.route("/phase3", methods=["POST", "GET"])
def phase3():
    if "user" in session:
        data = Users()
        data = Users.query.filter_by(mail=session["user"]).first()
        if request.method=="POST":
            data.p31=request.form["p31"]
            data.p32=request.form["p32"]
            db.session.commit()
            return redirect(url_for("logout"))
        else:
            return render_template("phase3.html", pp1=data.p31, pp2=data.p32)
    else:
        return redirect(url_for("login"))


#loging out takes you back to login
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
