JING = graph_schema/external/jing-20081028/bin/jing.jar

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
	$P bin/epoch_sim  --log-level 0 --max-steps 100 \
		$< \
		> $@

#demos/digital_circuit_simulator/digital_circuit_$1.xml \
#providers/digital_circuit_simulator.graph.so

$(JING): graph_schema/external/jing-20081028.zip
	cd $(<D) && unzip -o $(<F)
	touch $@

graphs/%.checked: graphs/%.xml $(JING)
	$P java -jar $(JING) -c graph_schema/master/virtual-graph-schema-v2.2.rnc $<
	$P java -jar $(JING) derived/virtual-graph-schema-v2.2.xsd $<
	touch $@
