docker kill test_scraper
docker rm test_scraper
docker run -it --network=test_bridge --name test_scraper codify.ai/scraper
#docker logs -f test_scraper
