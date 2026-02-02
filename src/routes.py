from flask import Blueprint, jsonify, request
from models import User, Character, Location, db, favorites_table

api = Blueprint('api', __name__)


# Usuarios


@api.route('/users', methods=['GET'])
def get_all():
    users = User.query.all()
    response = [user.serialize() for user in users]
    return jsonify(response), 200


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    return jsonify(user.serialize()), 200


@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': "email and password is necessary"}), 400

    new_user = User(
        email=data['email'],
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201


@api.route('/users/<int:id>', methods=['PUT'])
def edit_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if user:
        new_email = data.get('email')
        new_user = data.get('user')
        existing_user = User.query.filter_by(user=new_user).first()
        existing_email = User.query.filter_by(email=new_email).first()
        if new_email == existing_email:
            return jsonify({"error": "email already exist"}), 400

        if new_user == existing_user:
            return jsonify({"error": "user already exist"}), 400

        user['user'] = data.get('user', user['user'])
        user['email'] = data.get('email', user['email'])
        user['password'] = data.get('password', user['password'])
        db.session.commit()
        return jsonify(user.serialize()), 200
    return jsonify({"error": "User doesn't exist"}), 404


@api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(user, id)
    if not user:
        return jsonify({"error": "User not found"})

    db.session.delete(user)
    db.session.commit()
    return jsonify({"Delete succesfully"}), 200

# Personajes


@api.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    response = [character.serialize() for character in characters]
    return jsonify(response), 200


@api.route('/characters/<int:id>', methods=['GET'])
def get_character(id):
    character = Character.query.get(id)
    if not character:
        return jsonify({"error": "character does not exist"}), 404
    return jsonify(character.serialize()), 200


@api.route('/characters', methods=['POST'])
def create_character():
    data = request.get_json()
    if not data.get('name') or not data.get('quote') or not data.get('image'):
        return jsonify({'error': "name, quote and image is necessary"}), 400

    new_character = Character(
        name=data['name'],
        quote=data['quote'],
        image=data['image']
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201


@api.route('/characters/<int:id>', methods=['PUT'])
def edit_character(id):
    data = request.get_json()
    character = Character.query.get(id)
    if character:
        new_name = data.get('name')
        existing_name = Character.query.filter_by(name=new_name).first()
        if new_name == existing_name:
            return jsonify({"error": "character name already exist"}), 400

        character['name'] = data.get('name', character['name'])
        character['quote'] = data.get('quote', character['quote'])
        character['image'] = data.get('image', character['image'])
        db.session.commit()
        return jsonify(character.serialize()), 200
    return jsonify({"error": "User doesnt exist"}), 404


@api.route('/users/<int:id>', methods=['DELETE'])
def delete_character(id):
    Character = db.session.get(Character, id)
    if not Character:
        return jsonify({"error": "character not found"})

    db.session.delete(Character)
    db.session.commit()
    return jsonify({"Delete succesfully"}), 200

# Locaciones


@api.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    response = [location.serialize() for location in locations]
    return jsonify(response), 200


@api.route('/locations/<int:id>', methods=['GET'])
def get_location(id):
    location = Location.query.get(id)
    if not location:
        return jsonify({"error": "location does not exist"}), 404
    return jsonify(location.serialize()), 200


@api.route('/locations', methods=['POST'])
def create_location():
    data = request.get_json()
    if not data.get('name') or not data.get('use') or not data.get('town'):
        return jsonify({'error': "name, use, and town is necessary"}), 400

    new_location = Location(
        name=data['name'],
        use=data['use'],
        image=data['image'],
        town=data['town']
    )
    db.session.add(new_location)
    db.session.commit()
    return jsonify(new_location.serialize()), 201


@api.route('/characters/<int:id>', methods=['PUT'])
def edit_location(id):
    data = request.get_json()
    location = Location.query.get(id)
    if location:
        new_name = data.get('name')
        existing_name = Location.query.filter_by(name=new_name).first()
        if new_name == existing_name:
            return jsonify({"error": "location name already exist"}), 400

        location['name'] = data.get('name', location['name'])
        location['use'] = data.get('use', location['use'])
        location['image'] = data.get('image', location['image'])
        location['town'] = data.get('town', location['town'])
        db.session.commit()
        return jsonify(location.serialize()), 200
    return jsonify({"error": "location doesn't exist"}), 404


@api.route('/users/<int:id>', methods=['DELETE'])
def delete_location(id):
    location = db.session.get(location, id)
    if not location:
        return jsonify({"error": "location not found"})

    db.session.delete(location)
    db.session.commit()
    return jsonify({"Delete succesfully"}), 200

# Favorites


@api.route('/users/<int:id>/favorites', methods=['GET'])
def get_favorites(id):
    user = User.query.get(id)
    return jsonify(user.favorites_serialize()), 200


@api.route('/users/<int:id>/characters/<int:char_id>', methods=['POST'])
def add_favorite_character(id, char_id):
    user = User.query.get(id)
    character = Character.query.get(char_id)

    user.character_liked.append(character)
    db.session.commit()
    return jsonify(user.favorites_serialize()), 201


@api.route('/users/<int:id>/locations/<int:char_id>', methods=['POST'])
def add_favorite_location(id, char_id):
    user = User.query.get(id)
    location = Location.query.get(char_id)

    user.location_liked.append(location)
    db.session.commit()
    return jsonify(user.favorites_serialize()), 201
