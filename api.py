#!/usr/bin/env python3
#Code by Lukas Hennicks, lukashen@kth.se.
#Note that this file should be in the root directory.

from flask import Flask, request, jsonify, Response, abort
from datetime import datetime
from time import sleep
from pprint import pformat
import socket
import sys, getopt
import json
import logging
import sqlite3
import subprocess




""" Set up logging """
logging.basicConfig(filename='./Resources/api_log.log', level=40, format='%(asctime)s %(message)s')


""" Set up db params and path. """
HEALTH_DB_PATH = './Resources/health.db'
QUERY_DB_PATH = './Resources/queries.db'
C_CODE_PATH = './dummy'

""" Define PORTS. Pre-decided."""
API_PORT = 9000
MVMT_PORT = 9001
localhost = "127.0.0.1"

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
        conn = sqlite3.connect(HEALTH_DB_PATH)
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

        conn = sqlite3.connect(HEALTH_DB_PATH)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS HEALTH_SNAPSHOTS(ID integer PRIMARY KEY AUTOINCREMENT, datetime_added text NOT NULL, heat text NOT NULL, time_running integer NOT NULL, vibrations text NOT NULL, disturbances text NOT NULL);")
        c.execute("INSERT INTO HEALTH_SNAPSHOTS VALUES (?, ?, ?, ?, ?, ?)", (None, entry_added_at, heat, time_running, vibrations, disturbances))
        conn.commit()
        conn.close()
        return "Post Successful!"



@app.route('/health/<attribute>', methods=['GET'])
def GET_health_attr(attribute):
    """ Return specific health data """
    conn = sqlite3.connect(HEALTH_DB_PATH)
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
        seq_num = request.args.get('seq_num', None)

        """ Update DB """
        dbconn = sqlite3.connect(QUERY_DB_PATH)
        db = dbconn.cursor()
        db.execute("CREATE TABLE IF NOT EXISTS QUERIES(ID integer PRIMARY KEY AUTOINCREMENT, parameters integer NOT NULL, seq_num integer NOT NULL);")
        db.execute("INSERT INTO QUERIES VALUES(?, ?, ?)", (None, parameters, seq_num))
        dbconn.commit()
        dbconn.close()

        """ Run C-code """
        result = subprocess.run(C_CODE_PATH, stdout=subprocess.PIPE)
        print(result.stdout)

        if parameters == None or seq_num == None:
            logging.error("Bad request was issued. Missing parameters in query.")
            abort(400) #Bad request, missing params.
            #return ("Request Unsuccessful. Missing query parameters.")

        return ("Request Successful for SEQ: " + str(seq_num))

        """ Set up local inter-app TCP socket and establish connection."""
        """try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((localhost, MVMT_PORT))
            s.send(parameters.encode('utf-8'))
            return ("Request Successful for ID: " + str(id))
        except socket.error:
            logging.error("A GET-Query could not be resolved. There was an error connecting to the movement program.")
            abort(500)"""

    elif request.method == 'POST':
        if request.form['parameters'] == None or request.form['seq_num'] == None:
            logging.error("Bad request was issued. Missing parameters in query.")
            abort(400) #Bad request, missing params.
            """ Set up local inter-app TCP socket and establish connection."""
        else:
            """ Update DB """
            parameters = request.form['parameters']
            seq_num = request.form['seq_num']
            dbconn = sqlite3.connect(QUERY_DB_PATH)
            db = dbconn.cursor()
            db.execute("CREATE TABLE IF NOT EXISTS QUERIES(ID integer PRIMARY KEY AUTOINCREMENT, parameters integer NOT NULL, seq_num integer NOT NULL);")
            db.execute("INSERT INTO QUERIES VALUES(?, ?, ?)", (None, parameters, seq_num))
            dbconn.commit()
            dbconn.close()

            """ Run C-code """
            result = subprocess.run(C_CODE_PATH, stdout=subprocess.PIPE)
            print(result.stdout)

            if parameters == None or seq_num == None:
                logging.error("Bad request was issued. Missing parameters in query.")
                abort(400) #Bad request, missing params.

            return ("Request Successful for SEQ: " + str(seq_num))

        """try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((localhost, MVMT_PORT))
            s.send(request.form['parameters'].encode('utf-8'))
            return ("Request Successful for ID: " + str(request.form['id']))
        except socket.error:
            logging.error("A POST could not be resolved. There was an error connecting to the movement program.")
            abort(500)"""


def app_run(ip='local'):
    """ Default to localhost """
    if(ip == 'local'):
        app.run(host="127.0.0.1", port=API_PORT, debug = 'ON')
    else:
        app.run(host=ip, port=API_PORT)

def main(argv):


    """ Set options. """
    try:
      opts, args = getopt.getopt(argv,"i:l",["ip="])
    except getopt.GetoptError:
      print('api.py -i <interface ip> -l (local)')
      sys.exit(2)

    for opt, arg in opts:
        if opt == '-l':
            app_run()
        elif opt in ("-i", "--ip"):
            app_run(arg)





if __name__ == '__main__':
    main(sys.argv[1:])
