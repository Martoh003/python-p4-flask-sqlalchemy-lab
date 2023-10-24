#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter_by(id=id).first()
    if not animal:
        response_body = f'This animal is not found'
        status_code = 404
        response = make_response(response_body,status_code)
        return response
    
    response_body = f'''<h1>id:{animal.id}</h1> 
                        <h1>Name: {animal.name}</h1>
                        <h1>Species: {animal.species}
                        <h1>Zookeper: {animal.zookeeper.name}</h1>
                        <h1>Enclosure: {animal.enclosure.environment}</h1>'''
    response = make_response(response_body,202)
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter_by(id=id).first()
    if not zookeeper:
        response_body = 'The zookeeper is not found'
        response = make_response(response_body, 404)
        return response
    
    response_body = f'''<h1>id: {zookeeper.id}</h1>
                        <h1>Name: {zookeeper.name}</h1>
                        <h1>Birthday: {zookeeper.birthday}</h1>
                        '''
    animals = [animal for animal in zookeeper.animals]
    if not animals:
        response_body += f'<h1>This zookeper has no animals as of now</h1>'
    else:
        for animal in animals:
            response_body += f'<h1>Animal: {animal.name}</h1>'

    response = make_response(response_body, 202)
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter_by(id=id).first()
    if not enclosure:
        response_body = 'The zookeeper is not found'
        response = make_response(response_body, 404)
        return response
    
    response_body = f'''<h1>id: {enclosure.id}</h1>
                        <h1>Environment: {enclosure.environment}</h1>
                        <h1>Open to Visitors: {enclosure.open_to_visitors}</h1>'''
    
    animals = [animal for animal in enclosure.animals]
    if not animals:
        response_body += f'<h1>This enclosure has no animals as of now</h1>'
    else:
        for animal in animals:
            response_body += f'<h1>Animal: {animal.name}</h1>'

    response = make_response(response_body, 202)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
    