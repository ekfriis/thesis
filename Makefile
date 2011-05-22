
OPTS= -halt-on-error -file-line-error

CHAPTERS= theory_chapter/theory_chapter.tex \
	  tanc_chapter/tanc_chapter.tex\
	  backgrounds_chapter/backgrounds_chapter.tex

DIAGRAMS := $(foreach file, $(basename $(wildcard output/*mp)), $(file).1)

all: output/dissertation.pdf  output/umi_abstract.pdf

output/dissertation.pdf: output/dissertation.aux output/dissertation.bbl 
	pdflatex ${OPTS} --output-directory=./output/ dissertation/dissertation.tex

output/dissertation.bbl: output/dissertation.aux
	bibtex output/dissertation  
	#pdflatex ${OPTS} --output-directory=./output/ dissertation/dissertation.tex

output/dissertation.aux: dissertation/dissertation.tex  ${DIAGRAMS}
	pdflatex ${OPTS} --output-directory=./output/ dissertation/dissertation.tex

output/dissertation.tex: ${CHAPTERS}

output/feynmp.1:
	true

output/umi_abstract.pdf: prelim/umi_abstract.tex
	pdflatex ${OPTS} --output-directory=./output/ $<
	pdflatex ${OPTS} --output-directory=./output/ $<

output/svfit_chapter.pdf: svfit_chapter/svfit_chapter.tex
	pdflatex ${OPTS} --output-directory=./output/ svfit_chapter/svfit_chapter.tex
	pdflatex ${OPTS} --output-directory=./output/ svfit_chapter/svfit_chapter.tex

output/results_chapter.pdf: results_chapter/results_chapter.tex
	pdflatex ${OPTS} --output-directory=./output/ $<
	pdflatex ${OPTS} --output-directory=./output/ $<

output/detector_chapter.pdf: detector_chapter/detector_chapter.tex
	pdflatex ${OPTS} --output-directory=./output/ $<
	pdflatex ${OPTS} --output-directory=./output/ $<


# Uncomment me if the files need to be recompiled
#output/%.1: output/%.mp
	#cd output/ && mpost $*

#output/nonperturbative_qcd_diagram.mp output/perturbative_qcd_diagram.mp output/muon_decay_propagator.mp output/muon_decay.mp: theory_chapter/theory_chapter.tex
