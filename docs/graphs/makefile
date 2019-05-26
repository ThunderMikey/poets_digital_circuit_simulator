io_oracle_overview.pdf: inkscape_svg/io_oracle_overview.svg
	inkscape $< --export-pdf=$@
%.pdf: %.gv
	dot -Tpdf $< -o $@

%.png: %.gv
	dot -Tpng $< -o $@
