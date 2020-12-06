# MAKEFILE https://github.com/tstelzle/GameStatPlotter
# AUTHORS: Tarek Stelzle

IMAGE-NAME := python-env-game_stat_plotter
CONTAINER-NAME := game_stat_plotter
MOUNT-DIR := $(PWD)
GAME := skat
DAY := ''
RUN := docker exec -it -w /usr/src $(CONTAINER-NAME) python main.py -g=$(GAME) -d=$(DAY)
RUN-COUNTER := docker exec -it -w /usr/src $(CONTAINER-NAME) python main.py -g=$(GAME) -c -d=$(DAY)
IGNORE-OUTPUT := > /dev/null 2>&1

.PHONY: default build-image container run run-master

default:
	 @echo "Possible Commands:"
	 @echo " build-image     - Builds the image."
	 @echo " container       - Runs the container."
	 @echo " run             - Runs the main file of the 'GameStatPlotter' repository (change GAME and DAY paramter)."
	 @echo " run-counter     - Runs the main file of the 'GameStatPlotter' repository with the counter parameter set (change GAME and DAY parameter)."

build-image:
	docker build -t $(IMAGE-NAME) .

container:
	docker run -d -t --rm -v $(MOUNT-DIR):/usr/src --name $(CONTAINER-NAME) $(IMAGE-NAME)

run:
	$(RUN)

run-counter:
	$(RUN-COUNTER)

ssh:
	docker exec -it $(CONTAINER-NAME) bash
