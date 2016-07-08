
.PHONY: default
default: build

.PHONY: build
build:
	./init.sh

.PHONY: clean
clean:
	rm -rf WustScript
	rm -rf stl.txt
	rm -rf *.log

