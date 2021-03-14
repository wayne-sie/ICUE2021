from app import app#, db
from flask import render_template
from pymongo import MongoClient
# from app.models import Customers
from flask import request
import datetime



@app.route("/")
@app.route("/index")
def index():
    cluster = MongoClient('mongodb+srv://sanjeev2001:mEm39dShwBgbf2@cluster0.w43vk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = cluster["customer"]
    collection = db["customer"]

    id = request.args['id']
    num = request.args['num']
    # enter = request.args['enter']
    # exit = request.args['exit']
    infected = request.args['infected']
    inStore = request.args['inStore']


    if inStore == True:
        json_customer = {
            '_id' : id,
            'phone_num' : num,
            'enter_time' : datetime.datetime.now(),
            'exit_time' : "", 
            'is_infected' : infected,
            'inStore' : inStore
        }
    else :
        json_customer = {
            '_id' : id,
            'phone_num' : num,
            'enter_time' : "",
            'exit_time' : datetime.datetime.now(), 
            'is_infected' : infected,
            'inStore' : inStore
        }
        

    collection.insert_one(json_customer)
    
    return render_template("index.html", id = id, num = num)#, customers = customers)

    