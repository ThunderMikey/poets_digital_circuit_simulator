

$(eval $(call provider_rules_template,number_tree))

define number_tree_instance_template
# $1 = D_B  (depth and branching)
# $2 = max-steps
# $3 = filters
# $4 = add to demo

demos/number_tree/number_tree_$1.xml : apps/number_tree/create_number_tree_instance.py
	mkdir -p $$(dir $$@)
	$$(PYTHON) apps/number_tree/create_number_tree_instance.py  $$(subst _, ,$1) > $$@

demos/number_tree/number_tree_$1.snap : demos/number_tree/number_tree_$1.xml bin/epoch_sim providers/number_tree.graph.so demos/number_tree/number_tree_$1.checked
	bin/epoch_sim  --log-level 0 --max-steps $2 --snapshots 1 $$@  demos/number_tree/number_tree_$1.xml

ALL_NUMBER_TREE_TESTS += demos/number_tree/number_tree_$1.snap

ifneq ($4,)

demos/number_tree/number_tree_$1.mp4 : demos/number_tree/number_tree_$1.xml demos/number_tree/number_tree_$1.snap number_tree_provider
	mkdir -p demos/number_tree/number_tree_$1.tmp
	$(PYTHON) tools/render_graph_as_dot.py demos/number_tree/number_tree_$1.xml --snapshots demos/number_tree/number_tree_$1.snap --output demos/number_tree/number_tree_$1.tmp/out $3
	(cd demos/number_tree/number_tree_$1.tmp/  &&  for i in *.dot; do echo $$$$i; neato -Nlabel="" -Gsize=5,5\! -Gdpi=100 -Tpng $$$$i > $$$$i.png; done )
	#(cd demos/number_tree/number_tree_$1.tmp/  && convert -delay 20 -loop 0 *.dot.png ../../number_tree_$1.gif)
	$(FFMPEG) -y -r 10 -i demos/number_tree/number_tree_$1.tmp/out_%06d.dot.png -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -crf 18 demos/number_tree/number_tree_$1.mp4


ALL_NUMBER_TREE_DEMOS +=  demos/number_tree/number_tree_$1.mp4

endif

$(eval $(call softswitch_instance_template,number_tree_$1,demos/number_tree/number_tree_$1.xml,1))
$(eval $(call softswitch_instance_template,number_tree_$1,demos/number_tree/number_tree_$1.xml,4))
$(eval $(call softswitch_instance_template,number_tree_$1,demos/number_tree/number_tree_$1.xml,16))
$(eval $(call softswitch_instance_template,number_tree_$1,demos/number_tree/number_tree_$1.xml,32))
$(eval $(call softswitch_instance_template,number_tree_$1,demos/number_tree/number_tree_$1.xml,64))
$(eval $(call softswitch_instance_template,number_tree_$1,demos/number_tree/number_tree_$1.xml,128))
$(eval $(call softswitch_instance_template,number_tree_$1,demos/number_tree/number_tree_$1.xml,256))
$(eval $(call softswitch_instance_template,number_tree_$1,demos/number_tree/number_tree_$1.xml,512))

endef

NUMBER_TREE_FILTERS = \
	--bind-dev "branch" "state" "status" "color" "'gray' if value==0 else 'green' if value==1 else 'red'" \
	--bind-dev "leaf" "rts" "-" "color" "'red' if value>0 else 'green'" \

$(eval $(call number_tree_instance_template,8_3,50,$(NUMBER_TREE_FILTERS)))
$(eval $(call number_tree_instance_template,8_2,50,$(NUMBER_TREE_FILTERS)))
$(eval $(call number_tree_instance_template,6_3,50,$(NUMBER_TREE_FILTERS)))
$(eval $(call number_tree_instance_template,4_4,50,$(NUMBER_TREE_FILTERS),1))

number_tree_tests : $(ALL_NUMBER_TREE_TESTS)

number_tree_demos : $(ALL_NUMBER_TREE_DEMOS)

ALL_DEMOS += number_tree_demos

ALL_TESTS += number_tree_tests

# vim:ft=make:
