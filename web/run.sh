docker kill test_ui
docker rm test_ui
docker run --rm -it --network=test_bridge --name test_ui -d -p5000:5000 codify.ai/web 
docker logs -f test_ui
