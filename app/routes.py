from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, weather):
        self.id = id
        self.name = name
        self.description = description
        self.weather = weather

planet_list = [
    Planet(1, "Mercury", "a rocky planet", "hot/dry"), 
    Planet(2, "Venus", "a yellow planet", "hot/stormy"), 
    Planet(3, "Earth", "a blue planet", "habitable")
    ]

planets_bp = Blueprint('planets', __name__, url_prefix="/planets")

@planets_bp.route('', methods = ['GET'])
def return_planet_list():
    planet_response = []
    for planet in planet_list:
        planet_response.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "weather": planet.weather
        })
    return jsonify(planet_response) 


@planets_bp.route('/<planet_id>', methods = ['GET'])
def get_one_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        rsp = {"msg": f"Invalid ID {planet_id}"}
        return jsonify(rsp), 400

    chosen_planet = None
    for planet in planet_list:
        if planet.id == planet_id:
            chosen_planet = planet
            break

    if chosen_planet is None:
        rsp = {"msg": f"Could not find planet with ID {planet_id}"}
        return jsonify(rsp), 404

    rsp = {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "weather": planet.weather
    }
    
    return jsonify(rsp), 200



    