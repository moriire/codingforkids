from flask import Flask, jsonify, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import os
import json
basedir = os.path.dirname(__file__) 
app = Flask(__name__, static_folder='assets', static_url_path='/assets', template_folder='templates')
ma = Marshmallow(app)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///"+ os.path.join(basedir, "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(1), nullable=False)
    def __init__(self,  question, option_a, option_b, option_c, answer):
        self.question = question
        self.option_a = option_a
        self.option_b = option_b
        self.option_c = option_c
        self.answer = answer

    def __repr__(self):
        return self.question

class ExamSchema(ma.Schema):
    class Meta:
        fields = ("id", "question", "option_a", "option_b", "option_c", "answer")

exams_schema = ExamSchema(many=True)
@app.route("/api", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        exams = Exam.query.all()
        #exams["status"] = 200
        return jsonify(data=exams_schema.dump(exams), status=200)
    
exam_schema = ExamSchema()
@app.route("/remove/<pk>", methods=["GET"])
def delete_exam(pk):
    exams = Exam.query.get_or_404(pk)
    db.session.delete(exams)
    db.session.commit()
    redirect("/")
    
@app.route("/api/<pk>", methods=["GET", "DELETE"])
def apihome(pk):
    if request.method == "GET":
        exams = Exam.query.get_or_404(pk)
        return jsonify(data=exam_schema.dump(exams), status=200)
    if request.method == "DELETE":
        exams = Exam.query.get_or_404(pk)
        db.session.delete(exams)
        db.session.commit()
        return jsonify(data=exam_schema.dump(exams), status=204)
    
@app.route("/dashboard/add", methods=["GET", "POST", ])
def home():
    exam_data = Exam.query.all()
    if request.method=="POST":
        question = request.form.get("question")
        option_a = request.form.get("option_a")
        option_b = request.form.get("option_b")
        option_c = request.form.get("option_c")
        answer = request.form.get("answer")
        data = Exam(question=question, option_a=option_a, option_b=option_b, option_c=option_c, answer=answer)
        db.session.add(data)
        db.session.commit()
    return render_template("index.html", exam_data = exam_data)

@app.route("/dashboard/<pk>/edit", methods=["GET", "POST", "DELETE"])
def edit(pk):
    exam_one = Exam.query.get_or_404(pk)
    if request.method=="DELETE":
        db.session.delete(exam_one)
        

    if request.method=="POST":
        #db.session.delete(exam_one)
        #db.session.commit()
        exam_one.question = request.form.get("question")
        exam_one.option_a = request.form.get("option_a")
        exam_one.option_b = request.form.get("option_b")
        exam_one.option_c = request.form.get("option_c")
        exam_one.answer = request.form.get("answer")

        db.session.commit()
    return render_template("edit.html", exam_one = exam_one)

@app.route("/", methods=["GET", "POST", ])
def app_home():
    # datas = Exam.query.all()
    #rows = exams_schema.dump(datas)
    return render_template("app.html")

@app.route("/dashboard", methods=["GET", "POST", ])
def home_home():
    datas = Exam.query.all()
    #rows = exams_schema.dump(datas)
    return render_template("tables.html", rows = datas)

if __name__ == "__main__":
    app.run(debug=True)