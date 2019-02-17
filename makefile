
# prefix
P:=./run_docker.sh

graphs:
	mkdir -p $@

bin:
	mkdir -p $@

sim_results:
	mkdir -p $@

netlists/%.edif: yosys_scripts/%.ys
	scripts/yosys -s $<

graphs/%.xml: netlists/%.edif | graphs
	$P python3 scripts/edif_xml.py \
		-i $< \
		-o $@

graph_schema/bin/epoch_sim:
	$P ${MAKE} -C graph_schema bin/epoch_sim

bin/epoch_sim: graph_schema/bin/epoch_sim | bin
	ln -s ../$< $@

sim_results/%.log: graphs/%.xml bin/epoch_sim | sim_results
	$P bin/epoch_sim $< > $@
