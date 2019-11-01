#!/usr/bin/python3

# -----------------------------------
# ----------- Import list -----------
# -----------------------------------
import json
import base64
import redislite
import consts

from flask import Flask, request, send_from_directory, render_template, jsonify, session, redirect
from db import DBInterface
from redis_collections import Dict
# -----------------------------------

# -----------------------------------
# -------- Flask parameters ---------
# -----------------------------------
app = Flask(__name__, template_folder='../../frontend/templates')
# -----------------------------------

# -----------------------------------
# --------- DB credentials ----------
# -----------------------------------
db = DBInterface('localhost', 'test', 'test', 'test')
# -----------------------------------

# -----------------------------------
# --------- Static delivery ---------
# -----------------------------------
@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory('../../frontend/css', path)

@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory('../../frontend/js', path)

@app.route('/img/<path:path>')
def send_img(path):
	return send_from_directory('../../frontend/img', path)
# -----------------------------------
# --------- Routes go here ----------
# -----------------------------------
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title=consts.page_title)
# -----------------------------------
# -----------------------------------
# -------- Flask entrypoint ---------
# -----------------------------------
if __name__ == '__main__':
	app.run(host='0.0.0.0')
# -----------------------------------
