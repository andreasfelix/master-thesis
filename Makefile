SHELL := /bin/bash
.SHELLFLAGS := -O extglob -O globstar -c
.PHONY: dist pdf html tex epub deploy

dist:
	mkdir -p dist
	rsync -avu --delete figures layout/images layout/css layout/js dist

tex-dir:
	mkdir -p _tex/figures

tex-pngs: tex-dir
	rsync -avu --delete --include "/*" --include "*.png" --exclude="*" figures _tex

tex-pdfs: tex-dir $(patsubst figures/%.svg, _tex/figures/%.pdf, $(wildcard figures/*.svg))

_tex/figures/%.pdf: figures/%.svg
	rsvg-convert -f pdf -o $@ $<

html: dist
	pandoc content/!(_*).md \
	--standalone \
	-o dist/index.html \
	--metadata-file metadata.yml \
	--bibliography bibliography.bib \
	--template layout/template.html \
	--css css/variables.css \
	--css css/ui.css \
	--css css/page.css \
	--section-divs \
	--number-sections \
	--csl layout/ieee.csl \
	--mathml \
	--filter pandoc-crossref \
	--filter pandoc-citeproc \
	--toc

print: dist
	pandoc content/!(_*).md \
	--standalone \
	-o dist/print.html \
	--metadata-file metadata.yml \
	--bibliography bibliography.bib \
	--template layout/template-print.html \
	--css css/variables.css \
	--css css/page.css \
	--css css/print.css \
	--css css/ressources_interface-0.1.css \
	--number-sections \
	--section-divs \
	--csl layout/ieee.csl \
	--mathml \
	--filter pandoc-crossref \
	-M chapters \
	--filter pandoc-citeproc \
	--toc

pdf-pandoc: dist
	pandoc content/*.md \
	-o dist/thesis.pdf \
	--bibliography=bibliography.bib \
	--number-sections \
	--csl layout/ieee.csl \
	--metadata link-citations \
	--filter pandoc-crossref \
	--filter pandoc-citeproc \
	--verbose

tex: dist tex-pdfs tex-pngs
	pandoc content/*.md \
	--standalone \
	-o _tex/thesis.tex \
	--bibliography=bibliography.bib \
	-V fontsize=12pt \
	-V papersize=a4paper \
	-V documentclass=report \
	-N \
	--csl layout/ieee.csl \
	--filter pandoc-crossref \
	--filter pandoc-citeproc \
	--toc
	sed -i 's/.svg/.pdf/g' _tex/thesis.tex
	cd _tex; latexmk -pdf thesis.tex
	mv thesis.pdf ../dist/thesis-tex.pdf

epub: dist
	pandoc content/*.md \
	-o dist/thesis.epub \
	--bibliography=bibliography.bib \
	--number-sections \
	--csl layout/ieee.csl \
	--filter pandoc-crossref \
	--filter pandoc-citeproc \
	--verbose

.ONESHELL:
deploy: html
	cd dist
	git init
	git add -A
	git commit -m 'deploy'
	git push -f git@github.com:andreasfelix/master-thesis.git master:gh-pages
	cd -
