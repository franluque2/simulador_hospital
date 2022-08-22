from flask import Flask, jsonify


class User:
    def signup(self):
        user = {
            "_id": "",
            "name": "",
            "email": "",
            "password": "",
            "profile_img":"",
            "phone_number": "",
            "is_professor": ""
        }

        return jsonify(user),200
