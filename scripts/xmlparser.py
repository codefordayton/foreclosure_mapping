import xml.etree.ElementTree as ET
import base64

data = ET.parse('data/dockets.xml')
root = data.getroot()

casenumber = 'init'

for child in root:
    for subchild in child:
        if subchild.tag == 'CaseNumber':
            casenumber = "".join(subchild.text.split())
        elif subchild.tag == 'Docket':
            bin = base64.b64decode(subchild.text)
            with open('pdfs/' + casenumber + '.pdf', 'wb') as g:
                g.write(bin)
