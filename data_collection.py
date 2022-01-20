import csv
import sys
import spotipy
import spotipy.util as util

def write_songs(sp):

    with open('songs.csv', 'w') as songs_file:
        writer = csv.writer(songs_file)

        headers = ['Song Number', 'Song Title', 'Artist Name', 'Danceability', 'Energy', 'Loudness', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Liveness', 'Tempo']
        writer.writerow(headers)

        for i in range(200):
            results = sp.current_user_saved_tracks(50, i*50)
            if not results['items']:
                break

            song_num = 1
            for item in results['items']:
                track = item['track']
                track_audio = sp.audio_features(track['uri'])[0]
                track_info = [str(i * 50 + song_num), 
                            track['name'].replace(",", " "), 
                            track['artists'][0]['name'],
                            track_audio['danceability'],
                            track_audio['energy'],
                            track_audio['loudness'],
                            track_audio['speechiness'],
                            track_audio['acousticness'],
                            track_audio['instrumentalness'],
                            track_audio['liveness'],
                            track_audio['tempo']]
                writer.writerow(track_info)
                song_num += 1

    songs_file.close()

if __name__ == '__main__':
    scope = 'user-library-read'

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    token = util.prompt_for_user_token(username, scope)

    if token:
        write_songs(spotipy.Spotify(auth=token))
    else:
        print("Can't get token for", username)