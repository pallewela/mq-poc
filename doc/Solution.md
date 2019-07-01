![Current State](https://github.com/pallewela/mq-poc/raw/master/doc/c1.png)

Currently when multiple requests are made simultaneously, scraper node will create parallel jobs in multiple thread. This could be a problem when the number of parallel jobs goes beyond what a single node can handle. To scale better, a straight forward solution is to add a load balancer and distributing the load across multiple scraper nodes. As the number of expected parallel scraper jobs go higher, it’s possible to add more scraper nodes to handle the increased load. Addition/removal of new nodes will need to be configured in the load balancer.

![Load Balancer](https://github.com/pallewela/mq-poc/raw/master/doc/c2.png)

Yet another approach to distributing load is to use a message queue, with which, it would not require as many nodes to serve peak load (depending on the response time requirements). In this solution, instead of sending a request, C+D will enqueue a message containing the request into a message queue (MQ). Here it’s assumed that C+D resides in the same network as scraper node is. If C+D has to be communicating in HTTP, it is possible to use a http binding to post messages to an MQ. Scraper can invoke the callback url with the response once it has completed the scraper job.

![MQ](https://github.com/pallewela/mq-poc/raw/master/doc/c3.png)

With this approach, each new scraper instance will register with the MQ as it comes online. It can be ensured that the MQ delivers messages to each node fairly, and only after it has completed the last scraper job. Ideally, if the response time doesn’t matter, as far as the peak boost of requests for scraper jobs do not go beyond the queue’s capacity, it should be possible to run the system with just a single scraper instance running.

We can run as many parallel jobs in a single node as it can handle. Also, there is no need for the configuration to be managed centrally as in the case of the load balancer, as it is the scraper that must register itself as a consumer with the MQ.

There are many options for the choice of MQ such as RabbitMQ, Amazon SQS, ActiveMQ (AmazonMQ) etc. In the demo I’ve used RabbitMQ as it’s easy to work with.

It is also possible to improve on the response callback webhook with this approach. Instead, it is possible to post the results from scraper to a different queue in MQ and C+D can be consuming that queue to consume the responses. 
