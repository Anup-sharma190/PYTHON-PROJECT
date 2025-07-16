import urllib.request
import xml.etree.ElementTree as ET

url = input('Enter location: ')
data = urllib.request.urlopen(url).read()

tree = ET.fromstring(data)
counts = tree.findall('.//count')
total = sum(int(c.text) for c in counts)

print('Count:', len(counts))
print('Sum:', total)
