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
    e1 = db.Column(db.String(500), default="")
    e2 = db.Column(db.String(500), default="")
    e3 = db.Column(db.String(500), default="")
    e4 = db.Column(db.String(200), default="")
    don = db.Column(db.Integer, default=0)


#new user registration, shit
@app.route("/rodin/create/<email>/<passw>")
def newuser(email,passw):
    user = Users(mail=email, password=passw)
    db.session.add(user)
    db.session.commit()
    return '<h1>New added</h1>'



#index stuff
@app.route("/", methods=["POST","GET"])
def index():
    if request.method=="POST":
        user = request.form["id"]
        password = request.form["pwd"]
        #index check here
        data = Users()
        if(user=="rodinjack@gmail.com" and password=="akigai1@"): #superuser details hardcoded
            session["supes"]=user
            return redirect(url_for("supes"))

        data = Users.query.filter_by(mail=user).first()
        if (data and data.password==password):
            session["user"]=user
            return redirect(url_for("choice"))
        else:
            return render_template("index.html", rem="Incorrect Email or Password")
    else: 
        if "user" in session:
            return redirect(url_for("phase1"))
        return render_template("index.html")

#search content for super user
@app.route("/rodin", methods=["POST","GET"])
def supes():
    if request.method=="POST":
        if request.form["savedirec"]== "search":
            used = request.form["mail"]
            if used:
                data = Users()
                data = Users.query.filter_by(mail=used).first()
                datab = [[data.mail,data.p32,data.e4]]
                content = "<h3>Phase1:</h3><br /><strong>Shit they're passionate about:</strong><br />"+data.p11+"<br>"+"<strong>Shit they're good at:</strong><br />"+data.p12+"<br><strong>Shit they get paid for:</strong><br />"+data.p13+"<br><strong>Shit they care for:</strong><br />"+data.p14+"<br><br>"
                content += "<h3>Phase2:</h3><br /><strong>Passion:</strong><br />"+data.p21+"<br><strong>Mission:</strong><br />"+data.p22+"<br><strong>Vocation:</strong><br />"+data.p23+"<br><strong>Profession:</strong><br />"+data.p24+"<br><br>"      
                content += "<h3>Phase3:</h3><br /><strong>All Options:</strong><br />"+data.p31+"<br><strong>Final Ikigai:</strong><br />"+data.p32+"<br><br>"
                content += "<h3>ECG:</h3><br /><strong>Experience:</strong><br />"+data.e1+"<br><strong>Growth:</strong><br />"+data.e2+"<br><strong>Contribution:</strong><br />"+data.e3+"<br><strong>Top 3 ECG:</strong><br />"+data.e4+"<br>"
                if data:
                    return render_template("supes.html",content=content, lens=1, data=datab)
            else:
                return redirect(url_for("supes"))
        else:
            return redirect(url_for("logout"))
    else:
        if "supes" in session:
            data = Users()
            data = Users.query.all()
            datab = []
            for user in data:
                databi = [user.mail,user.p32,user.e4]
                datab.append(databi)
            return render_template("supes.html",lens=len(datab), data=datab)
        else:
            return(redirect(url_for("index")))
#route choice
@app.route("/choice")
def choice():
    if "user" in session:
        return render_template("choice.html")
    else:
        return redirect(url_for("index"))

#ecg primary
@app.route("/ecg", methods=["POST", "GET"])
def ecg():
    if "user" in session:
        data = Users()
        data = Users.query.filter_by(mail=session["user"]).first()
        if request.method=="POST":
            data.e1=request.form["e1"]
            data.e2=request.form["e2"]
            data.e3=request.form["e3"]
            db.session.commit()
            if request.form["savedirec"]== "phase2":
                return redirect(url_for("topecg"))
            elif request.form["savedirec"]== "ikigai":
                return redirect(url_for("phase1"))
            else:
                return redirect(url_for("logout"))
        else:
            return render_template("ecg.html", pp1=data.e1, pp2=data.e2, pp3=data.e3)
    else:
        return redirect(url_for("index"))

#top ecg entry
@app.route("/topecg", methods=["POST", "GET"])
def topecg():
    if "user" in session:
        data = Users()
        data = Users.query.filter_by(mail=session["user"]).first()
        if request.method=="POST":
            data.e4=request.form["e4"]
            db.session.commit()
            if request.form["savedirec"]== "phase1":
                return redirect(url_for("ecg"))
            elif request.form["savedirec"]== "ikigai":
                return redirect(url_for("phase1"))
            else:
                return redirect(url_for("logout"))
        else:
            return render_template("topecg.html", pp1=data.e4)
    else:
        return redirect(url_for("index"))




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
            if request.form["savedirec"]== "phase2":
                return redirect(url_for("phase2"))
            elif request.form["savedirec"]== "phase3":
                return redirect(url_for("phase3"))
            elif request.form["savedirec"]== "ecg":
                return redirect(url_for("ecg"))
            else:
                return redirect(url_for("logout"))
        else:
            return render_template("phase1.html", pp1=data.p11, pp2=data.p12, pp3=data.p13, pp4=data.p14)
    else:
        return redirect(url_for("index"))


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
            if request.form["savedirec"]== "phase1":
                return redirect(url_for("phase1"))
            elif request.form["savedirec"]== "phase3":
                return redirect(url_for("phase3"))
            elif request.form["savedirec"]== "ecg":
                return redirect(url_for("ecg"))
            else:
                return redirect(url_for("logout"))
        else:
            return render_template("phase2.html", pp1=data.p21, pp2=data.p22, pp3=data.p23, pp4=data.p24)
    else:
        return redirect(url_for("index"))
    

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
            if request.form["savedirec"]== "phase2":
                return redirect(url_for("phase2"))
            elif request.form["savedirec"]== "phase1":
                return redirect(url_for("phase1"))
            elif request.form["savedirec"]== "ecg":
                return redirect(url_for("ecg"))
            else:
                return redirect(url_for("logout"))
        else:
            return render_template("phase3.html", pp1=data.p31, pp2=data.p32)
    else:
        return redirect(url_for("index"))


#indexg out takes you back to index
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
