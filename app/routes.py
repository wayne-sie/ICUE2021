from app import app
from flask import render_template, redirect
from pymongo import MongoClient
from flask import request
import datetime



@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('messaged'))
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

# @app.route("/messaged")
# def messaged():

#     cluster = MongoClient('mongodb+srv://sanjeev2001:mEm39dShwBgbf2@cluster0.w43vk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
#     history = db["history"]
#     query = {'rfid': ""}
#     infectedPerson = history.find_one()
#     for i in range(len(history['rfid'])):
#         if history['enter_time'] < 


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
    

