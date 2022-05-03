import json
from flask import Blueprint, jsonify, request
from app.models.solar_system import Planet
from app import db

planets_bp = Blueprint('planets', __name__, url_prefix="/planets")

@planets_bp.route('', methods = ['POST'])
def create_one_planet():
    request_body = request.get_json()
    new_planet = Planet(name = request_body["name"],
                        description = request_body["description"],
                        weather = request_body["weather"])
    db.session.add(new_planet)
    db.session.commit()

    return {
        "id": new_planet.id,
        "msg": f"Successfully created planet with ID {new_planet.id}"
    }, 201    

@planets_bp.route('', methods = ['GET'])
def get_all_planets():
    planets = Planet.query.all()
    planets_response = []
    for planet in planets:
        planets_response.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "weather": planet.weather
        })

    return jsonify(planets_response), 200

@planets_bp.route('/<planet_id>', methods = ['GET'])
def get_one_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        rsp = {"msg": f"Invalid ID: {planet_id}"}
        return jsonify(rsp), 400
    chosen_planet = Planet.query.get(planet_id)
    if chosen_planet is None:
        rsp = {"msg": f"Could not find planet with ID: {planet_id}"}
        return jsonify(rsp), 404

    rsp = {
        "id": chosen_planet.id,
        "name": chosen_planet.name,
        "description": chosen_planet.description,
        "weather": chosen_planet.weather
    }  
    return jsonify(rsp), 200

@planets_bp.route('/<planet_id>', methods = ['PUT'])
def put_one_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        rsp = {"msg": f"Invalid ID: {planet_id}"}
        return jsonify(rsp), 400
    chosen_planet = Planet.query.get(planet_id)
    if chosen_planet is None:
        rsp = {"msg": f"Could not find planet with ID: {planet_id}"}
        return jsonify(rsp), 404

    request_body = request.get_json()    
    try:
        chosen_planet.name = request_body["name"]
        chosen_planet.description = request_body["description"]
        chosen_planet.weather = request_body["weather"]
    except KeyError:
        return {
            "msg": "name, description, and weather are required."
        }, 400
    db.session.commit()

    return {
        "msg": f"planet #{chosen_planet.id} successfully replaced"
    }, 200        

@planets_bp.route('/<planet_id>', methods = ['DELETE'])
def delete_one_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        rsp = {"msg": f"Invalid ID: {planet_id}"}
        return jsonify(rsp), 400

    chosen_planet = Planet.query.get(planet_id)
    if chosen_planet is None:
        rsp = {"msg": f"Could not find planet with ID: {planet_id}"}
        return jsonify(rsp), 404

    db.session.delete(chosen_planet)
    db.session.commit()

    return {
        "msg": f"planet #{chosen_planet.id} successfully deleted."
    }, 200    