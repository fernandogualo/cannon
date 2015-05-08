#!/usr/bin/make -f
# -*- mode:makefile -*-

run-container:
	python ./container.py --Ice.Config=container.config | tee proxy_container.out 

run-processor:

	for number in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25; do \
		./processor.py --Ice.Config=processor.config "$(shell head -1 proxy_container.out)" &  \
    done

run-frontend:
	python ./frontend.py --Ice.Config=frontend.config "$(shell head -1 proxy_container.out)" | tee proxy_frontend.out

run-client:
	python ./client.py --Ice.MessageSizeMax=25800000 "$(shell head -1 proxy_frontend.out)"
	killall -I python

clean:
	rm -f *~ proxy*.out core *.pyc

run-test:
	nosetests test/
