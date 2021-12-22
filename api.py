from flask import Flask
from flask import jsonify
from flask import request
import psql_connection
import neo4j_connection
import os
import parser

app = Flask(__name__)

# PSQL

@app.route('/songs', methods=['GET'])
def get_songs():
    title = request.args.get('title')
    artist = request.args.get('artist')
    if title is None and artist is None:
        result = psql_connection.get_songs()
        if result is None:
            return {}
        return jsonify(songs=[s.serialize() for s in result])
    if title is None or artist is None:
        return "Missing parameters"
    result = psql_connection.get_song(title,artist)
    if result is None:
        return {}
    return jsonify(result.serialize())


@app.route('/similar', methods=['GET'])
def get_similar():
    title = request.args.get('title')
    artist = request.args.get('artist')
    if title is None or artist is None:
        return "Missing parameters"
    result = psql_connection.get_similar_songs(title,artist)
    if result is None:
        return {}
    return jsonify(songs=[s.serialize() for s in result])

@app.route('/intensity_ratio', methods=['GET'])
def get_ratio():
    return psql_connection.get_intensity_tension_relationship()

# NEO4J

@app.route('/song_by_feeling', methods=['GET'])
def get_by_feeling():
    feeling = request.args.get('feeling')
    if feeling is None:
        return "Missing parameters"
    if int(feeling) > 1 or int (feeling) < 0:
        return "Invalid parameters"
    result = neo4j_connection.get_songs_by_feeling(int(feeling))
    if result is None:
        return {}
    return jsonify(songs=[s.serialize() for s in result])

@app.route('/positive_artists', methods=['GET'])
def get_positive_artists():
    result = neo4j_connection.get_artists_with_positive_song()
    if result is None:
        return {}
    return jsonify(artists=[s.serialize() for s in result])

@app.route('/popular_sequence', methods=['GET'])
def get_popular_sequence():
    return neo4j_connection.get_most_used_sequence()

@app.route('/artist_feeling', methods=['GET'])
def get_artist_feeling():
    artist = request.args.get('artist')
    if artist is None:
        return "Missing parameters"
    return neo4j_connection.get_artist_feeling(artist)

@app.route('/songs', methods=['POST'])
def insert():
    file = request.files['file']
    artist = request.form['artist']
    if file is None or artist is None:
        return "Missing parameters"
    os.system('midicsv ' + file.filename + ' out.csv')
    csv_file = open('out.csv')
    parser.parser(csv_file, artist)
    print(file.filename)
    print(artist)
    return "Inserted succesfully"

@app.route('/tracks', methods=['GET'])
def get_tracks():
    title = request.args.get('title')
    artist = request.args.get('artist')
    if title is None or artist is None:
        return "Missing parameters"
    result = neo4j_connection.get_song_tracks(title,artist)
    if result is None:
        return {}
    return jsonify(tracks=[s.serialize() for s in result])  

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081)

    