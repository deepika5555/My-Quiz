from flask import Flask,request,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from datetime import datetime
import re
import base64
import first
import requests
import json
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI']= os.environ.get('DATABASE_URL','sqlite:////var/www/html/likiproject/project/WT_data.db')
db=SQLAlchemy(app)
uniqueNumber=2000000
class Login(db.Model):
    userName=db.Column(db.String(100),primary_key=True)
    password=db.Column(db.String(100))
    emailId=db.Column(db.String(100))
    phone=db.Column(db.String(100))
    dob=db.Column(db.String(100))
class QuizData(db.Model):
	number=db.Column(db.String(100),primary_key=True)
	quizTopic=db.Column(db.String(100))
	date=db.Column(db.String(50))
	startTime=db.Column(db.String(10))
	timeZone=db.Column(db.String(100))
	automaticStart=db.Column(db.String(10))	#yes or no
	answerTime=db.Column(db.String(10))		#yes or no
	reviewTime=db.Column(db.String(10))		#yes or no
	awardWinners=db.Column(db.String(10))	#yes or no
	username=db.Column(db.String(100),primary_key=True)
class Questions(db.Model):
	number=db.Column(db.String(100))
	questionId=db.Column(db.String(20),primary_key=True)
	question=db.Column(db.String(200))
	correctAnswers=db.Column(db.String(100))
class Answers(db.Model):
	answerId=db.Column(db.String(20),primary_key=True)
	questionId=db.Column(db.String(20))
	answer=db.Column(db.String(100))
class Results(db.Model):
    marksScored=db.Column(db.Integer)
    totalMarks=db.Column(db.Integer)
    number=db.Column(db.String(100),primary_key=True)
    username=db.Column(db.String(100),primary_key=True)

@app.route('/api/user/number',methods=['GET'])
def GetUserNumbers(): 
    try:
        data=request.args["username"]
    except:
        return jsonify({"msg":"enter properly"}),400
    quizzes=QuizData.query.filter_by(username=data).order_by(QuizData.date.desc()).all()
    q={}
    for quiz in quizzes:
        q[quiz.number]=[quiz.date,quiz.startTime]
    if len(q)==0:
        return jsonify({"msg":"No Quiz registerd"}),403
    return jsonify(q),200
@app.route('/api/user',methods=['GET'])
def GetUserDetails():
    try:
        data=request.args["username"]
    except:
        return jsonify({"msg":"enter properly"}),400
    user=Login.query.filter_by(userName=data).first()
    if user:
        return jsonify({"username":user.userName,"emailId":user.emailId,"phone":user.phone,"dob":user.dob}),200
    else:
        return jsonify({"msg":"invalid"}),403
     
@app.route('/api/user',methods=['POST'])
def UserDetails():
    try:
        data=request.get_json()
    except:
        return jsonify({"msg":"enter properly"}),400
    login=Login(userName=data['username'],password=data['password'],emailId=data['emailId'],dob=data['dob'],phone=data['phone']);
    db.session.add(login);
    db.session.commit();
    return jsonify({"msg":"user details created"}),201

@app.route('/api/quiz/file',methods=['POST'])
def FIleUpload():
    try:
        data=request.get_json()
    except:
        return jsonify({"msg":"enter properly"}),400
    file=data['number']+'.'+data["file_type"]
    img_64_d=base64.decodebytes(data['base64_str'].encode())
    img=open(file,"wb")
    img.write(img_64_d)
    img.close()
    dic=first.tika_function(file)
    print(dic)
    dic['number']=data["number"]
    resp=requests.post('http://127.0.0.1:5000'+'/api/quiz/questions',json=dic)
    return jsonify(resp.json()),resp.status_code



@app.route('/api/quiz/results',methods=['POST'])
def GetResults():
    try:
        data=request.get_json()
    except:
        return jsonify({"msg":"enter properly"}),400
    n=len(data)
    print(data)
    questions=Questions.query.filter_by(number=data[str(n-1)]).all()
    index=1
    scored=0
    total=0
    order=[]
    for question in questions:
        answer=question.correctAnswers.split(";");
        score=1
        if len(answer)-1==len(data[str(index)]):
            for i in range(len(answer)-1):
                if answer[i] not in data[str(index)]:
                    score=0
        else:
            score=0
        order.append(score)
        index+=1
        scored+=score
        total+=1
    marks=Results(marksScored=scored,totalMarks=total,username=data[str(n)],number=data[str(n-1)])
    db.session.add(marks)
    db.session.commit()
    return jsonify({"scored":scored,"total":total,"order":order}),200

@app.route('/api/quiz/time',methods=['GET'])
def GetTime():
    try:
        data=request.args["number"]
    except:
        return jsonify({"msg":"enter properly"}),400
    details=QuizData.query.filter_by(number=data).first()
    print(details.startTime)
    question_count=Questions.query.filter_by(number=data).count()
    if details.startTime=="NULL":
        return jsonify({"msg":"quizzes","quesCount":question_count,"quizTopic":details.quizTopic,"answerTime":details.answerTime,"reviewTime":details.reviewTime}),201
    return jsonify({"date":details.date,"quesCount":question_count,"startTime":details.startTime,"quizTopic":details.quizTopic,"answerTime":details.answerTime,"reviewTime":details.reviewTime}),200

@app.route('/api/quiz/details',methods=['POST'])
def PostQuizDetails():
    fp=open("number.txt","r+")
    uniqueNumber=fp.read()
    data=request.get_json()
    print(data)
    try:
        data["quizTopic"]
        data["date"]
        data["startTime"]
        data["timeZone"]
        data["username"]
        data["automaticStart"]
        data["answerTime"]
        data["reviewTime"]
        data["awardWinners"]
    except :
        return jsonify({"msg":"not proper"}),400

    Quiz=QuizData(number=uniqueNumber,quizTopic=data["quizTopic"],date=data['date'],startTime=data["startTime"],timeZone=data["timeZone"],automaticStart=data["automaticStart"],answerTime=data["answerTime"],reviewTime=data["reviewTime"],awardWinners=data["awardWinners"],username=data["username"])
    db.session.add(Quiz)
    db.session.commit()
    uniqueNumber=int(uniqueNumber)
    uniqueNumber+=1
    fp=open("number.txt","w")
    fp.write(str(uniqueNumber))
    fp.close()
    return jsonify({"number":uniqueNumber-1}),201

@app.route('/api/user/validate',methods=['POST'])
def ValidateUser():
    data=request.get_json()
    try:
        data["username"]
        data["password"]
    except:
        return  jsonify({'enter':'properly'}),400
    user=Login.query.filter_by(userName=data["username"]).first();
    if user:
    	if user.password==data["password"]:
    		quiz=QuizData.query.filter_by(username=user.userName).first()
    		if quiz:
    			return jsonify({"number":quiz.number}),200
    		return jsonify({"number":0}),200
    	else:
    		return jsonify({"msg":"Password Do not match"}),403
    else:
    	return jsonify({"msg":"No User Name Found"}),405


@app.route('/api/quiz/questions',methods=['POST'])
def AddQuestionsAndAnswers():
    data=request.get_json()
    try:
        data["answers"]
        data["questions"]
        data["number"]
    except:
        return  jsonify({'enter':'properly'}),400
    q=1
    index=0
    for question in data["questions"]:
    	question_id=str(data["number"])+"q"+str(q)
    	q+=1
    	correct=len(data["answers"][index])-1
    	ques=Questions(questionId=question_id,correctAnswers=data["answers"][index][correct],question=question,number=data["number"])
    	db.session.add(ques)
    	db.session.commit()
    	a=1
    	for an in range(correct):
    		answer_id=question_id+"a"+str(a)
    		a+=1
    		ans=Answers(questionId=question_id,answerId=answer_id,answer=data["answers"][index][an])
	    	db.session.add(ans)
	    	db.session.commit()
    	index+=1
    return jsonify({"msg":"Successfully Added"}),201

@app.route('/api/quiz/questions/review',methods=['GET'])
def GetQuestionsAndAnswersForReview():
    try:
        data=request.args["number"]
        data1=request.args["username"]
    except:
        return jsonify({"msg":"enter properly"}),400
    ques=[]
    ans=[]
    questions=Questions.query.filter_by(number=data).all()
    if questions:
        for  question in questions:
            ques.append([question.question,question.correctAnswers])
            answers=Answers.query.filter_by(questionId=question.questionId).all()
            opt=[]
            for answer in answers:
                opt.append(answer.answer)
            ans.append(opt)
        quiz=QuizData.query.filter_by(number=data).first()
        print(ans)
        return jsonify({"questions":ques,"answers":ans,"answerTime":quiz.answerTime,"reviewTime":quiz.reviewTime}),200
    return jsonify({"msg":"No Quiz Found!!!!"}),400

@app.route('/api/quiz/questions',methods=['GET'])
def GetQuestionsAndAnswers():
    try:
        data=request.args["number"]
        data1=request.args["username"]
    except:
        return jsonify({"msg":"enter properly"}),400
    res=Results.query.filter_by(number=data,username=data1).first()
    if res:
        return jsonify({"msg":"null"}),403
    ques=[]
    ans=[]
    questions=Questions.query.filter_by(number=data).all()
    if questions:
        for  question in questions:
            ques.append([question.question,question.correctAnswers])
            answers=Answers.query.filter_by(questionId=question.questionId).all()
            opt=[]
            for answer in answers:
                opt.append(answer.answer)
            ans.append(opt)
        quiz=QuizData.query.filter_by(number=data).first()
        print(ans)
        return jsonify({"questions":ques,"answers":ans,"answerTime":quiz.answerTime,"reviewTime":quiz.reviewTime}),200
    return jsonify({"msg":"No Quiz Found!!!!"}),400

@app.route('/api/quiz/check',methods=['GET'])
def CheckNumber():
    try:
        data=request.args["number"]
    except:
        return jsonify({"msg":"enter properly"}),400
    quiz=QuizData.query.filter_by(number=data).first()
    if quiz:
        return jsonify({"msg":"Exists"}),200
    return jsonify({"msg":"Does Not Exists"}),403
    
if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True)
