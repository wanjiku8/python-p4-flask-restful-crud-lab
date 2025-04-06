#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants])


class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return [plant.to_dict() for plant in plants], 200

    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
            is_in_stock=data.get('is_in_stock', True)  # Default to True if not provided
        )
        db.session.add(new_plant)
        db.session.commit()
        return new_plant.to_dict(), 201


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get_or_404(id)
        return plant.to_dict(), 200

    def put(self, id):
        data = request.get_json()
        plant = Plant.query.get_or_404(id)
        plant.name = data['name']
        plant.image = data['image']
        plant.price = data['price']
        db.session.commit()
        return plant.to_dict(), 200

    def delete(self, id):
        plant = Plant.query.get_or_404(id)
        db.session.delete(plant)
        db.session.commit()
        return '', 204

    def patch(self, id):
        plant = Plant.query.get_or_404(id)
        data = request.get_json()

        # Updating fields based on the received data
        if 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']

        db.session.commit()
        return plant.to_dict(), 200


# Adding the Resources to API with corresponding routes
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
