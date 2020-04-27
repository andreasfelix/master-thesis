.PHONY: pdf html

pdf:
	pandoc content/*.md \
	-o _dist/thesis.pdf \
	--bibliography=content/bibliography.bib \
	--number-sections \
	--verbose

html:
	pandoc content/*.md \
	-o _dist/thesis.html \
	--metadata title="Master Thesis" \
	--bibliography=content/bibliography.bib \
	--highlight-style=pygments \
	--template=layout/layout.html \
	--standalone \
	--number-sections \
	--filter pandoc-crossref \
	--toc

