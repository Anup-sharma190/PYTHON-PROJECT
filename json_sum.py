import urllib.request, json

url = input('Enter location: ')
data = urllib.request.urlopen(url).read().decode()
info = json.loads(data)

total = sum(item['count'] for item in info['comments'])

print('Count:', len(info['comments']))
print('Sum:', total)
