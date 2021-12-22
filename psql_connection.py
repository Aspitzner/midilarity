import psycopg2

signatures = ['C', 'G', 'D', 'A', 'E', 'Cb', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F']  # Modify to make it circular

delta_bpm = 10
delta_time_signature = 0.5
delta_stress = 1
delta_key_signature = 2

radius = 40

time_multiplier = delta_bpm / delta_time_signature
stress_multiplier = delta_bpm / delta_stress
key_multiplier = delta_bpm / delta_key_signature


class Song(object):
    title = ""
    artist = ""
    csv_tempo = 0
    bpm = 0
    time_signature = ""
    key_signature = ""
    avg_pressure = 0
    stress = 0
    file = []
    distance = -1

    # The class "constructor" - It's actually an initializer 
    def __init__(self, title, artist, csv_tempo, bpm, time_signature, key_signature, avg_pressure, stress, file,
                 distance):
        self.title = title
        self.artist = artist
        self.csv_tempo = csv_tempo
        self.bpm = bpm
        self.time_signature = time_signature
        self.key_signature = key_signature
        self.avg_pressure = avg_pressure
        self.stress = stress
        self.file = file
        self.distance = distance

    def serialize(self):
        if self.distance != -1:
            return {
                'distance': self.distance,
                'song': {
                    'title': self.title,
                    'artist': self.artist,
                    'csv_tempo': self.csv_tempo,
                    'bpm': self.bpm,
                    'time_signature': self.time_signature,
                    'key_signature': self.key_signature,
                    'avg_pressure': self.avg_pressure,
                    'stress': self.stress,
                    'file': self.file
                }}
        return {
            'title': self.title,
            'artist': self.artist,
            'csv_tempo': self.csv_tempo,
            'bpm': self.bpm,
            'time_signature': self.time_signature,
            'key_signature': self.key_signature,
            'avg_pressure': self.avg_pressure,
            'stress': self.stress,
            'file': self.file
        }


def get_song_by_row(row, has_distance):
    if has_distance:
        return Song(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], "", float(row[9]))
    return Song(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], "", -1)


def init_connection():
    con = psycopg2.connect(database="tp_midi", user="postgres", password="1234", host="localhost", port="5433")
    print("Database opened successfully")
    return con


def close_connection(con):
    con.commit()
    con.close()


def insert(title, artist, csv_tempo, bpm, time_signature, key_signature, avg_pressure, stress, file_name):
    mybytearray = bytearray()
    try:
        with open(file_name, "rb") as f:
            byte = f.read(1)
            while byte:
                mybytearray += byte
                byte = f.read(1)
    except IOError:
        print('Error While Opening the file!')

    signature_index = -1
    for i in range(0, len(signatures)):
        if signatures[i] == key_signature:
            signature_index = i
            break
    if signature_index == -1:
        print("Unexistent key signature")
        return

    con = init_connection()
    cur = con.cursor()

    attributes = '({0},{1},{2},{3})'.format(str(bpm), eval(time_signature) * time_multiplier,
                                            signature_index * key_multiplier, str(stress * stress_multiplier))

    cur.execute(
        "create extension if not exists cube; create table if not exists midi (id SERIAL,title TEXT,artist TEXT,csv_tempo INTEGER,bpm INTEGER,time_signature TEXT,key_signature TEXT,avg_pressure INTEGER,stress INTEGER,file bytea,attributes cube,PRIMARY KEY (id));CREATE UNIQUE INDEX IF NOT EXISTS idx_song_identification ON midi (title, artist);insert into midi(title,artist,csv_tempo,bpm,time_signature,key_signature,avg_pressure,stress,file,attributes) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
        (title, artist, str(csv_tempo), str(bpm), time_signature, key_signature, str(avg_pressure), str(stress),
         mybytearray, attributes))
    print("Inserted successfully")

    close_connection(con)


def get_songs():
    con = init_connection()
    cur = con.cursor()
    results = []

    cur.execute("SELECT title,artist,csv_tempo,bpm,time_signature,key_signature,avg_pressure,stress,file from midi")
    if cur.rowcount == 0:
        return None
    row = cur.fetchone()

    while row is not None:
        song = get_song_by_row(row, False)  # str(row[8].tobytes())
        results.append(song)
        row = cur.fetchone()

    close_connection(con)
    return results


def get_song(title, artist):
    con = init_connection()
    cur = con.cursor()

    cur.execute(
        "SELECT title,artist,csv_tempo,bpm,time_signature,key_signature,avg_pressure,stress,file from midi where title = \'{0}\' and artist = \'{1}\'".format(
            title, artist))
    if cur.rowcount == 0:
        return None
    row = cur.fetchone()
    close_connection(con)
    return get_song_by_row(row, False)


def get_similar_songs(title, artist):
    con = init_connection()
    cur = con.cursor()
    results = []

    query = "SELECT title,artist,csv_tempo,bpm,time_signature,key_signature,avg_pressure,stress,file,cube_distance(attributes, (select attributes from midi where title = '{0}' and artist = '{1}')) dist FROM midi WHERE (title != '{0}' or artist != '{1}') and cube_enlarge((select attributes from midi where title = '{0}' and artist = '{1}')::cube, {2}, 4) @> midi.attributes ORDER BY dist;".format(
        title, artist, radius)
    cur.execute(query)
    if cur.rowcount == 0:
        return None
    row = cur.fetchone()

    while row is not None:
        song = get_song_by_row(row, True)
        results.append(song)
        row = cur.fetchone()

    close_connection(con)
    return results


def get_intensity_tension_relationship():
    con = init_connection()
    cur = con.cursor()

    cur.execute(
        "SELECT (SELECT SUM(avg_pressure) FROM midi)::DOUBLE PRECISION / (SELECT sum(stress) FROM midi) as ratio")
    row = cur.fetchone()

    close_connection(con)
    return {'intensity-tension-ratio': row[0]}
