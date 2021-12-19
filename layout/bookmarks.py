from typing import List
import re
from itertools import dropwhile
from pathlib import Path

import fitz

base_dir = Path(__file__).parent.parent / "dist"
pdf_path = base_dir / "thesis.pdf"
pdf = fitz.open(pdf_path)
pattern = re.compile(r"\s+")

# get chapter names
chapters = ["Abstract", "Acknowledgments", "Contents"]
last_prefix = "0.0.0"
for page in pdf.pages(6, 9):
    blocks = page.get_text("blocks")
    texts: List[str] = [block[4] for block in blocks]
    for text in dropwhile(lambda text: text.count("\n") < 2, texts):
        *chapter, page, empty = text.split("\n")
        chapter = " ".join(chapter)
        chapters.append(chapter)
        # run some checks
        assert int(page)
        assert empty == ""
        prefix = chapter.split(maxsplit=1)[0]
        if prefix != "Bibliography":
            assert prefix.split(".") > last_prefix.split(".")
            last_prefix = prefix

# cleanup chapter names
chapters = [pattern.sub(" ", chapter).strip() for chapter in chapters]

# search for first occurence and store page number
toc = [[1, "Title Page", 1, 0]]
pages = pdf.pages()
page = next(pages)
text = page.get_text()
for chapter in chapters:
    while pattern.sub("", chapter) not in pattern.sub("", text):
        page = next(pages)
        text = page.get_text()

    entry = [chapter.count(".") + 1, chapter.replace(" ", " "), page.number + 1, 0]
    print(entry)
    toc.append(entry)
    # as contents contains all chapter names we must skip this page
    if chapter == "Contents":
        page = next(pages)
        text = page.get_text()

# write toc to pdf
pdf.set_toc(toc)
pdf.set_page_labels(
    [
        {"startpage": 0, "prefix": "", "style": "", "firstpagenum": 0},
        {"startpage": 2, "prefix": "", "style": "r", "firstpagenum": 1},
        {"startpage": toc[4][2] - 1, "prefix": "", "style": "D", "firstpagenum": 1},
    ]
)

# set metadata
from yaml import load, Loader

with open("metadata.yaml") as file:
    metadata = load(file, Loader=Loader)

# remove non-breakable spaces from title
pdf.metadata["title"] = metadata["title"].replace("\xa0", " ")
pdf.metadata["author"] = metadata["author"]
pdf.set_metadata(pdf.metadata)

pdf.saveIncr()
