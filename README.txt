  This api has several routes/views:

    GET /health: returns a json file of all health parameters.

    GET /health/<param>: returns a specific parameter of type <param>

    POST /health: Append a new entry to the health database (main.db) Parameters used as of now: heat, time_running, disturbances and vibrations as demonstration.
    Real scenario will most likely only be heat of different motors and time_running.

    GET /run?params=<params>&id=<id>: Sends the parameters to the example_squidcom (temporarily) program and returns a response stating if the query was sucessful or not.
    The parameters should be an int that will be parsed by the example_squidcom.
    This GET request query format does not follow standards and is only for demonstrative purposes. The POST method below should be used.

    POST /run Should include parameters=<params> and id=<id>. This is used for posting data to the dummy program.

  Files included should be:

    -../api.py
    -../dummy_program.py
    -../Resources/ (folder will include api_log.log and main.db after first run of api)

  Before deployment, IP_IFACE has to be adjusted to the IPv4 of the used interface of the computer.

  Ports used:

    API - 9000
    CALCULATIONS_APP - 9001
    ...



  Dependencies:
    Python:
      * Flask
      * Python3
      * SQLite3
