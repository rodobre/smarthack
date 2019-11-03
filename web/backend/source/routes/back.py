from flask import Blueprint, jsonify, request, render_template
from db import Session, Cache
from db.family import Family, Caretaker, Patient
from db.todo import Todo
from db.stats import Stats
from base64 import b64encode, b64decode
import json
backend = Blueprint('back', __name__)
api_path = '/api/'

import qrcode
import io

import string
import random

def random_key(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


@backend.route('/dashboard')
def dashboard():
    return render_template('dashboard/index.html', title='Dashboard')

# ############# CARETAKER ROUTES ################## #
# GET_QR - POST
# SEND:
# RECV: caretaker_qr
@backend.route(api_path + 'get_qr', methods=['POST'])
def get_qr():
    if not is_auth(request.headers):
        return 'not authenticated', 401

    data = request.json
    session = Session()
    u = Patient(name = data['name'], img = data['img'], family_id = Cache[request.headers["Token"]]["family_id"])
    session.add(u)
    session.commit()

    family_id = str(Cache[request.headers["Token"]]["family_id"])
    img = qrcode.make(family_id + "#" + str(u.id))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()

    fn = random_key(64) + ".png"
    with open(fn, 'wb') as f:
        f.write(img_bytes)

    return jsonify({"qr":fn})

# ADD_FAMILY_MEMBER - POST
# SEND: family_id, name, description, image (B64)
# RECV: NOTHING
# USELESS
@backend.route(api_path + 'add_family_member', methods=['POST'])
def add_family_member():
    data = request.json

    if not is_auth(request.headers):
        return 'not authenticated', 401

    family_id = None
    name = None
    description = None
    image = None

    try:
        family_id = data['family_id']
        name = data['name']
        description = data['description']
        image = data['image']
    except:
        return 'invalid parameters', 400


    c = Caretaker(name = name,desc=description,img=image)
    s = Session()
    s.add(c)
    s.commit()
    return 'OK'

# ADD_PATIENT - POST
# SEND: family_id, name, description, image (B64)
# RECV: NOTHING
@backend.route(api_path + 'add_patient', methods=['POST'])
def add_patient():
    data = request.json

    if not is_auth(request.headers):
        return 'not authenticated', 401

    family_id = None
    name = None
    description = None
    image = None

    try:
        family_id = Cache[request.headers['Token']]['family_id']
        name = data['name']
        description = data['description']
        image = data['image']
    except:
        return 'invalid parameters', 400

    p = Patient(name=name,desc=description,img=image,family_id=family_id)
    s = Session()
    s.add(p)
    s.commit()
    return 'OK'

# ADD_TODO - POST
# SEND: family_id, patient_id, todo
# RECV: NOTHING
@backend.route(api_path + 'add_todo', methods=['POST'])
def add_todo():
    data = request.json

    if not is_auth(request.headers):
        return 'not authenticated', 401

    family_id = None
    patient_id = None
    todo = None

    try:
        family_id = Cache[request.headers['Token']]['family_id']
        patient_id = data['patient_id']
        todo = data['todo']
    except:
        return 'invalid parameters', 400

    t = Todo(desc=todo,done=False,patient_id=patient_id,caretaker_id=Cache[request.headers['Token']]['id'])
    s = Session()
    s.add(t)
    s.commit()
    return 'OK'

# SEND_STATS - POST
# SEND: time (INT), moves (INT), answers_right (INT), answers_wrong (INT), patient_id (INT)
# RECV: NOTHING
@backend.route(api_path + 'send_stats', methods=['POST'])
def send_stats():
    data = request.json

    if not is_auth(request.headers):
        return 'not authenticated', 401

    patient_id = None
    time = None
    moves = None
    answers_right = None
    answers_wrong = None

    try:
        time = data['time']
        answers_right = data['answers_right']
        answers_wrong = data['answers_wrong']
        patient_id = Cache[request.headers['Token']]['id']
    except:
        return 'invalid parameters', 400

    t = Stats(time=time,answers_wrong=answers_wrong,answers_right=answers_right,patient_id=patient_id)
    s = Session()
    s.add(t)
    s.commit()
    return 'OK'

@backend.route(api_path + 'get_stats', methods=['GET'])
def get_stats():
    data = request.json

    if not is_auth(request.headers):
        return 'not authenticated', 401

    patient_id = None

    try:
        patient_id = data['patient_id']
    except:
        return 'invalid parameters', 400

    s = Session()
    r = s.query(Stats).filter_by(patient_id=patient_id).first()
    return str(repr(r))

# VIEW_MEMBERS - GET
# SEND: family_id
# RECV: names, images
@backend.route(api_path + 'view_members', methods=['GET'])
def view_members():
    data = request.json
    if not is_auth(request.headers):
       return 'not authenticated', 401

    s = Session()
    family_id = Cache[request.headers['Token']]['family_id']
    r = s.query(Caretaker).filter_by(family_id=family_id).all()
    print('Family id', family_id)
    print(repr(r))
    persons = []
    for p in r:
        print(p)
        persons += [{'name':p.name,'img':p.img,'desc':p.desc}]
    print(persons)
    return str(json.dumps(persons))

# VIEW_PATIENTS - GET
# SEND: family_id
# RECV: names, descriptions, images
@backend.route(api_path + 'view_patients', methods=['GET'])
def view_patients():
    data = request.json

    if not is_auth(request.headers):
        return 'not authenticated', 401

    family_id = None

    try:
        family_id = Cache[request.headers['Token']]['family_id']
    except:
        return 'invalid parameters', 400

    s = Session()
    r = s.query(Patient).filter_by(family_id=family_id).all()
    return repr(r)

# VIEW_PATIENT - GET
# SEND: family_id, patient_id
# RECV: name, description, image
@backend.route(api_path + 'view_patient', methods=['GET'])
def view_patient():
    data = request.json

    if not is_auth(request.headers):
        return 'not authenticated', 401

    family_id = None
    patient_id = None

    try:
        family_id = Cache[request.headers['Token']]['family_id']
        patient_id = data['patient_id']
    except:
        return 'invalid parameters', 400

    s = Session()
    r = s.query(Patient).filter_by(family_id=family_id, id=patient_id).first()
    return str(r)

# VIEW_TODO - GET
# SEND: family_id, patient_id
# RECV: todo list as json array
@backend.route(api_path + 'view_todo', methods=['GET'])
def view_todo():
    data = request.json

    print ( Cache[request.headers['Token']])
    if not is_auth(request.headers):
        return 'not authenticated', 401

    family_id = None
    patient_id = None

    #try:
    family_id = Cache[request.headers['Token']]['family_id']

    if Cache[request.headers['Token']]['type'] == 0:
        patient_id = Cache[request.headers['Token']]['id']
    else:
        patient_id = data['patient_id']
    #except Exception as e:
    #    print (e)
    #    return 'invalid parameters', 400

    s = Session()
    r = s.query(Todo).filter_by(patient_id=patient_id, done=False).all()
    data = []
    for e in r:
        data.append(
                {
                    "desc":e.desc,
                    "name":e.caretaker.name,
                    "img":e.caretaker.img,
                    }
                )

    return jsonify(data)

def is_auth(header):
    if header['Token'] in Cache:
        return True
    return False
