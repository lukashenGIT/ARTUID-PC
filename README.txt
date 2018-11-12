  This api has several routes/views:

    GET /health: returns a json plaintext file of all health parameters.

    GET /health/<param>: returns a specific parameter of type <param>

    POST /health: Append a new entry to the health database (main.db) Parameters used as of now: heat, time_running, disturbances and vibrations as demonstration.
    Real scenario will most likely only be heat of different motors and time_running.

    GET /run?params=<params>&seq_num=<seq_num>: Sends the parameters queries db and returns a response stating if the query was sucessful or not.
    The parameters should be an int.
    This GET request query format does not follow standards and is only for demonstrative purposes. The POST method below should be used.

    POST /run Body should include parameters=<params> and seq_num=<seq_num>. This is used for posting data to the dummy program.

  Files included should be:

    -../api.py
    -../dummy_program.py
    -../Resources/ (folder will include api_log.log , health.db and queries.db after first run of api)

  Before deployment, the IP addresses has to change from localhost to the interface connected to the LAN. This can be done by changing the -l option of api.py to -i <iface address>.

  Ports used:

    API - 9000
    ...



  Non standard Dependencies (for python3):
    Python:
      * Flask
      * SQLite3 (Might be standard depending on version.)
