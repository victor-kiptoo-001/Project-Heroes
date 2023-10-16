from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return ''

# Get all heroes from the database
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [hero.__dict__ for hero in heroes]
    return jsonify(heroes_data)

# Get hero by ID from the database
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.__dict__)
    else:
        return jsonify({"error": "Hero not found"}), 404

# Get all powers from the database
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [power.__dict__ for power in powers]
    return jsonify(powers_data)

# Get power by ID from the database
@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.__dict__)
    else:
        return jsonify({"error": "Power not found"}), 404

# Update power description by ID
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    new_description = request.json.get('description')
    if new_description:
        power = Power.query.get(id)
        if power:
            power.description = new_description
            db.session.commit()
            return jsonify(power.__dict__)
        else:
            return jsonify({"error": "Power not found"}), 404
    else:
        return jsonify({"error": "Invalid request. 'description' parameter is required."}), 400

# Create a new hero power
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    request_data = request.json
    power_id = request_data.get("power_id")
    hero_id = request_data.get("hero_id")

    hero_power = HeroPower(strength=request_data.get("strength"),
                            description=request_data.get("description"),
                            hero_id=hero_id,
                            power_id=power_id)

    db.session.add(hero_power)
    db.session.commit()

    hero = Hero.query.get(hero_id)
    if hero:
        return jsonify(hero.__dict__), 201  
    else:
        return jsonify({"error": "Hero not found"}), 404

if __name__ == '__main__':
    app.run(port=5555)
