
from flask import Flask, jsonify, request
        
app = Flask(__name__)

@app.route("/", methods=['GET'])
def getsimples():	
	return "Api FaceMatch - {}".format(datetime.datetime.now())

def getsimples2():	
	return "HELLO WORLD")
    
