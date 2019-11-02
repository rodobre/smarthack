from flask import Blueprint, jsonify, request
from db import Session, Cache
from base64 import b64encode, b64decode

backend = Blueprint('back', __name__)
api_path = '/api/'

# ############# CARETAKER ROUTES ################## #
# CREATE_FAMILY - POST
# SEND: name
# RECV: caretaker_qr, patient_qr, family_id
@backend.route(api_path + 'create_family', methods=['POST'])
def create_family():
	data = request.json

	name = None
	try:
		name = data['name']
	except:
		return 'invalid parameters', 400

	return 'A'

# ADD_FAMILY_MEMBER - POST
# SEND: family_id, name, description, image (B64)
# RECV: NOTHING
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


	return 'A'

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
		family_id = data['family_id']
		name = data['name']
		description = data['description']
		image = data['image']
	except:
		return 'invalid parameters', 400

	return 'A'

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
		family_id = data['family_id']
		patient_id = data['patient_id']
		todo = data['todo']
	except:
		return 'invalid parameters', 400

	return 'A'


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
		family_id = data['family_id']
	except:
		return 'invalid parameters', 400

	return 'A'

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
		family_id = data['family_id']
		patient_id = data['patient_id']
	except:
		return 'invalid parameters', 400

	return 'A'

# VIEW_TODO - GET
# SEND: family_id, patient_id
# RECV: todo list as json array
@backend.route(api_path + 'view_todo', methods=['GET'])
def view_todo():
	data = request.json

	if not is_auth(request.headers):
		return 'not authenticated', 401

	family_id = None
	patient_id = None

	try:
		family_id = data['family_id']
		patient_id = data['patient_id']
	except:
		return 'invalid parameters', 400

	return 'A'

def is_auth(header):
	if header['Token'] in Cache:
		return True
	return False
