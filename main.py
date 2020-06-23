from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)


@app.route("/1", methods=['GET'])
def getsimples1():
	return "hello world 1"
    
@app.route("/2", methods=['GET'])
def getsimples2():
	return "<!DOCTYPE html><html><body><h2>Wagnao Voando</h2></body></html>"
    
@app.route("/", methods=['GET'])
def getsimples():
	return "Api FaceMatch - {}".format(datetime.datetime.now())