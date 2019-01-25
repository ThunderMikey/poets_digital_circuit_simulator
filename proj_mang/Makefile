reports:
	mkdir -p reports

u := $(shell id -u)
p := $(shell pwd)
reports/%.html: %.tjp reports
	#tj3 fyp.tjp -o reports
	docker run --rm --user $u:$u \
		-v $p:/proj_mang \
		tmikey/tj3 \
		tj3 /proj_mang/$< -o /proj_mang/reports

reports/before_interim_gantt.pdf: reports/before_interim.html tjreport.css
	cp tjreport.css reports/css/
	wkhtmltopdf -T 0 -B 0 -L 0 -R 0 --disable-smart-shrinking \
		$< $@

reports/before_interim_gantt_min.pdf: reports/before_interim_gantt.pdf
	pdfcrop $< $@
