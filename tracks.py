import sqlite3
import csv

conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title   TEXT UNIQUE,
    artist_id  INTEGER
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
)
''')

fname = 'tracks.csv'
with open(fname) as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        if len(row) < 8: continue

        name, artist, album, count, rating, length, genre = row[0], row[1], row[2], row[3], row[4], row[5], row[7]

        cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)', (artist,))
        cur.execute('SELECT id FROM Artist WHERE name = ?', (artist,))
        artist_id = cur.fetchone()[0]

        cur.execute('INSERT OR IGNORE INTO Genre (name) VALUES (?)', (genre,))
        cur.execute('SELECT id FROM Genre WHERE name = ?', (genre,))
        genre_id = cur.fetchone()[0]

        cur.execute('INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)', (album, artist_id))
        cur.execute('SELECT id FROM Album WHERE title = ?', (album,))
        album_id = cur.fetchone()[0]

        cur.execute('''INSERT OR REPLACE INTO Track
            (title, album_id, genre_id, len, rating, count)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (name, album_id, genre_id, length, rating, count))

conn.commit()
