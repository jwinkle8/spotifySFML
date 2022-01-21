import clustering_helpers
import create_playlists
import csv
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set()  
from sklearn.metrics import pairwise_distances_argmin


def read_songs():
    song_data = []
    with open("songs.csv", newline="") as songs_file:
        song_reader = csv.reader(songs_file, delimiter=',', quotechar='|')
        for row in song_reader:
            song_data.append(row)
    return np.array(song_data)


def find_clusters(X, n_clusters, rseed=2):
    
    rng = np.random.RandomState(rseed)
    i = rng.permutation(X.shape[0])[:n_clusters]
    centers = X[i]
    
    while True:
        
        labels = pairwise_distances_argmin(X, centers)
        
        new_centers = np.array([X[labels == i].mean(0)
                                for i in range(n_clusters)])
        
        if np.all(centers == new_centers):
            break
        centers = new_centers
    
    return centers, labels


def cluster_songs(token, username):

    song_data = read_songs()

    headers = song_data[0]
    feature_pairs = clustering_helpers.get_all_feature_pairs()

    errors = []

    for rseed in range(11):
        for pair in feature_pairs:

            col1 = np.array(song_data[:,pair[0]][1:]).astype(float)
            col2 = np.array(song_data[:,pair[1]][1:]).astype(float)

            clustering_helpers.normalize_feature_statistics(col1)
            clustering_helpers.normalize_feature_statistics(col2)

            X = np.column_stack((col1, col2))

            centers, labels = find_clusters(X, 4, rseed)

            errors.append(clustering_helpers.compute_error(X, centers, labels))

    min_pair = feature_pairs[errors.index(min(errors)) % 10]
    rseed = errors.index(min(errors)) // 10
    

    ax = plt.axes()
    ax.set_xlabel(headers[min_pair[0]])
    ax.set_ylabel(headers[min_pair[1]])

    col1 = song_data[:,min_pair[0]][1:]
    col2 = song_data[:,min_pair[1]][1:]
    X = np.column_stack((col1, col2)).astype(float)

    centers, labels = find_clusters(X, 4, rseed)

    plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap='viridis')
    plt.show()

    create_playlists.fill_playlists(labels, username, token)
