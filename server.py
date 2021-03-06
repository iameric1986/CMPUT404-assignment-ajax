#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask


import flask
from flask import Flask, request, redirect, jsonify
import json
app = Flask(__name__)
app.debug = True

# An example world
# {
#    'a':{'x':1, 'y':2},
#    'b':{'x':2, 'y':3}
# }

class World:
    def __init__(self):
        self.clear()
        
    def update(self, entity, key, value):
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data

    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity,dict())
    
    def world(self):
        return self.space

# you can test your webservice from the commandline
# curl -v   -H "Content-Type: appication/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 

myWorld = World()          

# I give this to you, this is how you get the raw body/data portion of a post in flask
# this should come with flask but whatever, it's not my project.
def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data != ''):
        return json.loads(request.data)
    else:
        return json.loads(request.form.keys()[0])

# Parse the JSON object and update the World
# Ref: http://stackoverflow.com/questions/2733813/iterating-through-a-json-object
# Author: tzot
def data_parse(entity, data):
    #print("Parsing data " + data);
    for axis, coord in data.iteritems():
        #print("Axis is " + axis + " coord is " + coord)
        myWorld.update(entity, axis, coord)
    return

# General reference to Flask API documentation for how to do stuff
# Ref: http://flask.pocoo.org/docs/0.12/api/

# General reference to Python JSON API documentation for how to do the things
# Ref: https://docs.python.org/2/library/json.html

@app.route("/")
def hello():
    '''Return something coherent here.. perhaps redirect to /static/index.html '''
    #print("Root")
    return redirect("/static/index.html")

@app.route("/entity/<entity>", methods=['POST','PUT'])
def update(entity):
    '''update the entities via this interface'''
    entity_data = flask_post_json()
    
    if (len(entity_data) == 0): #Make sure there is data
        print("No data")
        return None

    if (request.method == 'POST'): # Update the object if it is a POST
        #print("POST/entity/<entity>")
        data_parse(entity, entity_data)
        return jsonify(myWorld.get(entity))

    # Assume that if the method is not POST it is automatically PUT since this end-point only accepts POST and PUT REST requests
    # We create a new entity in the world.
    #print("PUT/entity/<entity>")
    myWorld.set(entity, entity_data)
    return jsonify(myWorld.get(entity))

@app.route("/world", methods=['POST','GET'])    
def world():
    #print("/world")
    '''you should probably return the world here'''
    # If we're simply returning the world with this end point then we do not need to do separate operations for each RESTful method
    return jsonify(myWorld.world()) # Wrap the dict into a Response object with JSON mimetype

@app.route("/entity/<entity>")    
def get_entity(entity):
    #print("GET/entity/<entity>")
    '''This is the GET version of the entity interface, return a representation of the entity'''
    return jsonify(myWorld.get(entity)) # Wrap the dict into a Response object with JSON mimetype

@app.route("/clear", methods=['POST','GET'])
def clear():
    #print("/clear")
    '''Clear the world out!'''
    myWorld.clear() # myWorld.space now points to an empty dictionary
    return jsonify(myWorld.world()) # Wrap the dict into a Response object with JSON mimetype

if __name__ == "__main__":
    app.run()
