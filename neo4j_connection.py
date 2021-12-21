from py2neo import Graph
from parser import Track
graph = Graph(host="localhost")

class SimpleSong(object):
    title = ""
    artist = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
    def serialize(self):
        if self.title == None:
            return {'artist': self.artist}
        return {
        'title': self.title, 
        'artist': self.artist
        }

class SimpleTrack(object):
    track = ""
    instrument = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, track, instrument):
        self.track = track
        self.instrument = instrument
    def serialize(self):
        return {
        'track': self.track, 
        'instrument': self.instrument
        }

def initialize():
    tx = graph.begin()
    count = tx.evaluate("MATCH (i:Instrument) RETURN count(i)") 
    if count == 0:
        f = open("instruments.txt", "r")
        for line in f:
            line = line.split(" ", 1)
            tx.run("CREATE (i:Instrument {{id: \"{0}\", name: \"{1}\"}}) RETURN i".format(line[0],line[1]))
        tx.run("CREATE (f:Feeling {type: \"Positive\"}) RETURN f") 
        tx.run("CREATE (f:Feeling {type: \"Negative\"}) RETURN f") 
        graph.commit(tx) 
        f.close()

POSITIVE = 1
NEGATIVE = 0


def insert(title,artist,sequence,positiveness,tracks):
    initialize()
    tx = graph.begin()
    if positiveness >= 0 and positiveness <= 1:
        song_node = tx.evaluate("CREATE (s:Song {{title: \"{0}\"}}) RETURN s".format(title))
        tx.run("MERGE (a:Artist {{name: \"{0}\"}})".format(artist))
        tx.run("MERGE (s:Sequence {{value: \"{0}\"}})".format(sequence))
        for t in tracks:
            track_node = tx.evaluate("CREATE (t:Track {{name: \"{0}\"}}) RETURN t".format(t.title))
            tx.run("MATCH (p:Instrument {{id: \"{0}\"}}),(w) WHERE id(w) = {1} CREATE (w)-[r:instrument_type]->(p)".format(t.instrument,track_node.identity))
            tx.run("MATCH (p),(w) WHERE id(p) = {0}  and id(w) = {1} CREATE (w)-[r:appears_in]->(p)".format(song_node.identity,track_node.identity))
        
        tx.run("MATCH (p),(w:Artist {{name: \"{1}\"}}) WHERE id(p) = {0} CREATE (p)-[r:played_by]->(w)".format(song_node.identity,artist))
        tx.run("MATCH (p),(w:Sequence {{value: \"{1}\"}}) WHERE id(p) = {0} CREATE (p)-[r:sequence_type]->(w)".format(song_node.identity,sequence))
        if positiveness >= 0.5:
            tx.run("MATCH (p),(w:Feeling {type: \"Positive\"}) WHERE id(p) = " +str(song_node.identity)+ " CREATE (p)-[r:feels {{positiveness: {0}}}]->(w)".format(positiveness))
        else:
            tx.run("MATCH (p),(w:Feeling {type: \"Negative\"}) WHERE id(p) = " +str(song_node.identity)+ " CREATE (p)-[r:feels {{positiveness: {0}}}]->(w)".format(positiveness))
    graph.commit(tx)

def get_song_tracks(title,artist):
    initialize()
    tx = graph.begin()
    result = []
    
    artists = tx.run('MATCH (a:Artist)<-[:played_by]-(s:Song)<-[:appears_in]-(t:Track)-[:instrument_type]->(i:Instrument) WHERE s.title = \'{0}\' and a.name = \'{1}\' return t,i'.format(title,artist))
    for a in artists:
        result.append(SimpleTrack(a.values()[0]["name"],a.values()[1]["name"]))

    graph.commit(tx)
    return result

def get_songs_by_feeling(feeling):
    initialize()
    tx = graph.begin()
    songs = []
    result = []
    if feeling == POSITIVE:
        songs = tx.run('MATCH (a:Artist)<-[:played_by]-(s:Song)-[fe:feels]->(f:Feeling) WHERE f.type = \'Positive\' return s,a ORDER BY fe.positiveness desc;')
    else:
        songs = tx.run('MATCH (a:Artist)<-[:played_by]-(s:Song)-[fe:feels]->(f:Feeling) WHERE f.type = \'Negative\' return s,a ORDER BY fe.positiveness asc;')
    
    for s in songs:
        result.append(SimpleSong(s.values()[0]["title"],s.values()[1]["name"]))
    graph.commit(tx)
    return result

def get_artists_with_positive_song():
    initialize()
    tx = graph.begin()
    result = []
    
    artists = tx.run('MATCH (a:Artist)<-[:played_by]-(s:Song)-[:feels]->(f:Feeling) WHERE f.type = \'Positive\' RETURN DISTINCT a ')
    for a in artists:
        result.append(SimpleSong(None,a.values()[0]["name"]))

    graph.commit(tx)
    return result

def get_most_used_sequence():
    initialize()
    tx = graph.begin()
    
    sequence = tx.run('MATCH (s:Song)-[:sequence_type]->(seq:Sequence) return count(s) as c,seq.value ORDER BY c DESC')

    seq = sequence.data()[0]['seq.value']

    graph.commit(tx)
    return {'most_used_sequence': "{0}".format(seq)}

def get_artist_feeling(artist):
    initialize()
    tx = graph.begin()
    
    feeling = tx.evaluate('MATCH (a)<-[:played_by]-(s:Song)-[:feels]->(f:Feeling) WHERE a.name = \'{0}\' and f.type = \'Positive\' WITH a, count(s) as positive_cnt MATCH (a)<-[:played_by]-(s1) return toFloat(positive_cnt)/count(s1)'.format(artist))

    if feeling is None:
        return {}

    graph.commit(tx)
    return {
        'artist': artist,
        'artist_feeling': feeling}

