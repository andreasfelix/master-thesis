SHELL := /bin/bash
.SHELLFLAGS := -O extglob -O globstar -c
.PHONY: dist pdf html tex epub deploy

dist:
	mkdir -p _dist
	# TODO: --delete also deletes .pdf images
	rsync -avu --delete figures layout/images layout/style.css _dist

# convert to pdf because latex cannot read svg
svg2pdf: $(patsubst %.svg, %.pdf, $(wildcard _dist/figures/*.svg))
	echo run all

_dist/figures/%.pdf: _dist/figures/%.svg
	rsvg-convert -f pdf -o $@ $<

html: dist
	pandoc content/!(_*).md \
	--standalone \
	-o _dist/index.html \
	--metadata title="Master Thesis" \
	--metadata link-citations \
	--bibliography bibliography.bib \
	--template layout/template.html \
	--css style.css \
	--number-sections \
	--csl layout/ieee.csl \
	--mathml \
	--filter pandoc-crossref \
	--filter pandoc-citeproc \
	--toc

pdf: dist
	pandoc content/*.md \
	-o _dist/thesis.pdf \
	--bibliography=bibliography.bib \
	--number-sections \
	--csl layout/ieee.csl \
	--metadata link-citations \
	--filter pandoc-crossref \
	--filter pandoc-citeproc \
	--verbose

tex: svg2pdf
	pandoc content/*.md \
	-o _dist/thesis.tex \
	--bibliography=bibliography.bib \
	-V fontsize=12pt \
	-V papersize=a4paper \
	-V documentclass=report \
	-N \
	--csl layout/ieee.csl \
	--pdf-engine=xelatex
	sed -i 's/.svg/.pdf/g' _dist/thesis.tex

epub: dist
	pandoc content/*.md \
	-o _dist/thesis.epub \
	--bibliography=bibliography.bib \
	--number-sections \
	--csl layout/ieee.csl \
	--filter pandoc-crossref \
	--filter pandoc-citeproc \
	--metadata title:"Felix Andreas" \
	--verbose

.ONESHELL:
deploy: html pdf
	cd _dist
	git init
	git add -A
	git commit -m 'deploy'
	git push -f git@github.com:andreasfelix/master-thesis.git master:gh-pages
	cd -
