# How to run this POC

This sample application is modeled after the communication between C+D and the Scraper. Only dependency to get this sample up is Docker. Once docker is installed, running the given shell scripts will build and start the required application nodes as described below.

1.	Clone the Git repo of the POC from: https://github.com/pallewela/mq-poc.git

  It contains two directories:
  -	web: mocks the C+D application
  -	scraper: mocks the scraper

  Also, it contains a file named `run-rabbit.sh`

2. Create a new bridge network on docker named `test-network`. We create a network as we have multiple containers running on docker which would need to communicate with each other for the sample application to work.
```
docker network create test-network
```

3. Open a console and execute `run-rabbit.sh` file. This would start a RabbitMQ server in `test-network`.
```
sh run-rabbit.sh
```

4.	Now change the directory to `web` and start the C+D mock server.
```
cd web
sh buildandrun.sh
```
`buildandrun.sh` script builds the docker image for the C+D mock application (`ui.py`) and starts a container using that image.

5.	Open a console and start scraper nodes. `runnode.sh` inside the scraper directory could be used to start a new scraper node. Provide a unique number as a parameter so that docker containers names won’t conflict:
```
cd scraper
sh runnode.sh 1
sh runnode.sh 2 (on another console)
...
sh runnode.sh N (on another console)
```
Any number of scraper nodes can be run this way, provide a unique number is given as the parameter.

6.	Now browse to http://localhost:5000. It will show the simple mock C+D UI here which allows you to do a request to the mock scraper service. If the value entered in the input field is a number, the mock scraper service will simply sleep for the given number of **seconds**. Otherwise, it will sleep for 1 second.

7.	As scraper jobs are added through the UI, checking the consoles of each scraper node will show that these jobs get distributed among the nodes.

8.	The response of each scrape job is sent to a callback URL that C+D provided with the scraper job. This callback is is mocked as [http://test_ui:5000/scraper-callback/\<uuid\>](http://test_ui:5000/scraper-callback/\<uuid\>) on the C+D application (`ui.py`).
