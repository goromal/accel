import os, shutil, subprocess

_build_str = """####################################################################################################
# Configuration
####################################################################################################

# Build configuration

BUILD = build
MAKEFILE = Makefile
OUTPUT_FILENAME = book
METADATA = metadata.yml
CHAPTERS = chapters/*.md
TOC = --toc --toc-depth 2
METADATA_ARGS = --metadata-file $(METADATA)
IMAGES = $(shell find images -type f)
TEMPLATES = $(shell find templates/ -type f)
COVER_IMAGE = images/cover.png
MATH_FORMULAS = --webtex

# Chapters content
CONTENT = awk 'FNR==1 && NR!=1 {print "\\n\\n"}{print}' $(CHAPTERS)
CONTENT_FILTERS = tee # Use this to add sed filters or other piped commands

# Debugging

# DEBUG_ARGS = --verbose

# Pandoc filtes - uncomment the following variable to enable cross references filter. For more
# information, check the "Cross references" section on the README.md file.

# FILTER_ARGS = --filter pandoc-crossref

# Combined arguments

ARGS = $(TOC) $(MATH_FORMULAS) $(METADATA_ARGS) $(FILTER_ARGS) $(DEBUG_ARGS)
	
PANDOC_COMMAND = pandoc

# Per-format options

DOCX_ARGS = --standalone --reference-doc templates/docx.docx
EPUB_ARGS = --template templates/epub.html --epub-cover-image $(COVER_IMAGE)
HTML_ARGS = --template templates/html.html --standalone --to html5
PDF_ARGS = --template templates/pdf.latex --pdf-engine xelatex

# Per-format file dependencies

BASE_DEPENDENCIES = $(MAKEFILE) $(CHAPTERS) $(METADATA) $(IMAGES) $(TEMPLATES)
DOCX_DEPENDENCIES = $(BASE_DEPENDENCIES)
EPUB_DEPENDENCIES = $(BASE_DEPENDENCIES)
HTML_DEPENDENCIES = $(BASE_DEPENDENCIES)
PDF_DEPENDENCIES = $(BASE_DEPENDENCIES)

####################################################################################################
# Basic actions
####################################################################################################

all:	book

book:	epub html pdf docx

clean:
	rm -r $(BUILD)

####################################################################################################
# File builders
####################################################################################################

epub:	$(BUILD)/epub/$(OUTPUT_FILENAME).epub

html:	$(BUILD)/html/$(OUTPUT_FILENAME).html

pdf:	$(BUILD)/pdf/$(OUTPUT_FILENAME).pdf

docx:	$(BUILD)/docx/$(OUTPUT_FILENAME).docx

$(BUILD)/epub/$(OUTPUT_FILENAME).epub:	$(EPUB_DEPENDENCIES)
	mkdir -p $(BUILD)/epub
	$(CONTENT) | $(CONTENT_FILTERS) | $(PANDOC_COMMAND) $(ARGS) $(EPUB_ARGS) -o $@
	@echo "$@ was built"

$(BUILD)/html/$(OUTPUT_FILENAME).html:	$(HTML_DEPENDENCIES)
	mkdir -p $(BUILD)/html
	$(CONTENT) | $(CONTENT_FILTERS) | $(PANDOC_COMMAND) $(ARGS) $(HTML_ARGS) -o $@
	cp --parent $(IMAGES) $(BUILD)/html/
	@echo "$@ was built"

$(BUILD)/pdf/$(OUTPUT_FILENAME).pdf:	$(PDF_DEPENDENCIES)
	mkdir -p $(BUILD)/pdf
	$(CONTENT) | $(CONTENT_FILTERS) | $(PANDOC_COMMAND) $(ARGS) $(PDF_ARGS) -o $@
	@echo "$@ was built"

$(BUILD)/docx/$(OUTPUT_FILENAME).docx:	$(DOCX_DEPENDENCIES)
	mkdir -p $(BUILD)/docx
	$(CONTENT) | $(CONTENT_FILTERS) | $(PANDOC_COMMAND) $(ARGS) $(DOCX_ARGS) -o $@
	@echo "$@ was built"
"""

_template_str = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"$if(lang)$ xml:lang="$lang$"$endif$>
<head>
  <meta charset="utf-8" />
  <meta name="generator" content="pandoc" />
  <title>$pagetitle$</title>
$if(highlighting-css)$
  <style>
$highlighting-css$
$style.css()$
  </style>
$endif$
$for(css)$
  <link rel="stylesheet" type="text/css" href="$css$" />
$endfor$
$for(header-includes)$
  $header-includes$
$endfor$
</head>
<body$if(coverpage)$ id="cover"$endif$$if(body-type)$ epub:type="$body-type$"$endif$>
$if(titlepage)$
<section epub:type="titlepage" class="titlepage">
$for(title)$
$if(title.type)$
  <h1 class="$title.type$">$title.text$</h1>
$else$
  <h1 class="title">$title$</h1>
$endif$
$endfor$
$if(subtitle)$
  <p class="subtitle">$subtitle$</p>
$endif$
$for(author)$
  <p class="author">$author$</p>
$endfor$
$for(creator)$
  <p class="$creator.role$">$creator.text$</p>
$endfor$
$if(publisher)$
  <p class="publisher">$publisher$</p>
$endif$
$if(date)$
  <p class="date">$date$</p>
$endif$
$if(rights)$
  <div class="rights">$rights$</div>
$endif$
</section>
$else$
$if(coverpage)$
<div id="cover-image">
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="100%" height="100%" viewBox="0 0 $cover-image-width$ $cover-image-height$" preserveAspectRatio="none">
<image width="$cover-image-width$" height="$cover-image-height$" xlink:href="../media/$cover-image$" />
</svg>
</div>
$else$
$for(include-before)$
$include-before$
$endfor$
$body$
$for(include-after)$
$include-after$
$endfor$
$endif$
$endif$
</body>
</html>

"""

_style_str = """/*
 * Custom CSS file. Override it as you like.
 *
 * Credits to @killercup (https://gist.github.com/killercup); Extracted from this Gist:
 *   https://gist.github.com/killercup/5917178
 */

html {
    font-size: 100%;
    overflow-y: scroll;
    -webkit-text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
}

body {
    color: #444;
    font-family: Georgia, Palatino, 'Palatino Linotype', Times, 'Times New Roman', serif;
    font-size: 12px;
    line-height: 1.7;
    padding: 1em;
    margin: auto;
    max-width: 42em;
    background: #fefefe;
}

a {
    color: #0645ad;
    text-decoration: none;
}

a:visited {
    color: #0b0080;
}

a:hover {
    color: #06e;
}

a:active {
    color: #faa700;
}

a:focus {
    outline: thin dotted;
}

*::-moz-selection {
    background: rgba(255, 255, 0, 0.3);
    color: #000;
}

*::selection {
    background: rgba(255, 255, 0, 0.3);
    color: #000;
}

a::-moz-selection {
    background: rgba(255, 255, 0, 0.3);
    color: #0645ad;
}

a::selection {
    background: rgba(255, 255, 0, 0.3);
    color: #0645ad;
}

p {
    margin: 1em 0;
}

img {
    max-width: 100%;
}

h1,
h2,
h3,
h4,
h5,
h6 {
    color: #111;
    line-height: 125%;
    margin-top: 2em;
    font-weight: normal;
}

h4,
h5,
h6 {
    font-weight: bold;
}

h1 {
    font-size: 2.5em;
}

h2 {
    font-size: 2em;
}

h3 {
    font-size: 1.5em;
}

h4 {
    font-size: 1.2em;
}

h5 {
    font-size: 1em;
}

h6 {
    font-size: 0.9em;
}

blockquote {
    color: #666666;
    margin: 0;
    padding-left: 3em;
    border-left: 0.5em #EEE solid;
}

hr {
    display: block;
    height: 2px;
    border: 0;
    border-top: 1px solid #aaa;
    border-bottom: 1px solid #eee;
    margin: 1em 0;
    padding: 0;
}

pre,
code,
kbd,
samp {
    color: #000;
    font-family: monospace, monospace;
    _font-family: 'courier new', monospace;
    font-size: 0.98em;
}

pre {
    white-space: pre;
    white-space: pre-wrap;
    word-wrap: break-word;
}

b,
strong {
    font-weight: bold;
}

dfn {
    font-style: italic;
}

ins {
    background: #ff9;
    color: #000;
    text-decoration: none;
}

mark {
    background: #ff0;
    color: #000;
    font-style: italic;
    font-weight: bold;
}

sub,
sup {
    font-size: 75%;
    line-height: 0;
    position: relative;
    vertical-align: baseline;
}

sup {
    top: -0.5em;
}

sub {
    bottom: -0.25em;
}

ul,
ol {
    margin: 1em 0;
    padding: 0 0 0 2em;
}

li p:last-child {
    margin-bottom: 0;
}

ul ul,
ol ol {
    margin: .3em 0;
}

dl {
    margin-bottom: 1em;
}

dt {
    font-weight: bold;
    margin-bottom: .8em;
}

dd {
    margin: 0 0 .8em 2em;
}

dd:last-child {
    margin-bottom: 0;
}

img {
    border: 0;
    -ms-interpolation-mode: bicubic;
    vertical-align: middle;
}

figure {
    display: block;
    text-align: center;
    margin: 1em 0;
}

figure img {
    border: none;
    margin: 0 auto;
}

figcaption {
    font-size: 0.8em;
    font-style: italic;
    margin: 0 0 .8em;
}

table {
    margin-bottom: 2em;
    border-bottom: 1px solid #ddd;
    border-right: 1px solid #ddd;
    border-spacing: 0;
    border-collapse: collapse;
}

table th {
    padding: .2em 1em;
    background-color: #eee;
    border-top: 1px solid #ddd;
    border-left: 1px solid #ddd;
}

table td {
    padding: .2em 1em;
    border-top: 1px solid #ddd;
    border-left: 1px solid #ddd;
    vertical-align: top;
}

.author {
    font-size: 1.2em;
    text-align: center;
}

@media only screen and (min-width: 480px) {
    body {
        font-size: 14px;
    }
}

@media only screen and (min-width: 768px) {
    body {
        font-size: 16px;
    }
}

@media print {
    * {
        background: transparent !important;
        color: black !important;
        filter: none !important;
        -ms-filter: none !important;
    }
    body {
        font-size: 12pt;
        max-width: 100%;
    }
    a,
    a:visited {
        text-decoration: underline;
    }
    hr {
        height: 1px;
        border: 0;
        border-bottom: 1px solid black;
    }
    a[href]:after {
        content: " (" attr(href) ")";
    }
    abbr[title]:after {
        content: " (" attr(title) ")";
    }
    .ir a:after,
    a[href^="javascript:"]:after,
    a[href^="#"]:after {
        content: "";
    }
    pre,
    blockquote {
        border: 1px solid #999;
        padding-right: 1em;
        page-break-inside: avoid;
    }
    tr,
    img {
        page-break-inside: avoid;
    }
    img {
        max-width: 100% !important;
    }
    @page :left {
        margin: 15mm 20mm 15mm 10mm;
    }
    @page :right {
        margin: 15mm 10mm 15mm 20mm;
    }
    p,
    h2,
    h3 {
        orphans: 3;
        widows: 3;
    }
    h2,
    h3 {
        page-break-after: avoid;
    }
}
"""

class PandocBook(object):
    def __init__(self, title, author, abstract='Auto-generated ebook by Andrew.'):
        self.num_chaps = 0
        self.chap = None
        self.title = title
        self.author = author
        self.abstract = abstract
        os.makedirs(self.title)
        os.makedirs(os.path.join(self.title, 'chapters'))
        os.makedirs(os.path.join(self.title, 'images'))
        os.makedirs(os.path.join(self.title, 'templates'))
        with open(os.path.join(self.title, 'Makefile'), 'w') as makefile:
            makefile.write(_build_str)
        with open(os.path.join(self.title, 'templates', 'epub.html'), 'w') as templatefile:
            templatefile.write(_template_str)
        with open(os.path.join(self.title, 'templates', 'style.css'), 'w') as stylefile:
            stylefile.write(_style_str)
        with open(os.path.join(self.title, 'metadata.yml'), 'w') as configfile:
            configfile.write('---\n')
            configfile.write('title: {}\n'.format(self.title))
            configfile.write('author: {}\n'.format(self.author))
            configfile.write('rights: MIT License\n')
            configfile.write('lang: en-US\n')
            configfile.write('tags: [pandoc, book, my-book, etc]\n')
            configfile.write('abstract: {}\n'.format(self.abstract))
            configfile.write('mainfont: DejaVu Sans\n')
            configfile.write('linkReferences: true\n---\n')

    def addCover(self, imgfile):
        shutil.copy(imgfile, os.path.join(self.title, 'images', 'cover.png'))

    def newChapter(self, title):
        self.num_chaps += 1
        if not self.chap is None:
            self.chap.close()
        self.chap = open(os.path.join(self.title, 'chapters', "{:02d}-{}.md".format(self.num_chaps, title)), 'w')
        self.chap.write('# {}\n\n'.format(title))

    def addImage(self, imgfile, caption='', width=None):
        assert(not self.chap is None)
        dest_img = os.path.join('images', imgfile.split('/')[-1])
        if not width is None:
            self.chap.write('![{}]({}){{ width={} }}\n\n'.format(caption, dest_img, width))
        else:
            self.chap.write('![{}]({})\n\n'.format(caption, dest_img))
        shutil.copy(imgfile, os.path.join(self.title, dest_img))

    def addParagraph(self, text):
        assert(not self.chap is None)
        self.chap.write('{}\n\n'.format(text))

    def addSubHeading(self, title):
        assert(not self.chap is None)
        self.chap.write('## {}\n\n'.format(title))

    def addList(self, items):
        assert(not self.chap is None)
        for item in items:
            self.chap.write('- {}\n'.format(item))
        self.chap.write('\n')

    def addQuote(self, text):
        assert(not self.chap is None)
        self.chap.write('> {}\n\n'.format(text))

    def addTODO(self, text='TODO'):
        assert(not self.chap is None)
        self.chap.write('++++ {}\n\n'.format(text))

    def build(self):
        if not self.chap is None:
            self.chap.close()
        os.chdir(self.title)
        subprocess.call(['make','epub'])
    