from flask import Flask, jsonify, request
import json
import datetime
import base64
import uuid
import os
import math
import api_classes
import api_funcoes

app = Flask(__name__)

@app.route('/')
def home():
	return "hello world!"

@app.route('/a')
def a():
	return "Func A Funcionou"

@app.route('/a/b')
def ab():
	return "Func A/B Funcionou"

if __name__ == '__main__':
	print ('API_FACEMATCH INICIADA')
	app.run(host='127.0.0.1', port=6068)