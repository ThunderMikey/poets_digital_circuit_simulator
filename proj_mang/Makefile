u := $(shell id -u)
p := $(shell pwd)

ifeq (${USE_DOCKER}, 1)
pf := docker run --rm --user $u:$u -v $p:/docs tmikey/doc_maker
else
pf :=
endif

reports:
	mkdir -p reports

reports/%.html: %.tjp tasks.tji resource_mike.tji | reports
	#tj3 fyp.tjp -o reports
	docker run --rm --user $u:$u \
		-v $p:/proj_mang \
		tmikey/tj3 \
		tj3 /proj_mang/$< -o /proj_mang/reports

reports/before_interim_gantt.pdf: reports/before_interim.html tjreport.css
	cp tjreport.css reports/css/
	${pf} wkhtmltopdf -T 0 -B 0 -L 0 -R 0 --disable-smart-shrinking \
		$< $@

reports/before_interim_gantt_min.pdf: reports/before_interim_gantt.pdf
	${pf} pdfcrop $< $@

reports/after_interim_gantt.pdf: reports/after_interim.html tjreport.css
	cp tjreport.css reports/css/
	${pf} wkhtmltopdf -T 0 -B 0 -L 0 -R 0 --disable-smart-shrinking \
		$< $@

reports/after_interim_gantt_min.pdf: reports/after_interim_gantt.pdf
	${pf} pdfcrop $< $@
