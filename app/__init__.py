# Libs necessárias para utilização dessa api
# Libs required to use this api
# Libs requeridas para usar esta API
# Libs Externas
# Libs External
# Libs externa
from flask import Flask, jsonify, request
import json
import datetime
import base64
import uuid
import os
import math
# Libs Internas
# Libs Internal
# Libs interna
from app import api_classes
from app import api_funcoes
app = Flask(__name__)
from app import FaceMatchMain