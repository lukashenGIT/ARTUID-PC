  This api has several routes/views:

    GET /health: returns a json file of all arms and their motor temperatures.

    GET /health/arm/<arm_number>: returns temperatures of a specific arm

    POST /run The api expects a sequence number with key "seq_num" in the heder of the request and input data in the body of the format of the sample_json file included.

    GET /run/status Returns a 1 if the robot is performing a request. Otherwise 0.

  Files included should be:

    -../api.py
    -../helpers.py
    -../dummy_program.py
    -../Resources/ (folder will include api_log.log and main.db after first run of api)
    -../sample_json.py

  Before deployment, the IP addresses has to change from localhost to the interface connected to the LAN. This can be done by changing the -l option of api.py to -i <iface address>.

  Ports used:

    API - 9000
    DRIVER - 9001
    ...



  Non standard Dependencies (for python3):
    Python:
      * Flask
      * SQLite3
