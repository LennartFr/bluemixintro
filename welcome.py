# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# https://cloudant.com/blog/using-python-with-cloudant/#.V7XWYHrG8WY

import os
from flask import Flask, redirect, jsonify
import urllib  
import datetime  
import json  
import requests
import couchdb  # Loeser

app = Flask(__name__)

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/watson')
def WelcomeToWatson():
    return app.send_static_file('index1.html')
	
@app.route('/iot')
def WelcomeToIoT():
    return app.send_static_file('indexiot.html')
	
@app.route('/innovate')
def WelcomeToInnovate():
    return app.send_static_file('innovate.html')
		
	
###
###
###	
@app.route('/createdb/<db>')
def create_db(db):
    try:
        vcap = json.loads(os.getenv("VCAP_SERVICES"))['cloudantNoSQLDB']

        cl_username = vcap[0]['credentials']['username']
        cl_password = vcap[0]['credentials']['password']

        url         = vcap[0]['credentials']['url']
        auth        = ( cl_username, cl_password )

    except:
        return 'A Cloudant service is not bound to the application.  Please bind a Cloudant service and try again.'

    requests.put( url + '/' + db, auth=auth )
    return 'Database %s created.' % db	
	
	
@app.route('/insertdb/<db>')
def insert_db(db):
    try:
        vcap = json.loads(os.getenv("VCAP_SERVICES"))['cloudantNoSQLDB']

        cl_username = vcap[0]['credentials']['username']
        cl_password = vcap[0]['credentials']['password']

        url         = vcap[0]['credentials']['url']
        auth        = ( cl_username, cl_password )

    except:
        return 'A Cloudant service is not bound to the application.  Please bind a Cloudant service and try again.'

# couchDB/Cloudant-related global variables
    couchInfo=''
    couchServer=''
    couch=''		
	
	#if 'VCAP_SERVICES' in os.environ:
    couchInfo = json.loads(os.environ['VCAP_SERVICES'])['cloudantNoSQLDB'][0]
    couchServer = couchInfo["credentials"]["url"]
    couch = couchdb.Server(couchServer)
		
    db = couch['mindatabas']
	
		
    doc= { "Namn" : "Anna", "City" : "Beijing" }
    db.save(doc)
			
    doc_id, doc_rev = db.save({
        'name': 'Mike Broberg',
        'title': 'Fun Captain',        
    })
	
	#doc = db[doc_id]
			
    #requests.put( url + '/' + doc, auth=auth )
	#requests.post( url + '/' + doc, auth=auth)
	
    return 'Data inserted into %s .' % db		
	
### 
###
###
###	
	
	
###
###
###	
	
	
@app.route('/api/people')
def GetPeople():
    list = [
        {'name': 'John', 'age': 28},
        {'name': 'Bill', 'val': 26}
    ]
    return jsonify(results=list)

@app.route('/api/people/<name>')
def SayHello(name):
    message = {
        'message': 'Hello ' + name
    }
    return jsonify(results=message)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
