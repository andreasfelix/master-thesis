.PHONY: dist pdf html deploy

dist:
	mkdir -p _dist

# TODO: use MathML once supported in chrome
html: dist
	pandoc content/*.md \
	-o _dist/index.html \
	--metadata title="Master Thesis" \
	--bibliography=bibliography.bib \
	--highlight-style=pygments \
	--template=layout/layout.html \
	--standalone \
	--number-sections \
	--csl layout/ieee.csl \
	--metadata link-citations \
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
	--filter pandoc-xnos \
	--filter pandoc-crossref \
	--filter pandoc-citeproc \
	--verbose

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
