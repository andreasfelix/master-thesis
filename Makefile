SHELL := /bin/bash
.SHELLFLAGS := -O extglob -O globstar -c
.PHONY: dist pdf html tex epub deploy

dist:
	mkdir -p _dist
	rsync -avu --delete figures layout/images layout/style.css _dist

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

# pdf: dist
# 	pandoc content/*.md \
# 	-o _dist/thesis.pdf \
# 	--bibliography=bibliography.bib \
# 	--number-sections \
# 	--csl layout/ieee.csl \
# 	--metadata link-citations \
# 	--filter pandoc-crossref \
# 	--filter pandoc-citeproc \
# 	--verbose

tex: dist tex-pdfs tex-pngs
	pandoc content/*.md \
	--standalone \
	-o _tex/thesis.tex \
	--bibliography=../bibliography.bib \
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
	mv thesis.pdf ../_dist/thesis-tex.pdf

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
deploy: html
	cd _dist
	git init
	git add -A
	git commit -m 'deploy'
	git push -f git@github.com:andreasfelix/master-thesis.git master:gh-pages
	cd -
