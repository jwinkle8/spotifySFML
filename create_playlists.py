import spotipy as sp
import spotipy.util as util

def fill_playlists(song_data, labels, user_id, token):

    spotify = sp.Spotify(auth=token)

    playlists = spotify.current_user_playlists()
    playlist_names = []
    for playlist in playlists['items']:
        playlist_names.append(playlist['name'])

    for i in range(1, 5):
        proposed_playlist_name = "ML_Playlist" + str(i)
        if proposed_playlist_name not in playlist_names:
            spotify.user_playlist_create(user_id, proposed_playlist_name)

    playlists = spotify.current_user_playlists()
    playlist_ids = []
    for playlist in playlists['items']:
        if "ML_Playlist" in playlist['name']:
            playlist_ids.append(playlist['id'])

    playlist_dict = {'0': [], '1': [], '2': [], '3': []}
    for i in range(200):
            
        results = spotify.current_user_saved_tracks(50, i*50)
        if not results['items']:
            break

        song_num = 0 + i * 50 
        for item in results['items']:
            playlist_dict[str(labels[song_num])].append(item['track']['id'])
            song_num += 1
 
    for num in playlist_dict:
        spotify.user_playlist_add_tracks(user_id, playlist_ids[int(num)], playlist_dict[num])
