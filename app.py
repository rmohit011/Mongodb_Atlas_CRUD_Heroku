from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
def homePage():
    return render_template("index.html")

#
# @app.route('/docker',methods=['GET'])
# def check_on_docker():
#     return jsonify("Running fine on docker")

@app.route('/find/key/postman', methods=['POST']) # for calling the API from Postman/SOAPUI
def find_in_db_by_key_postman():
    if (request.method=='POST'):
        conn = MongoClient("localhost:27017")
        print("Connection Successful")
        db = conn["csv_bunch"]
        collection=request.json['collection']
        key=request.json['key']
        col=db[collection]
        cursor = col.find()
        for record in cursor:
            if key in list(record.keys()):
                return jsonify(record[key])

@app.route('/find/key', methods=['POST'])
def find_in_db_by_key():
    if (request.method=='POST'):
        conn = MongoClient("localhost:27017")
        print("Connection Successful")
        db = conn["csv_bunch"]
        collection=request.form['collection']
        key=request.form['key']
        col=db[collection]
        cursor = col.find()
        for record in cursor:
            if key in list(record.keys()):
                return render_template("results.html",prediction=record[key])
             #   return jsonify(record[key])


@app.route('/find/query', methods=['POST'])
def find_in_db_by_query():
    if (request.method=='POST'):
        conn = MongoClient("localhost:27017")
        print("Connection Successful")
        db = conn["csv_bunch"]
        collection=request.form['collection']
        element=request.form['element']
        value=request.form['value']
        query={element:value}
        col=db[collection]
        cursor = col.find(query)
        records=[]
        for record in cursor:
            record.pop("_id")
            records.append(record)
        return render_template("results.html",prediction=str(records))
      #  return jsonify(str(records))

@app.route('/delete/key', methods=['POST'])
def delete_in_db_by_key():
    if (request.method=='POST'):
        conn = MongoClient("localhost:27017")
        print("Connection Successful")
        db = conn["csv_bunch"]
        collection = request.form['collection']
        key = request.form['key']
        col = db[collection]
        cursor = col.find()
        for record in cursor:
            if key in list(record.keys()):
                entry=record[key]
                break
        print(entry)
        myquery = {key: entry}
        col.delete_many(myquery)
        return render_template("results.html", prediction="Record deleted for {} key in {} collection".format(key,collection))
        #return jsonify("Record deleted for {} key in {} collection".format(key,collection))

@app.route('/delete/query', methods=['POST'])
def delete_in_db_by_query():
    if (request.method=='POST'):
        conn = MongoClient("localhost:27017")
        print("Connection Successful")
        db = conn["csv_bunch"]
        collection = request.form['collection']
        element = request.form['element']
        value = request.form['value']
        query = {element: value}
        col = db[collection]
        col.delete_many(query)
        return render_template("results.html",prediction="Record deleted having {} as {} in {} collection".format(element,value,collection))
      #  return jsonify("Record deleted having {} as {} in {} collection".format(element,value,collection))

@app.route('/insert/one', methods=['POST'])
def insert_one_in_db():
    if (request.method=='POST'):
        conn = MongoClient("localhost:27017")
        print("Connection Successful")
        db = conn["csv_bunch"]
        collection = request.form["collection"]
        dic = request.form["dic"]
        res = json.loads(dic)
        col = db[collection]
        id1 = col.insert_one(res)
        return render_template("results.html",prediction="Record inserted in {} collection".format(collection))
     #   return jsonify("Record inserted in {} collection with id {}".format(col,id1))

@app.route('/insert/many', methods=['POST'])
def insert_many_in_db():
    if (request.method=='POST'):
        conn = MongoClient("localhost:27017")
        print("Connection Successful")
        db = conn["csv_bunch"]
        collection = request.form["collection"]
        list_of_dic = request.form["list_of_dic"]
        res = json.loads(list_of_dic)
        col = db[collection]
        id1 = col.insert_many(res)
        return render_template("results.html",prediction="Record inserted in {} collection".format(collection))



if __name__ == '__main__':
    app.run()
    #app.run(host="0.0.0.0")