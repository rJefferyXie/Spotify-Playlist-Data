# Spotify Playlist Data Gatherer - Jeffery Xie
# This is a personal project to familiarize myself with Spotify's API
# Given a Spotify Playlist, this program will gather interesting data like
# Popularity, Length, Name, Album, Energy, Time Signature, Tempo, and more

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# The playlist link, change for different playlists
playlist_link = 'https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=O8Q9bNgnQhutuB8oUoKjog'

# Authenticate and connect to spotify's API
client_id = "ab7b392758ea471baba19f59c236eacb"
client_secret = "e68dc297cb2c41ef86aac101020372d1"
client_credentials = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials)


def get_song_ids(playlist):
    """
    Extract every song ID from a playlist and put them all into a list.
    :param playlist: a spotify playlist link
    :return: a list of the song IDs for the playlist
    """
    ids = []
    playlist_data = sp.playlist(playlist)

    # Append the song ID for each song in the playlist
    # ex. '3UrYzeFR2wVIk2SAInaiDJ'
    for song in playlist_data['tracks']['items']:
        track = song['track']
        ids.append(track['id'])
    return ids


def make_csv(ids):
    """
    From a list of song IDs, get the relevant data and write it to the csv file.
    :param ids: a list of song IDs
    :return: None, but should make a csv file of the songs with interesting information
    """

    filename = "playlist.csv"
    f = open(filename, "w")

    headers = "Name, Artist, Album, Release Date, Length, Popularity," \
              "Acoustics, Dance, Energy, Speech, Tempo, Time Signature \n"

    f.write(headers)

    # Gather information for each song from the song ID
    for songID in ids:
        # Song name, artist(s), album, release date, length, popularity
        song_information = sp.track(songID)

        name = song_information['name']
        artist = song_information['album']['artists'][0]['name']
        album = song_information['album']['name']
        release_date = song_information['album']['release_date']

        # Convert length to minutes and seconds
        length_in_ms = song_information['duration_ms']
        seconds = round((length_in_ms / 1000) % 60)
        minutes = round((length_in_ms / (1000 * 60)) % 60)
        if seconds < 10:
            seconds = "0" + str(seconds)
        length = str(minutes) + ":" + str(seconds)
        popularity = str(song_information['popularity'])

        # Acoustics, Dance, Energy, Speech, Tempo, Time Signature
        song_audio_features = sp.audio_features(songID)

        acoustics = str(song_audio_features[0]['acousticness'])
        dance = str(song_audio_features[0]['danceability'])
        energy = str(song_audio_features[0]['energy'])
        speech = str(song_audio_features[0]['speechiness'])
        tempo = str(song_audio_features[0]['tempo'])
        time_signature = str(song_audio_features[0]['time_signature'])

        # Return a list of data for each song, (song information and audio features)
        f.write(
            name + "," + artist + "," + album + "," + release_date + "," + length + "," + popularity + "," + acoustics
            + "," + dance + "," + energy + "," + speech + "," + tempo + "," + time_signature + "\n")

    f.close()


def main():
    """
    Using the spotipy module, open a playlist and return a .csv file with cool information such as
    acoustics, dance, energy, speech, popularity, tempo, and time signature.

    :return: None
    """
    ids = get_song_ids(playlist_link)
    make_csv(ids)


if __name__ == "__main__":
    main()
