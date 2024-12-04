import hashlib
import datetime
import json

from bson.objectid import ObjectId
from bson.json_util import dumps
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
from FranWhatsappClient import sendWhatsAppMessage

import PatientCreation
import PatientSimulation
import FranMongoClient
import TreatmentParse

app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'Your_Secret_Key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

db = FranMongoClient.db
users_collection = db["Accounts"]
patients_collection = db["HospitalPatients"]


@app.route("/api/v1/register", methods=["POST"])
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
    # emit('my response', {'a':True}, broadcast=True)

    login_details = request.get_json()  # store the json body request
    user_from_db = users_collection.find_one({'email': login_details['email']})  # search for user in database

    if user_from_db:
        encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
        if encrpted_password == user_from_db['password']:
            access_token = create_access_token(identity=user_from_db['email'])  # create jwt token
            return jsonify(access_token=access_token), 200
    # , is_professor = user_from_db['is_professor']
    return jsonify({'msg': 'The email or password is incorrect'}), 401


@app.route("/api/v1/change_details", methods=["POST"])
@jwt_required()
def change_details():
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    change_details_account = request.get_json()
    if user_from_db:
        if "password_old" in change_details_account and change_details_account["password_old"] and change_details_account["password_new"] and hashlib.sha256(
                change_details_account['password_old'].encode("utf-8")).hexdigest() == user_from_db["password"]:
            users_collection.update_one(
            {'email': current_user}, 
            {'$set': {'password': change_details_account["password_new"]}}
        ) 
            return jsonify({'msg': "Changed Password"}), 200
        if "should_receive_whatsapp_notifications" in change_details_account:
            users_collection.update_one(
            {'email': current_user}, 
            {'$set': {'should_receive_whatsapp_notifications': change_details_account["should_receive_whatsapp_notifications"]}}
        )     
            return jsonify({'msg': "Changed Whatsapp Notification Options"}), 200

    else:
        return jsonify({'msg': 'Profile not found'}), 404


@app.route("/api/v1/get_user_info", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        del user_from_db['_id'], user_from_db['password'], user_from_db["notifications"], user_from_db[
            "pending_transfers"]  # delete data we don't want to return
        temparray=[]
        for i in user_from_db['patients']:
            temparray.append(str(i))
        user_from_db['patients']=temparray
        return jsonify({'profile': user_from_db}), 200
    else:
        return jsonify({'msg': 'Profile not found'}), 404


@app.route("/api/v1/patients", methods=["GET"])
@jwt_required()
def get_filtered_patients():
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        keys = user_from_db['patients']
        patients = []

        if not user_from_db['is_professor']:
            for key in keys:
                temp = patients_collection.find_one({'_id': ObjectId(key)})
                if temp is not None:
                    patients.append(temp)

            if patients is not []:
                for p in patients:
                    # print(str(patients[i]["_id"]))
                    p['_id'] = str(p['_id'])
                return jsonify({'patients': json.loads(dumps(patients))}), 200
            else:
                return jsonify({'msg': 'No Patients loaded'}), 204
        else:
            for temp in patients_collection.find({}):
                if temp is not None:
                    patients.append(temp)

            if patients is not []:
                for p in patients:
                    # print(str(patients[i]["_id"]))
                    p['_id'] = str(p['_id'])
                return jsonify({'patients': json.loads(dumps(patients))}), 200
            else:
                return jsonify({'msg': 'No Patients loaded'}), 204
    else:
        return jsonify({'msg': 'Profile not found'}), 404


@app.route("/api/v1/all_patients", methods=["GET"])
@jwt_required()
def get_all_patients():
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        patients = []
        for temp in patients_collection.find({}):
            if temp is not None:
                patients.append(temp)

        if patients is not []:
            for p in patients:
                p['_id'] = str(p['_id'])
                if not user_from_db['is_professor']:
                    del p['illnesses'], p['risk_factors']
                else:
                    users = FranMongoClient.FranMongo().get_users_by_assigned_patient(p['_id'])
                    if users:
                        temp = []
                        for u in users:
                            temp2 = u
                            temp2["_id"] = str(temp2["_id"])
                            del temp2["phone_number"]
                            del temp2["patients"]
                            del temp2["password"]
                            temp.append(temp2)
                        p["assigned_users"] = temp

            return jsonify({'patients': json.loads(dumps(patients))}), 200
        else:
            return jsonify({'msg': 'No Patients loaded'}), 204
    else:
        return jsonify({'msg': 'Profile not found'}), 404


@app.route("/api/v1/patient/<patientid>", methods=["GET"])
@jwt_required()
def get_single_patient(patientid):
    assert patientid == request.view_args['patientid']
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        keys = user_from_db['patients']
        patientidtemp = ObjectId(patientid)
        patients = patients_collection.find_one({'_id': patientidtemp})
        if patients:
            if patientidtemp not in keys and (not user_from_db['is_professor']):
                return jsonify({'msg': 'Forbidden'}), 403
            del patients['_id']
            if not user_from_db['is_professor']:
                del patients['illnesses'], patients['risk_factors']
            else:
                users = FranMongoClient.FranMongo().get_users_by_assigned_patient(patientid)
                if users:
                    temp = []
                    for u in users:
                        temp2 = u
                        temp2["_id"] = str(temp2["_id"])
                        del temp2["phone_number"]
                        del temp2["patients"]
                        del temp2["password"]
                        temp.append(temp2)
                    patients["assigned_users"] = temp
            return jsonify({'patient': json.loads(dumps(patients))}), 200
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
        keys = user_from_db['patients']
        patientidtemp = ObjectId(patientid)
        patients = patients_collection.find_one({'_id': patientidtemp})
        if patients:
            treatmentlist=TreatmentParse.parse_treatment_string(treatment_details['treatment'])
            patients_collection.find_one_and_update({'_id': patientidtemp},
                                                    {'$set': {'treatments': treatmentlist}})
            patients_collection.find_one_and_update({'_id': patientidtemp},
                                                    {'$set': {'treatments_string': treatment_details['treatment']}})
            return jsonify({'msg': 'Updated Treatment'}), 200
        else:
            return jsonify({'msg': 'Patient not found'}), 404
    else:
        return jsonify({'msg': 'Profile not found'}), 404
    

@app.route("/api/v1/patient/add_comment", methods=["POST"])
@jwt_required()
def add_comment():
    details = request.get_json()
    # print(treatment_details)
    patientid = details['id_patient']
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        keys = user_from_db['patients']
        patientidtemp = ObjectId(patientid)
        patients = patients_collection.find_one({'_id': patientidtemp})
        if patients:
            patients_collection.find_one_and_update({'_id': patientidtemp},
                                                    {'$push': {'comments': details['comment']}})
            return jsonify({'msg': 'Added Comment'}), 200
        else:
            return jsonify({'msg': 'Patient not found'}), 404
    else:
        return jsonify({'msg': 'Profile not found'}), 404


@app.route("/api/v1/patient/insert_patient", methods=["POST"])
@jwt_required()
def insert_patient():
    patient_details = request.get_json()
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        if not user_from_db["is_professor"]:
            return jsonify({'msg': 'Forbidden, only Professors may insert patients.'}), 403

        PatientCreation.generate_patient(patient_details)
        return jsonify({'msg': 'Inserted Patient'}), 200


@app.route("/api/v1/patient/delete_patient", methods=["POST"])
@jwt_required()
def delete_patient():
    patient_ids = request.get_json()
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        if not user_from_db["is_professor"]:
            return jsonify({'msg': 'Forbidden, only Professors may delete patients.'}), 403

        FranMongoClient.FranMongo().delete_patients(patient_ids["patient_ids"])
        return jsonify({'msg': 'Deleted Patients'}), 200

@app.route("/api/v1/patient/toggle_patient", methods=["POST"])
@jwt_required()
def toggle_patient_status():
    patient_details = request.get_json()
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        if not user_from_db["is_professor"]:
            return jsonify({'msg': 'Forbidden, only Professors may delete patients.'}), 403
        
        FranMongoClient.FranMongo().toggle_patient_status(patient_details["patient_id"], patient_details["should_update"])
        return jsonify({'msg': 'Updated Patient'}), 200



@app.route("/api/v1/delete_notifications", methods=["POST"])
@jwt_required()
def delete_notification():
    notifications = request.get_json()
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        FranMongoClient.FranMongo().delete_notification(str(user_from_db["_id"]), notifications["notification"])

        return jsonify({'msg': 'Deleted notifications'}), 200


@app.route("/api/v1/notifications", methods=["GET"])
@jwt_required()
def get_notifications():
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        notificationsdb = user_from_db["notifications"]
        return jsonify({'notifications': json.loads(dumps(notificationsdb))}), 200
    else:
        return jsonify({'msg': 'Profile not found'}), 404


@app.route("/api/v1/transfer/send_transfer_request", methods=["POST"])
@jwt_required()
def send_transfer_request():
    details = request.get_json()
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        if details["receiver_ids"] and details["patient_id"]:
            FranMongoClient.FranMongo().send_request(str(user_from_db["_id"]), (details["receiver_ids"]),
                                         str(details["patient_id"]))
            return jsonify({'msg': 'Transfered Patient'}), 200
        else:
            return jsonify({'msg': 'Missing info'}), 400


@app.route("/api/v1/transfer/", methods=["GET"])
@jwt_required()
def get_transfers():
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        temp = []
        transfer_requests = user_from_db["pending_transfers"]
        if transfer_requests and len(transfer_requests)>0:
            for transf in transfer_requests:
                item = {'patientid': transf["patient_id"],
                        'senderid': transf["sender_id"],
                        'patientname': patients_collection.find_one({"_id": ObjectId(transf["patient_id"])})["name"],
                        'sendername': users_collection.find_one({"_id": ObjectId(transf["sender_id"])})["name"],
                        'patientsrc': patients_collection.find_one({"_id": ObjectId(transf["patient_id"])})["src"]
                        }
                temp.append(item)
        return jsonify({'transfer_requests': json.loads(dumps(temp))}), 200
    else:
        return jsonify({'msg': 'Profile not found'}), 404


@app.route("/api/v1/transfer/reject_transfer", methods=["POST"])
@jwt_required()
def reject_transfer():
    details = request.get_json()
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        if "patient_id" in details and "user_id" in details:
            FranMongoClient.FranMongo().process_request(str(user_from_db["_id"]), details["user_id"], details["patient_id"], False)
            # FranMongoClient.FranMongo.assign_patient(details["patient_id"], user_from_db["_id"])
            # FranMongoClient.FranMongo.unassign_patient(details["patient_id"], details["user_id"])
            return jsonify({'msg': 'Transfered Patient'}), 200
        else:
            return jsonify({'msg': 'Missing info'}), 400


@app.route("/api/v1/transfer/accept_transfer", methods=["POST"])
@jwt_required()
def accept_transfer():
    details = request.get_json()
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        if "patient_id" in details and "user_id" in details:
            FranMongoClient.FranMongo().process_request(str(user_from_db["_id"]), details["user_id"], details["patient_id"], True)
            # FranMongoClient.FranMongo.assign_patient(details["patient_id"], user_from_db["_id"])
            # FranMongoClient.FranMongo.unassign_patient(details["patient_id"], details["user_id"])
            return jsonify({'msg': 'Transfered Patient'}), 200
        else:
            return jsonify({'msg': 'Missing info'}), 400


@app.route("/api/v1/patient/assign_patient", methods=["POST"])
@jwt_required()
def assign_patient():
    details = request.get_json()
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        if not user_from_db["is_professor"]:
            return jsonify({'msg': 'Forbidden, only Professors may assign patients.'}), 403
        if "patient_ids" in details and "user_ids" in details:
            FranMongoClient.FranMongo().assign_patient(details["patient_ids"], details["user_ids"])
            return jsonify({'msg': 'Assigned Patients'}), 200
        else:
            return jsonify({'msg': 'Missing info'}), 400


@app.route("/api/v1/patient/unassign_patient", methods=["POST"])
@jwt_required()
def unassign_patient():
    details = request.get_json()
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        if not user_from_db["is_professor"]:
            return jsonify({'msg': 'Forbidden, only Professors may unassign patients.'}), 403
        if "patient_ids" in details and "user_ids" in details:
            FranMongoClient.FranMongo().unassign_patient(details["patient_ids"], details["user_ids"])
            return jsonify({'msg': 'Unassigned Patients'}), 200
        else:
            return jsonify({'msg': 'Missing info'}), 400


@app.route("/api/v1/students", methods=["GET"])
@jwt_required()
def get_all_students():
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        # if not user_from_db["is_professor"]:
        #     return jsonify({'msg': 'Forbidden, only Professors may get the list of students.'}), 403
        users = []
        userdb = users_collection.find({})
        for u in userdb:
            temp = u
            temp["_id"] = str(temp["_id"])
            del temp["password"]
            users.append(temp)

        return jsonify({'users': json.loads(dumps(users))}), 200
    else:
        return jsonify({'msg': 'Profile not found'}), 404


@app.route("/api/v1/student/<studentid>", methods=["GET"])
@jwt_required()
def get_student(studentid):
    current_user = get_jwt_identity()
    assert studentid == request.view_args['studentid']
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        # if not user_from_db["is_professor"]:
        #     return jsonify({'msg': 'Forbidden, only Professors may get the list of students.'}), 403
        user = users_collection.find_one({'_id': ObjectId(studentid)})
        if user:
            temp = user
            temp["_id"] = str(temp["_id"])
            del temp["password"]
            return jsonify({'user': json.loads(dumps(temp))}), 200
        else:
            return jsonify({'msg': 'Student not found'}), 404
    else:
        return jsonify({'msg': 'Profile not found'}), 404


@app.route("/api/v1/regen_patient", methods=["POST"])
@jwt_required()
def regenerate_patient():
    details = request.get_json()
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        if details["patient_id"]:
            PatientCreation.regenerate_patient(details["patient_id"])
            return jsonify({'msg': 'Regenerated Patient'}), 200
        else:
            return jsonify({'msg': 'Missing info'}), 400


@app.route("/api/v1/students_by_assigned_patient/<patientid>", methods=["GET"])
@jwt_required()
def get_students_by_assigned_patient(patientid):
    current_user = get_jwt_identity()
    assert patientid == request.view_args['patientid']
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        if not user_from_db["is_professor"]:
            return jsonify(
                {'msg': 'Forbidden, only Professors may get the list of students assigned to a patient'}), 403
        users = FranMongoClient.FranMongo().get_users_by_assigned_patient(patientid)
        if users:
            temp = []
            for u in users:
                temp2 = u
                temp2["_id"] = str(temp2["_id"])
                del temp2["phone_number"]
                del temp2["patients"]
                del temp2["password"]
                temp.append(temp2)
            return jsonify({'users': json.loads(dumps(temp))}), 200
        else:
            return jsonify({'msg': 'Students not found'}), 404
    else:
        return jsonify({'msg': 'Profile not found'}), 404


@app.route("/api/v1/inner/updatesims", methods=["POST"])
def updatecurrentsims():
    patientid = request.get_json()['id_patient']
    patient = patients_collection.find_one({'_id': ObjectId(patientid)})
    del patient['illnesses'], patient['risk_factors']
    patient["_id"] = str(patient["_id"])

    socketio.emit('update patient', {'patient': json.loads(dumps(patient))})
    return jsonify({'data': True}), 200


@app.route("/api/v1/inner/senddangernotification", methods=["POST"])
def senddangernotification():
    patientid = request.get_json()['id_patient']
    patient = patients_collection.find_one({'_id': ObjectId(patientid)})
    del patient['illnesses'], patient['risk_factors']
    patient["_id"] = str(patient["_id"])

    users = FranMongoClient.FranMongo().get_users_by_assigned_patient(patientid)
    if users:
        for u in users:
            socketio.emit('patient danger', {'patient': json.loads(dumps(patient))})
            #Remove False when ready to test whatsapp messages
            if u["should_receive_whatsapp_notifications"]==True and len(u["phone_number"])==12:
                sendWhatsAppMessage(f'Tu Paciente {patient["name"]} ha tenido cambios importantes en el simulador!', u["phone_number"])
    return jsonify({'data': True}), 200



if __name__ == '__main__':
    # app.run(debug=True, host="0.0.0.0", threaded=True)
    PatientSimulation.start_sim()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
