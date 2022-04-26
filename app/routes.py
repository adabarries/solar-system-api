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