#!/usr/bin/python3

# ----
from os import system
system("rm database.sql")

from db import Session, Cache
from db.family import Caretaker, Patient, Family
from db.todo import Todo

def create_db():
    s = Session()

    f = Family()
    s.add(f)
    s.commit()

    c = Caretaker(name = "Maria Jones", password = "1234", img = "https://cdn.discordapp.com/attachments/633037289743712286/640246227778273344/woman1.jpg", family_id = f.id)
    s.add(c)

    c = Caretaker(name = "James Morgan", password = "1234", img = "https://cdn.discordapp.com/attachments/633037289743712286/640246255288844341/man1.jpg", family_id=f.id)
    s.add(c)

    c = Caretaker(name = "Piers Johnson", password = "1234", img = "https://cdn.discordapp.com/attachments/633037289743712286/640246279112359986/man2.jpg", family_id=f.id)
    s.add(c)

    c = Caretaker(name = "Michael Morrison", password = "1234", img = "https://cdn.discordapp.com/attachments/633037289743712286/640245068313395201/testimonial-4.jpg", family_id=f.id)
    s.add(c)

    c = Caretaker(name = "Luigi Martinelli", password = "1234", img = "https://cdn.discordapp.com/attachments/633037289743712286/640245081051234325/testimonial-5.jpg", family_id=f.id)
    s.add(c)

    p = Patient(name = "Bunica lu' trupples", img = "https://cdn.discordapp.com/attachments/633037289743712286/640246191791144980/unknown.png")
    s.add(p)
    
    t = Todo(desc = "Water my pussy at 6", done = False, patient_id = 1, caretaker_id = 1)
    s.add(t)

    t = Todo(desc = "Water my pussy at 6, but again", done = False, patient_id = 1, caretaker_id = 2)
    s.add(t)

    s.commit()

    print (f, c, p)
    print (f.id, c.id, p.id)

create_db()

# ----

# -----------------------------------
# ----------- Import list -----------
# -----------------------------------
import json
import base64
import redislite
import consts

from flask import Flask, request, render_template, jsonify, session, redirect
from flask_cors import CORS

from routes import test, login, back
# -----------------------------------

# -----------------------------------
# -------- Flask parameters ---------
# -----------------------------------
app = Flask(__name__,
        template_folder= consts.proj_path + '/../../frontend/templates',
        static_folder= consts.proj_path + '/../../frontend/static',
        static_url_path= '/static')
cors = CORS(app, resources={r"/*": {"origins": "*"}})

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
@app.route('/home')
@app.route('/home/')
@app.route('/home/index')
def index():
	return render_template('home/index.html', title='Forever Family')

@app.route('/login')
@app.route('/home/login')
def login():
    return render_template('home/login.html', title='Login - Forever Family')


@app.route('/game/memory')
@app.route('/game/memory/')
def memory():
    return render_template('game/memory/index.html', title='Memory - Forever Family')

@app.route('/game/recognizefaces')
@app.route('/game/recognizefaces/')
def recognizefaces():
    return render_template('game/recognizefaces/index.html', title='Recognize faces - Forever Family')
# -----------------------------------

# -----------------------------------
# -------- Flask entrypoint ---------
# -----------------------------------
if __name__ == '__main__':
	app.run(ssl_context=('certificate.pem', 'key.pem'), host='0.0.0.0')
# -----------------------------------
