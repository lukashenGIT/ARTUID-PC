  This api has several views:
    /health: returns a json file of all health parameters.
    /health/<param>: returns a specific parameter of type <param>
    /query?params=<params>&id=<id>: Sends the parameters to the example_squidcom (temporarily) program and returns a response stating if the query was sucessful or not.
    The parameters should be an int that will be parsed by the example_squidcom.

  Files included should be:

    -...



  Ports used:

    API - 9000
    CALCULATIONS_APP - 9001
    ...



  Dependencies:
    Python:
      * Flask
      * Python3
      * SQLite3
      * ...

    Cpp:
      *...
