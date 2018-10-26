#!/usr/bin/env python3
#Code by Lukas Hennicks, lukashen@kth.se.
#Note that this file should be in the root directory.

from flask import Flask, request, jsonify, Response, abort
from datetime import datetime
from time import sleep
from pprint import pformat
import socket
import sys
import json
import logging
import sqlite3



""" Set up logging """
logging.basicConfig(filename='./Resources/api_log.log', level=40, format='%(asctime)s %(message)s')


""" Set up db params and path. """
DB_PATH = './Resources/main.db'

""" Define PORTS & IP's """
API_PORT = 9000
MVMT_PORT = 9001
IP_LOCAL = '127.0.0.1'
IP_IFACE = '130.229.142.238' # dependent on platform. Lukas MBP at home as placeholder.

""" Create flask app. """
app = Flask(__name__)

@app.route('/')
def root():
    with open('./README.txt', 'r') as file:
        content = file.read()
        return Response(content, mimetype="text/plain")


""" Define routes & valid requests """
@app.route('/health', methods=['GET', 'POST'])
def GET_POST_health():
    """ Handle GET and POST requests for robot health."""
    if request.method == 'GET':
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM HEALTH_SNAPSHOTS")
        conn.commit()
        content = c.fetchall()
        content = pformat(content)
        conn.close()
        return Response(str(content), mimetype="text/plain")


    elif request.method == 'POST':

        """ Set up time instance"""
        now = datetime.now()

        """ Parameter fallback """
        heat = ''
        time_running = ''
        vibrations = ''
        disturbances = ''

        """ Format parameters """
        entry_added_at = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '@' + str(now.hour) + ':' + str(now.minute)\
        + ':' + str(now.second)
        heat = request.form['heat']
        time_running = request.form['time_running']
        vibrations = request.form['vibrations']
        disturbances = request.form['disturbances']

        """ add data to db (table 'health') """

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS HEALTH_SNAPSHOTS(ID integer PRIMARY KEY AUTOINCREMENT, datetime_added text NOT NULL, heat text NOT NULL, time_running integer NOT NULL, vibrations text NOT NULL, disturbances text NOT NULL);")
        c.execute("INSERT INTO HEALTH_SNAPSHOTS VALUES (?, ?, ?, ?, ?, ?)", (None, entry_added_at, heat, time_running, vibrations, disturbances))
        conn.commit()
        conn.close()

        return "Post Successful!"



@app.route('/health/<attribute>', methods=['GET'])
def GET_health_attr(attribute):
    """ Return specific health data """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT {} FROM HEALTH_SNAPSHOTS".format(attribute))
    conn.commit()
    content = c.fetchall()
    #content = pformat(content)
    conn.close()
    return Response(str(content), mimetype="text/plain")



@app.route('/run', methods=['GET', 'POST'])
def get_and_post():
    """ GET capability is only for demonstrations purposes. """
    if request.method == 'GET':
        # WITH QUERY PARAMETERS:
        parameters = request.args.get('parameters', None)
        id = request.args.get('id', None)

        if parameters == None or id == None:
            logging.error("Bad request was issued. Missing parameters in query.")
            abort(400) #Bad request, missing params.
            #return ("Request Unsuccessful. Missing query parameters.")

        """ Set up local inter-app TCP socket and establish connection."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((IP_LOCAL, MVMT_PORT))
            s.send(parameters.encode('utf-8'))
            return ("Request Successful for ID: " + str(id))
        except socket.error:
            logging.error("A GET-Query could not be resolved. There was an error connecting to the movement program.")
            abort(500)

    elif request.method == 'POST':
        if request.form['parameters'] == None or request.form['id'] == None:
            logging.error("Bad request was issued. Missing parameters in query.")
            abort(400) #Bad request, missing params.
            """ Set up local inter-app TCP socket and establish connection."""


        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((IP_LOCAL, MVMT_PORT))
            s.send(request.form['parameters'].encode('utf-8'))
            return ("Request Successful for ID: " + str(request.form['id']))
        except socket.error:
            logging.error("A POST could not be resolved. There was an error connecting to the movement program.")
            abort(500)


def app_run(scope=''):
    """ Default to localhost """
    if(scope == 'local'):
        app.run(host=IP_LOCAL, port=API_PORT, debug = 'ON')
    else:
        app.run(host=IP_IFACE, port=API_PORT)

def main():
    app_run('local')



if __name__ == '__main__':
    main()
