
OPTS= -halt-on-error -file-line-error

all: output/dissertation.pdf output/theory_chapter.pdf

output/dissertation.pdf: dissertation/dissertation.tex
	pdflatex ${OPTS} --output-directory=./output/ $<
	pdflatex ${OPTS} --output-directory=./output/ $<

output/theory_chapter.pdf: theory_chapter/theory_chapter.tex
	pdflatex ${OPTS} --output-directory=./output/ $<
	pdflatex ${OPTS} --output-directory=./output/ $<
