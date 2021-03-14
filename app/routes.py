from app import app
from flask import render_template, redirect, request
from pymongo import MongoClient
from flask import request
import datetime



@app.route("/")
@app.route("/index")
def index():
    if request.method == 'POST':
        x = str(request.form.getlist('checked'))
        return x
        # return redirect(url_for('messaged'))
    else:
        cluster = MongoClient('mongodb+srv://sanjeev2001:mEm39dShwBgbf2@cluster0.w43vk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
        db = cluster["customer"]
        history = db["history"]
        historyArr = {
            "rfid": [],
            'phone_num' : [],
            'enter_time' : [],
            'exit_time' : [],
            'is_infected' : []
        }
        
        for document in history.find():
            historyArr['rfid'].append(document['rfid'])
            historyArr['phone_num'].append(document['phone_num'])
            historyArr['enter_time'].append(document['enter_time'])
            historyArr['exit_time'].append(document['exit_time'])
            historyArr['is_infected'].append(document['is_infected'])

        return render_template("index.html", historyArr = historyArr, arrLen = len(historyArr['rfid']))

@app.route("/messaged", methods=['GET', 'POST'])
def messaged():
    if request.method == 'POST':
        # account_sid = os.environ['ACc40d883d6878ff32d457ab4c0d38216c']
        # auth_token = os.environ['b3130d8ddd38c115d9cf4990b5468e38']
        # client = Client(account_sid, auth_token)

        rfidOfInfected = str(request.form.getlist('checked'))

        cluster = MongoClient('mongodb+srv://sanjeev2001:mEm39dShwBgbf2@cluster0.w43vk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
        db = cluster["customer"]
        history = db["history"]
        query = {'rfid': rfidOfInfected}
        infectedPerson = history.find_one(query)
        for i in range(len(history['rfid'])):
            historyTime = datetime.datetime.striptime(history['enter_time'], '%d-%m-%y %H:%M:%S')
            infectedTime = datetime.datetime.striptime(infected['enter_time'], '%d-%m-%y %H:%M:%S')
            if historyTime > infectedTime:
                return "True"

    else: 
        return "Error 404 not found"


@app.route("/input")
def input():
    cluster = MongoClient('mongodb+srv://sanjeev2001:mEm39dShwBgbf2@cluster0.w43vk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = cluster["customer"]
    enterCollection = db["customer"]
    history = db["history"]

    rfid = request.args['rfid']
    num = request.args['num']
    infected = request.args['infected']

    dbResponse = enterCollection.find_one({"rfid": rfid})

    if (dbResponse == None) :
        enter_customer = {
            'rfid' : rfid,
            'phone_num' : num,
            'enter_time' : datetime.datetime.now(),
            'is_infected' : False
        }
        enterCollection.insert_one(enter_customer)
    else : 
        json_customer = {
            'rfid' : rfid,
            'phone_num' : num,
            'enter_time' : dbResponse['enter_time'],
            'exit_time' : datetime.datetime.now(),
            'is_infected' : False
        }
        history.insert_one(json_customer)
        enterCollection.delete_one(dbResponse)
    return "success"
    

