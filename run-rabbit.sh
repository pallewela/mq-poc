docker kill test-rabbit
docker rm test-rabbit
docker run --rm --network=test_bridge -p5672:5672 --name test-rabbit -d rabbitmq:3
