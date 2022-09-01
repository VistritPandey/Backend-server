from flask import Flask, jsonify, request
import json
from flask_cors import CORS
import pymongo
  
connection_url = 'put your id'
app = Flask(__name__)
client = pymongo.MongoClient(connection_url)

# Database
Database = client.get_database('Backend')
# Table
backend = Database.backend


@app.route('/', methods=['GET'])
def initial():

    return "What's up bitches...??!!!"
# To insert a single document into the database,
# insert_one() function is used
@app.route('/insert-one/<email>/', methods=['GET'])
def insertOne(email):
    queryObject = {
        'email': email,
        'currency': 1000,
        'Phillies': {'cardLocked': True}
    }
    query = backend.insert_one(queryObject)
    return "Query inserted...!!!"
  
# # To find the first document that matches a defined query,
# # find_one function is used and the query to match is passed
# # as an argument.
@app.route('/find-one/<email>/<value>/', methods=['GET'])
def findOne(email, value):
    queryObject = {email: value}
    query = backend.find_one(queryObject)
    obj=query['Phillies']
    print(json.dumps({"card":obj['cardLocked']}))
    return json.dumps({"card":obj['cardLocked']})

@app.route('/cardUnlock/<email>/<TeamName>/', methods=['GET','POST'])
def unlock(email, TeamName):
    queryObject = {'email': email}
    query = backend.find_one(queryObject)
    obj=query[TeamName]
    obj['cardLocked']=False
    updateObject = {TeamName: obj}
    query = backend.update_one(queryObject, {'$set': updateObject})
    if query.acknowledged:
        return "Update Successful"
    else:
        return "Update Unsuccessful"
    

@app.route('/enoughCurrency/<email>/<emailAddress>/<amount>/', methods=['GET'])
def checkCurrency(email, emailAddress,amount):
    queryObject = {email: emailAddress}
    query = backend.find_one(queryObject)
    obj=query['currency']
    if obj>=int(amount):
        return json.dumps({"curr":True})
    else:
        return json.dumps({"curr":False})
  
# # To update a document in a collection, update_one()
# # function is used. The queryObject to find the document is passed as
# # the first argument, the corresponding updateObject is passed as the
# # second argument under the '$set' index.

@app.route('/updateCurrency/<email>/<emailAddress>/<currencyDeducted>/', methods=['GET'])
def setCurrency(email,emailAddress,currencyDeducted):
    queryObject = {email: emailAddress}
    query = backend.find_one(queryObject)
    obj=query['currency']
    updateValue = obj + int(currencyDeducted)
    updateObject = {'currency': updateValue}
    query = backend.update_one(queryObject, {'$set': updateObject})
    if query.acknowledged:
        return "Update Successful"
    else:
        return "Update Unsuccessful"

@app.route('/getCurrency/<email>/<emailAddress>/', methods=['GET'])
def getCurrency(email,emailAddress):
    queryObject = {email: emailAddress}
    query = backend.find_one(queryObject)
    obj=query['currency']
    return json.dumps({"int":obj})
  
if __name__ == '__main__':
    app.run(debug=True)
