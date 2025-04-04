
remove_test:
	docker rm $(docker ps -a | grep test | awk '{print $1}')

remove_images:
	docker images | awk '{print $3}'| xargs docker rmi -f


