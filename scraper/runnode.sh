container="test_scraper_${1}"
echo ${container}
docker kill ${container}
docker rm ${container}
docker run -it -d --rm --network=test-network --name ${container} codify.ai/scraper
docker logs -f ${container}
