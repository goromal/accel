import requests, sys, re, subprocess
import lxml.html
sys.path.insert(0,'../')
from pandoc_book import PandocBook

plato_url = sys.argv[1]

def toHRText(text):
    return text.replace('-\n','').replace('\n',' ').replace('&','and').replace('\(','$').replace('\)','$')

def toSimpleTitle(text):
    return re.sub(r'([0-9]|\.)+','',text)

response = requests.get(plato_url, stream=True)
response.raw.decode_content = True
tree = lxml.html.parse(response.raw)

doctitle = tree.xpath('//*[@id="aueditable"]/h1')[0].text
doc = PandocBook(doctitle, 'Stanford Encyclopedia of Philosophy')

subprocess.call(['convert','PlatoLogo.png','-gravity','North','-size','800x200',
                 '-font','Times-Bold','-fill','white','-pointsize','100','-annotate',
                 '+0+400','%s' % doctitle, 'cover.png'])
doc.addCover('cover.png')

doc.newChapter('Preamble')
paragraphs = tree.xpath('//*[@id="preamble"]/*')
for paragraph in paragraphs:
    doc.addParagraph(toHRText(paragraph.text_content()))

main_content = tree.xpath('//*[@id="main-text"]/*')
for tag in main_content:
    if tag.tag == 'h2':
        doc.newChapter(toSimpleTitle(tag.text_content()))
    elif tag.tag == 'h3':
        doc.addSubHeading(toSimpleTitle(tag.text_content()))
    elif tag.tag == 'p':
        doc.addParagraph(toHRText(tag.text_content()))
    elif tag.tag == 'ul':
        doc.addList([toHRText(itemtag.text_content()) for itemtag in tag.iter('li')])
    elif tag.tag == 'blockquote':
        doc.addQuote(tag.text_content())
    else:
        print('WARNING: unrecognized environment: \'%s\'' % tag.tag)
        doc.addTODO(tag.tag)

doc.build()