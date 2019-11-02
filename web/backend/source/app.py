#!/usr/bin/python3

# -----------------------------------
# ----------- Import list -----------
# -----------------------------------
import json
import base64
import redislite
import consts

from flask import Flask, request, render_template, jsonify, session, redirect

from routes import test, login, back
# -----------------------------------

# -----------------------------------
# -------- Flask parameters ---------
# -----------------------------------
app = Flask(__name__,
        template_folder= consts.proj_path + '/../../frontend/templates',
        static_folder= consts.proj_path + '/../../frontend/static',
        static_url_path= '/static')

# -----------------------------------

# -----------------------------------
# ---------   Blueprints   ----------
# -----------------------------------
app.register_blueprint(test.test_blueprint, url_prefix = '/test')
app.register_blueprint(login.login_blueprint, url_prefix = '/api')
app.register_blueprint(back.backend)
# -----------------------------------

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

