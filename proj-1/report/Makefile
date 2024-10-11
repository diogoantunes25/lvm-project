all: wipe main.pdf

%.pdf: %.tex
	make clean || true
	latexmk $<
	pdflatex $<
	make clean || true

wipe:
	rm *.pdf || true

clean:
	rm *.aux *.blg *.dvi *.bcf *.bbl *.fls *.log *.xml *.fdb_latexmk *.toc *.out *.xcp *.pdfsync
