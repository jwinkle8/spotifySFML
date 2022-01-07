import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys


def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))


if __name__ == '__main__':

    with open("SFML/spotifySFML/dev_secrets.txt") as dev_secrets:
        cid = dev_secrets.readline().split(":")[1]
        secret = dev_secrets.readline().split(":")[1]

    #Authentication - without user
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Whoops, need your username!")
        print("usage: python user_playlists.py [username]")
        sys.exit()

    scope = "user-library-read"
    jwinkle8 = spotipy.util.prompt_for_user_token(username, scope=scope, client_id=cid, client_secret=secret, redirect_uri="https:/example.com/callback/")

    if jwinkle8:
        sp = spotipy.Spotify(auth=jwinkle8)
        playlists = sp.user_playlists(username)
        print(playlists)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                print()
                print(playlist['name'])
                print ('  total tracks', playlist['tracks']['total'])
                results = sp.playlist(playlist['id'],
                    fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
    else:
        print("Can't get token for", username)