import sqlite3
import urllib.request, urllib.parse, urllib.error
import json
import time
import ssl

api_key = False
serviceurl = 'https://py4e-data.dr-chuck.net/geojson?'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

fh = open("where.data")
for line in fh:
    address = line.strip()
    cur.execute("SELECT geodata FROM Locations WHERE address= ?", (address,))
    try:
        data = cur.fetchone()[0]
        print("Found in database", address)
        continue
    except:
        pass

    parms = dict()
    parms["address"] = address
    parms["key"] = api_key if api_key else 42
    url = serviceurl + urllib.parse.urlencode(parms)

    print("Retrieving", url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    count = 0
    try:
        js = json.loads(data)
    except:
        continue

    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS'):
        print('Failure To Retrieve')
        continue

    cur.execute('''INSERT INTO Locations (address, geodata)
            VALUES (?, ?)''', (address, data))
    conn.commit()
    time.sleep(1)
