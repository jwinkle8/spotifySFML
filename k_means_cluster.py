import csv
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set()  # for plot styling
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


if __name__ == "__main__":

    song_data = read_songs()

    col1 = song_data[:,4][1:]
    col2 = song_data[:,7][1:]
    X = np.column_stack((col1, col2)).astype(float)

    ax = plt.axes()
    ax.set_xlabel("Energy")
    ax.set_ylabel("Acousticness")

    centers, labels = find_clusters(X, 4)
    plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap='viridis')
    plt.show()
