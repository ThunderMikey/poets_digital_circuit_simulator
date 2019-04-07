GS:=graph_schema
JING = $(GS)/external/jing-20081028/bin/jing.jar

CPPFLAGS += -I $(GS)/include
CPPFLAGS += -W -Wall -Wno-unused-parameter -Wno-unused-variable
#CPPFLAGS += $(shell pkg-config --cflags libxml++-2.6)
CPPFLAGS += -std=c++11 -I/usr/include/libxml++-2.6 -I/usr/lib/x86_64-linux-gnu/libxml++-2.6/include -I/usr/include/libxml2 -I/usr/include/glibmm-2.4 -I/usr/lib/x86_64-linux-gnu/glibmm-2.4/include -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include -I/usr/include/sigc++-2.0 -I/usr/lib/x86_64-linux-gnu/sigc++-2.0/include
CPPFLAGS += -Wno-unused-local-typedefs
CPPFLAGS += -I providers
CPPFLAGS += -std=c++11 -g
CPPFLAGS += -O2 -fno-omit-frame-pointer -ggdb -DNDEBUG=1
SO_CPPFLAGS += -shared -fPIC
LDFLAGS += $(shell pkg-config --libs-only-L --libs-only-other libxml++-2.6)
LDFLAGS += -pthread
#LDLIBS += $(shell pkg-config --libs-only-l libxml++-2.6)
LDLIBS += -lxml++-2.6 -lxml2 -lglibmm-2.4 -lgobject-2.0 -lglib-2.0 -lsigc-2.0
LDLIBS += -ldl -fPIC

export PYTHONPATH = $(GS)/tools

# prefix
P:= docker run --rm -it \
  -v ${PWD}:/pdcs \
  -e LOCAL_USER_ID=$(shell id -u ${USER}) \
  tmikey/graph_schema

graphs bin sim_results providers netlists:
	mkdir -p $@

netlists/%.edif: yosys_scripts/%.ys | netlists
	scripts/yosys -s $<

graphs/%.xml: netlists/%.edif \
	graph_type/digital_circuit_simulator_graph_type.xml | graphs
	$P python3 scripts/edif_xml.py \
		-i $< \
		-o $@

$(GS)/bin/epoch_sim:
	$P ${MAKE} -C $(GS) bin/epoch_sim

bin/epoch_sim: $(GS)/bin/epoch_sim | bin
	ln -s ../$< $@

sim_results/%.log: graphs/%.xml bin/epoch_sim \
	providers/%.graph.so | sim_results
	$P bin/epoch_sim  --log-level 2 \
		$< \
		> $@ 2>&1

#demos/digital_circuit_simulator/digital_circuit_$1.xml
.PRECIOUS: providers/%.graph.so
providers/%.graph.so: providers/%.graph.cpp \
	providers/%.graph.hpp
	$P bash -c "g++ $(CPPFLAGS) -Wno-unused-but-set-variable $(SO_CPPFLAGS) $< \
		-o $@ $(LDFLAGS) $(LDLIBS)"

providers/%.graph.hpp: graphs/%.xml | providers
	$P sh -c "$(PYTHON) $(GS)/tools/render_graph_as_cpp.py --header < $< > providers/$*.graph.hpp"

providers/%.graph.cpp: graphs/%.xml $(JING) | providers
	$P java -jar $(JING) -c $(GS)/master/virtual-graph-schema-v2.1.rnc $<
	$P $(PYTHON) $(GS)/tools/render_graph_as_cpp.py $< \
		providers/$*.graph.cpp

$(JING): $(GS)/external/jing-20081028.zip
	cd $(<D) && unzip -o $(<F)
	touch $@

$(GS)/derived/virtual-graph-schema-v2.2.xsd:
	$P ${MAKE} -C $(GS) derived/$(@F)

graphs/%.checked: graphs/%.xml $(JING) \
	$(GS)/derived/virtual-graph-schema-v2.2.xsd
	$P java -jar $(JING) -c $(GS)/master/virtual-graph-schema-v2.2.rnc $<
	$P java -jar $(JING) $(GS)/derived/virtual-graph-schema-v2.2.xsd $<
	touch $@

.PHONY: clean
clean:
	-rm -r providers sim_results netlists graphs
