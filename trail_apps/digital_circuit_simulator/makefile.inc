

$(eval $(call provider_rules_template,digital_circuit_simulator))

define digital_circuit_simulator_instance_template
# $1 = D_B  (depth and branching)
# $2 = max-steps
# $3 = filters
# $4 = add to demo

demos/digital_circuit_simulator/digital_circuit_$1.xml : apps/digital_circuit_simulator/create_digital_circuit_instance.py
	mkdir -p $$(dir $$@)
	$$(PYTHON) \
		apps/digital_circuit_simulator/create_digital_circuit_instance.py \
		$1 > $$@

demos/digital_circuit_simulator/digital_circuit_$1.snap : \
	demos/digital_circuit_simulator/digital_circuit_$1.xml \
	bin/epoch_sim \
	providers/digital_circuit_simulator.graph.so \
	demos/digital_circuit_simulator/digital_circuit_$1.checked
	bin/epoch_sim  --log-level 0 --max-steps $2 --snapshots 1 $$@  demos/digital_circuit_simulator/digital_circuit_$1.xml

ALL_DIGITAL_CIRCUIT_SIMULATOR_TESTS += \
	demos/digital_circuit_simulator/digital_circuit_$1.snap

ifneq ($4,)

demos/digital_circuit_simulator/digital_circuit_$1.mp4 : demos/digital_circuit_simulator/digital_circuit_$1.xml demos/digital_circuit_simulator/digital_circuit_$1.snap number_tree_provider
	mkdir -p demos/digital_circuit_simulator/digital_circuit_$1.tmp
	$(PYTHON) tools/render_graph_as_dot.py demos/digital_circuit_simulator/digital_circuit_$1.xml --snapshots demos/digital_circuit_simulator/digital_circuit_$1.snap --output demos/digital_circuit_simulator/digital_circuit_$1.tmp/out $3
	(cd demos/digital_circuit_simulator/digital_circuit_$1.tmp/  &&  for i in *.dot; do echo $$$$i; neato -Nlabel="" -Gsize=5,5\! -Gdpi=100 -Tpng $$$$i > $$$$i.png; done )
	#(cd demos/digital_circuit_simulator/digital_circuit_$1.tmp/  && convert -delay 20 -loop 0 *.dot.png ../../digital_circuit_$1.gif)
	$(FFMPEG) -y -r 10 -i demos/digital_circuit_simulator/digital_circuit_$1.tmp/out_%06d.dot.png -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -crf 18 demos/digital_circuit_simulator/digital_circuit_$1.mp4


ALL_DIGITAL_CIRCUIT_SIMULATOR_DEMOS += \
	demos/digital_circuit_simulator/digital_circuit_$1.mp4

endif

$(eval $(call softswitch_instance_template,digital_circuit_$1,demos/digital_circuit_simulator/digital_circuit_$1.xml,1))
$(eval $(call softswitch_instance_template,digital_circuit_$1,demos/digital_circuit_simulator/digital_circuit_$1.xml,4))
$(eval $(call softswitch_instance_template,digital_circuit_$1,demos/digital_circuit_simulator/digital_circuit_$1.xml,16))
$(eval $(call softswitch_instance_template,digital_circuit_$1,demos/digital_circuit_simulator/digital_circuit_$1.xml,32))
$(eval $(call softswitch_instance_template,digital_circuit_$1,demos/digital_circuit_simulator/digital_circuit_$1.xml,64))
$(eval $(call softswitch_instance_template,digital_circuit_$1,demos/digital_circuit_simulator/digital_circuit_$1.xml,128))
$(eval $(call softswitch_instance_template,digital_circuit_$1,demos/digital_circuit_simulator/digital_circuit_$1.xml,256))
$(eval $(call softswitch_instance_template,digital_circuit_$1,demos/digital_circuit_simulator/digital_circuit_$1.xml,512))

endef

DIGITAL_CIRCUIT_SIMULATOR_FILTERS = \
	--bind-dev "branch" "state" "status" "color" "'gray' if value==0 else 'green' if value==1 else 'red'" \
	--bind-dev "leaf" "rts" "-" "color" "'red' if value>0 else 'green'" \

$(eval $(call digital_circuit_simulator_instance_template,typical,200,$(DIGITAL_CIRCUIT_SIMULATOR_FILTERS),1))

digital_circuit_simulator_tests : $(ALL_DIGITAL_CIRCUIT_SIMULATOR_TESTS)

digital_circuit_simulator_demos : $(ALL_DIGITAL_CIRCUIT_SIMULATOR_DEMOS)

ALL_TESTS += digital_circuit_simulator_tests

ALL_DEMOS += digital_circuit_simulator_demos


# vim:ft=make:
