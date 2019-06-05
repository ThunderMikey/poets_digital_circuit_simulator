io_oracle_overview.pdf: inkscape_svg/io_oracle_overview.svg
	inkscape $< --export-pdf=$@
%.pdf: graphviz_src/%.gv
	dot -Tpdf $< -o $@

%.png: graphviz_src/%.gv
	dot -Tpng $< -o $@
