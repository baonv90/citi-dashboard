Create your front-end elements in /frontend directory.

Prerequisites: Docker, docker-compose

Note: The provided back-end solution was built and tested on Linux.
We will not be able to provide guidance for Windows and/or Mac environments.

You can spin up the back-end with `docker-compose up`.

You can query the back-end programmatically at http://localhost:8010/devices
The route accepts an `n` query parameter, which determines the number 
of devices that will be generated, like so: http://localhost:8010/devices?n=10

You can also visit http://localhost:8010/docs for SwaggerUI API explorer.