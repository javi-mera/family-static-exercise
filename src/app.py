"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_get_all():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()

    if members: 
        return jsonify(members), 200
    else: 
        return 'Family not found', 400

@app.route('/members/<int:id>', methods=['GET'])
def handle_get_single(id):
    member = jackson_family.get_member(id)

    if member: 
        return jsonify(member), 200
    else: 
        return 'Member not found', 400

@app.route('/members/<int:id>', methods=['DELETE'])
def handle_delete_member(id):
    holder = jackson_family.get_member(id)
    member = jackson_family.delete_member(id)

    if member:
        return jsonify(holder), 200
    else:
        return 'Member not found', 400

@app.route('/members', methods=['POST'])
def handle_new_member():
    new_member = request.get_json()
    new_member["id"] = jackson_family._generateId()

    if new_member["first_name"] != "" and new_member["age"] != "" and new_member["lucky_numbers"] != "":
        member = jackson_family.add_member(new_member)
        return jsonify(member), 200
    else:
        return 'Incomplete member', 400




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
