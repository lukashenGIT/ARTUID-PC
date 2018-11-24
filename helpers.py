import sqlite3
import json

def json_to_light_parameters(json_file):

	out = ""
	""" light data """
	for arm in range(7):
		if arm == 0:
			pass
		else:
			out += str(json_file['light_parameters']['arm{}'.format(arm)]['delay']) + ";"
			for link in range(4):
				if link == 0:
					pass
				else:
					out += str(json_file['light_parameters']['arm{}'.format(arm)]['link{}'.format(link)]['pattern']) + ";"
					out += str(json_file['light_parameters']['arm{}'.format(arm)]['link{}'.format(link)]['color']) + ";"
					out += str(json_file['light_parameters']['arm{}'.format(arm)]['link{}'.format(link)]['bg']) + ";"
					out += str(json_file['light_parameters']['arm{}'.format(arm)]['link{}'.format(link)]['dir']) + ";"
					out += str(json_file['light_parameters']['arm{}'.format(arm)]['link{}'.format(link)]['size']) + ";"


	
	return out


def update_move_db(jsonf, dbcur):
	seq_num = jsonf["seq_num"]

	for arm in range(1,7):
		traveldistance = jsonf['move_parameters']["arm{}".format(arm)]["traveldistance"]
		radius = jsonf['move_parameters']["arm{}".format(arm)]["radius"]
		weight_1 = jsonf['move_parameters']["arm{}".format(arm)]["weight_1"]
		weight_2 = jsonf['move_parameters']["arm{}".format(arm)]["weight_2"]
		weight_3 = jsonf['move_parameters']["arm{}".format(arm)]["weight_3"]
		weight_4 = jsonf['move_parameters']["arm{}".format(arm)]["weight_4"]
		weight_5 = jsonf['move_parameters']["arm{}".format(arm)]["weight_5"]
		weight_6 = jsonf['move_parameters']["arm{}".format(arm)]["weight_6"]
		dbcur.execute("INSERT INTO MOV_QUERIES_ARM{} VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);".format(arm), (None, traveldistance, radius, weight_1, weight_2, weight_3, weight_4, weight_5, weight_6, seq_num))



def make_dbs():
	""" Set up db params and path. """
	HEALTH_DB_PATH = './Resources/health.db'
	QUERY_DB_PATH = './Resources/queries.db'

	""" All the temperature tables """
	conn = sqlite3.connect(HEALTH_DB_PATH)
	c = conn.cursor()
	for arm in range(1, 7):
		c.execute("CREATE TABLE IF NOT EXISTS HEALTH_SNAPSHOTS_ARM{}(ID integer PRIMARY KEY AUTOINCREMENT, datetime_added text NOT NULL, heat_motor1 integer NOT NULL, heat_motor2 integer NOT NULL, heat_motor3 integer NOT NULL, heat_motor4 integer NOT NULL, heat_motor5 integer NOT NULL);".format(arm))
	conn.commit()
	conn.close()

	""" All the mocement tables """
	conn = sqlite3.connect(QUERY_DB_PATH)
	c = conn.cursor()
	for arm in range(1, 7):
		c.execute("CREATE TABLE IF NOT EXISTS MOV_QUERIES_ARM{}(ID integer PRIMARY KEY AUTOINCREMENT, traveldistance integer NOT NULL,radius integer NOT NULL, weight_1 integer NOT NULL ,weight_2 integer NOT NULL ,weight_3 integer NOT NULL ,weight_4 integer NOT NULL ,weight_5 integer NOT NULL ,weight_6 integer NOT NULL ,seq_num integer NOT NULL);".format(arm))
		c.execute("CREATE TABLE IF NOT EXISTS LIGHT_QUERIES(ID integer PRIMARY KEY AUTOINCREMENT, light_parameters text NOT NULL, seq_num integer NOT NULL);")
	conn.commit()
	conn.close()

