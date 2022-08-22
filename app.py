import hashlib
import datetime
import json

from bson.objectid import ObjectId
from bson.json_util import dumps
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'Your_Secret_Key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

client = MongoClient("mongodb://localhost:27017/")  # your connection string
db = client["Hospital"]
users_collection = db["Accounts"]
patients_collection=db["HospitalPatients"]


@app.route("/api/v1/users", methods=["POST"])
def register():
    new_user = request.get_json()  # store the json body request
    new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest()  # encrpt password
    doc = users_collection.find_one({"email": new_user["email"]})  # check if user exist
    if not doc:
        users_collection.insert_one(new_user)
        return jsonify({'msg': 'User created successfully'}), 201
    else:
        return jsonify({'msg': 'Username already exists'}), 409


@app.route("/api/v1/login", methods=["POST"])
def login():
    login_details = request.get_json()  # store the json body request
    user_from_db = users_collection.find_one({'email': login_details['email']})  # search for user in database

    if user_from_db:
        encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
        if encrpted_password == user_from_db['password']:
            access_token = create_access_token(identity=user_from_db['email'])  # create jwt token
            return jsonify(access_token=access_token), 200
    # , is_professor = user_from_db['is_professor']
    return jsonify({'msg': 'The email or password is incorrect'}), 401


@app.route("/api/v1/get_user_info", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        del user_from_db['_id'], user_from_db['password'],user_from_db['patients']  # delete data we don't want to return
        return jsonify({'profile': user_from_db}), 200
    else:
        return jsonify({'msg': 'Profile not found'}), 404

@app.route("/api/v1/patients", methods=["GET"])
@jwt_required()
def get_all_patients():
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        keys=user_from_db['patients'].values()
        patients=patients_collection.find() # {'_id':{'$in':keys}}

        if patients:
            patients = list(patients)

            for i in range(len(patients)):
                # print(str(patients[i]["_id"]))
                patients[i]["_id"]=str(patients[i]["_id"])
            return jsonify({'patients':json.loads(dumps(patients))}), 200
        else:
            return jsonify({'msg' : 'No Patients loaded'}), 204
    else:
        return jsonify({'msg': 'Profile not found'}), 404

@app.route("/api/v1/patient/<patientid>", methods=["GET"])
@jwt_required()
def get_single_patient(patientid):
    assert patientid == request.view_args['patientid']
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        keys=list(user_from_db['patients'].values())
        patientidtemp=ObjectId(patientid)
        patients=patients_collection.find_one({'_id':patientidtemp})
        if patients:
            if patientidtemp not in keys:
                return jsonify({'msg': 'Forbidden'}), 403
            del patients['_id']
            if not user_from_db['is_professor']:
                del patients['illnesses'], patients['risk_factors']
            return jsonify({'patient':json.loads(dumps(patients))}), 200
        else:
            return jsonify({'msg': 'Patient not found'}), 404
    else:
        return jsonify({'msg': 'Profile not found'}), 404


@app.route("/api/v1/patient/update_treatment", methods=["POST"])
@jwt_required()
def update_treatment():
    treatment_details = request.get_json()
    # print(treatment_details)
    patientid = treatment_details['id_patient']
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        keys=list(user_from_db['patients'].values())
        patientidtemp=ObjectId(patientid)
        patients=patients_collection.find_one({'_id':patientidtemp})
        if patients:
            patients_collection.find_one_and_update({'_id':patientidtemp},{'$set':{'treatments':treatment_details['treatment']}})
            return jsonify({'msg':'Updated Treatment'}), 200
        else:
            return jsonify({'msg': 'Patient not found'}), 404
    else:
        return jsonify({'msg': 'Profile not found'}), 404



if __name__ == '__main__':
    app.run(debug=True)
