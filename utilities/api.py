from flask import Flask, request, jsonify

app = Flask(__name__)

def new_endpoint(endpoint, func):
    app.add_url_rule(endpoint, view_func=func, methods=["GET"])

def start():
    app.run(port=8000)