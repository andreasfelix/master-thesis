.PHONY: all dist html print deploy

# pandoc-crossref has to be run before citeproc
# https://lierdakil.github.io/pandoc-crossref/#citeproc-and-pandoc-crossref
OPTIONS = chapters/*.md --defaults layout/options.yaml --filter pandoc-crossref --citeproc

all: html print README.md

dist:
	mkdir -p dist
	rsync -avu --delete figures layout/css layout/favicon.svg dist

html: dist
	pandoc $(OPTIONS) -o dist/index.html \
	--template layout/templates/index.html \
	--css css/ui.css \

print: dist
	pandoc $(OPTIONS) -o dist/print.html \
	--template layout/templates/print.html \
	--css css/interface.css \
	--css css/print.css \

README.md: layout/templates/README.md metadata.yaml
	echo | pandoc -o README.md --template layout/templates/README.md --metadata-file metadata.yaml

# running google-chrome in headless mode results in no hyphens and no links
pdf: print
	google-chrome http://127.0.0.1:8080/print.html \
	--headless \
	--disable-gpu \
	--print-to-pdf-no-header \
	--no-margins \
	--print-to-pdf=dist/thesis-headless.pdf \

.ONESHELL:
deploy: all
	url=git@github.com:$$(yq eval '[.github,.repository] | join("/")' metadata.yaml).git
	cd dist
	git init
	git add -A
	git commit -m 'deploy'
	# git's default branch name is subject to change, let's make it future-proof
	git branch -M main
	git push -f $$url main:gh-pages
