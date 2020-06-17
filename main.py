from flask import Flask, jsonify, request
import json
import datetime
import base64
import uuid
import os
import math

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