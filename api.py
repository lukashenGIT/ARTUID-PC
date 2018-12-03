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
from helpers import json_to_light_parameters, make_dbs, feelings_to_json
from feelings import *


""" Make sure all necessary tables are created in db files. """
make_dbs()

""" status variable """
status = 0

""" Set up logging """
logging.basicConfig(filename='./Resources/api_log.log', level=40, format='%(asctime)s %(message)s')


""" Set up db params and path. """
HEALTH_DB_PATH = './Resources/health.db'
QUERY_DB_PATH = './Resources/queries.db'
C_CODE_PATH = './bin/runner'

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

		health_dict = {}

		""" Format the content and get table for each arm. """
		for arm in range(1, 7):
			c.execute("SELECT * FROM HEALTH_SNAPSHOTS_ARM{} WHERE ID==((SELECT max(ID) FROM HEALTH_SNAPSHOTS_ARM{}));".format(arm, arm))
			content = c.fetchall()

			for arm in range(1, 7):
				health_dict["heat_motor_1_arm{}".format(arm)] = {"heat_motor_1": content[0][2], "heat_motor_2": content[0][3], "heat_motor_3": content[0][4], "heat_motor_4": content[0][5], "heat_motor_5": content[0][6]}

		conn.close()
		return jsonify(health_dict)


	elif request.method == 'POST':
		""" For making test entries into the DB. Should not be in deployed api since these entries are added by the C program. """
		""" Set up time instance"""
		now = datetime.now()

		""" Parameter fallback """
		heat_motor_1 = request.form['heat_motor_1']
		heat_motor_2 = request.form['heat_motor_2']
		heat_motor_3 = request.form['heat_motor_3']
		heat_motor_4 = request.form['heat_motor_4']
		heat_motor_5 = request.form['heat_motor_5']

		""" Format parameters """
		entry_added_at = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '@' + str(now.hour) + ':' + str(now.minute)\
		+ ':' + str(now.second)


		""" add data to db (table 'health') """

		conn = sqlite3.connect(HEALTH_DB_PATH)
		c = conn.cursor()
		for arm in range(1,7):
			"""Adding the same data to each arm. As stated only for debugging purposes"""
			c.execute("INSERT INTO HEALTH_SNAPSHOTS_ARM{} VALUES (?, ?, ?, ?, ?, ?, ?)".format(arm), (None, entry_added_at, heat_motor_1, heat_motor_2, heat_motor_3, heat_motor_4, heat_motor_5))
		conn.commit()
		conn.close()
		return "Post Successful!"



@app.route('/health/arm/<arm_num>', methods=['GET'])
def GET_health_attr(arm_num):
	""" Return specific health data """
	conn = sqlite3.connect(HEALTH_DB_PATH)
	c = conn.cursor()
	c.execute("SELECT * FROM HEALTH_SNAPSHOTS_ARM{} WHERE ID==((SELECT max(ID) FROM HEALTH_SNAPSHOTS_ARM{}));".format(arm_num, arm_num))
	conn.commit()
	content = c.fetchall()
	conn.close()
	return Response(str(content) , mimetype="text/plain")



@app.route('/run', methods=['POST'])

def run_post_query():

	if request.get_json() == None or request.headers['seq_num'] == None:
		 logging.error("Bad request was issued. No json was provided.")
		 abort(400) #Bad request, missing params.

	else:
		""" Set status """
		global status
		status = 1

		""" get json """
		feels_jsonf = request.get_json()
		seq_num = request.headers['seq_num']

		anger = feels_jsonf['anger']
		fear = feels_jsonf['fear']
		joy = feels_jsonf['joy']
		sadness = feels_jsonf['sadness']
		analytical = feels_jsonf['analytical']
		confident = feels_jsonf['confident']
		tentative = feels_jsonf['tentative']



		anger_pi = anger*100
		fear_pi = fear*100
		joy_pi = joy*100
		sadness_pi = sadness*100
		analytical_pi = analytical*100
		confident_pi = confident*100
		tentative_pi = tentative*100


		""" Convert feelings to actual arm parameters """
		all_the_feels = normalize(anger, fear, joy, sadness, analytical, confident, tentative)


		""" Update movement in DB"""
		dbconn = sqlite3.connect(QUERY_DB_PATH)
		db = dbconn.cursor()
		db.execute("INSERT INTO MOV_QUERIES VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (None, anger, sadness, confident, fear, joy, tentative, analytical))		
		dbconn.commit()
		dbconn.close()


		""" Convert feels to format for pi """
		pi_jsonf = feelings_to_json(all_the_feels)
		print(pi_jsonf)


		""" Update lights in DB """
		#light_parameters = json_to_light_parameters(pi_jsonf)
		#dbconn = sqlite3.connect(QUERY_DB_PATH)
		#db = dbconn.cursor()
		#db.execute("INSERT INTO LIGHT_QUERIES VALUES(?, ?, ?)", (None, light_parameters, seq_num))
		#dbconn.commit()
		#dbconn.close()

		""" run python code comment out when testing"""
		#result = subprocess.run("./LEDcontrol_main.py", stdout=subprocess.PIPE)
		#print(result.stdout)

		""" Run C-code, comment out if only testing api."""
		#result = subprocess.run(C_CODE_PATH, stdout=subprocess.PIPE)

		""" Movement done. Status to 0 again """
		status = 0

		return Response("Request successful!" , mimetype="text/plain")

@app.route('/run/status', methods=['GET'])

def get_status():
	global status
	return str(status)




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
