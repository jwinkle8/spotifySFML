import data_collection
import k_means_cluster
import spotipy
import spotipy.util as util
import sys

if __name__ == '__main__':
    scope = 'playlist-modify-public user-library-read'

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    token = util.prompt_for_user_token(username, scope)

    if token:
        data_collection.write_songs(spotipy.Spotify(auth=token))
        k_means_cluster.cluster_songs(token, username)
    else:
        print("Can't get token for", username)