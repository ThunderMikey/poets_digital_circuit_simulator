.PHONY: gs

uid:=$(shell id -u)

gs: graph_schema.docker entrypoint.sh
	docker build -f $< -t tmikey/graph_schema .

yosys_builder: yosys_builder.docker
	docker build -f $< -t tmikey/yosys_builder .

build_yosys: yosys_src
	docker run --rm -it \
		--user $(uid):$(uid) \
		-v $(shell pwd)/$<:/$< \
		tmikey/yosys_builder \
		make -C /$< -j4

doc_maker: doc_maker.docker
	docker build -f $< -t tmikey/$@ .

yosys: yosys.docker
	docker build -f $< -t tmikey/$@ .
