.PHONY: gs

uid:=$(shell id -u)

gs: graph_schema.docker entrypoint.sh
	docker build -f $< -t tmikey/graph_schema .

yosys_builder: yosys_builder.docker
	docker build -f $< -t tmikey/yosys_builder .

build_yosys:
	docker run --rm -it \
		--user $(uid):$(uid) \
		-v $(shell pwd)/yosys_src:/yosys_src \
		tmikey/yosys_builder \
		sh

yosys: yosys.docker
	docker build -f $< -t tmikey/$@ .
