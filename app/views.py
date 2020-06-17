from app import app
from flask import Flask, jsonify, request
import json
import datetime
import base64
import uuid
import os
import math

@app.route('/')
def home():
   return "hello world!"