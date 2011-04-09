
OPTS= -halt-on-error -file-line-error

CHAPTERS= theory_chapter/theory_chapter.tex \
	  tanc_chapter/tanc_chapter.tex\
	  backgrounds_chapter/backgrounds_chapter.tex

all: output/dissertation.pdf 

output/dissertation.pdf: output/dissertation.aux output/dissertation.bbl
	pdflatex ${OPTS} --output-directory=./output/ dissertation/dissertation.tex

output/dissertation.bbl: output/dissertation.aux
	rm -f log/bibtex.log
	bibtex output/dissertation  >& log/bibtex.log

output/dissertation.aux: dissertation/dissertation.tex 
	pdflatex ${OPTS} --output-directory=./output/ dissertation/dissertation.tex

output/dissertation.tex: ${CHAPTERS}

## Feynamn diagrams
#theory_chapter/theory_chapter.tex: theory_chapter/fermi_contact_interaction.pdf

#theory_chapter/fermi_contact_interaction.pdf: theory_chapter/fermi_contact_interaction.1
	#epstopdf $<

#theory_chapter/fermi_contact_interaction.1: theory_chapter/fermi_contact_interaction.mp
	#mpost $<
	#mv fermi_contact_interaction* theory_chapter/

#theory_chapter/fermi_contact_interaction.mp: theory_chapter/fermi_contact_interaction_diagram.tex
	#pdflatex --output-directory=theory_chapter/ $<
