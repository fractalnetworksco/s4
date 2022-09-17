.PHONY: docker


docker:
	docker build -t fractalnetworks/s4:local .

# docker for desktop shell
# mount /var/lib/docker from docker for desktop vm
# mount s4 code to /code
volume:
	docker run --privileged --workdir /code/s4 -v `pwd`:/code -v /var/lib/fractal:/var/lib/fractal --rm -it --entrypoint /code/s4/s4.py fractalnetworks/s4:local create_volume /var/lib/fractal/$(NAME) 1G
loopback:
	docker run --privileged --rm -it --pid=host fractalnetworks/s4:local nsenter -t 1 -m -u -n -i losetup -fP /var/lib/fractal/$(NAME)


# useful for debugging
losetup:
	docker run --privileged --rm -it --pid=host fractalnetworks/s4:local nsenter -t 1 -m -u -n -i losetup -J
nsenter:
	docker run --privileged --rm -it --pid=host fractalnetworks/s4:local nsenter -t 1 -m -u -n -i bash