import numpy as numpy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_keywords():
    # Occurance of Top Keywords in Recent News
    keyword_data = pd.read_csv("keywords.csv")
    sns.barplot(x="keyword",y="occurance",data=keyword_data).set_title('Occurance of Top Keywords in Recent News')
    plt.show()

def visualize_lengths():
    # Categorical Representation of Playlist Lengths of all Playlists
    playlist_length_data = pd.read_csv("playlist_lengths.csv")
    sns.barplot(x="playlist_range",y="total",data=playlist_length_data).set_title('Categorical Representation of Playlist Lengths of all Playlists')
    plt.show()

def visualize_features():
    # Categorical Representation of Most Popular Feature among songs in Each Playlist
    feature_data = pd.read_csv("features.csv")
    sns.barplot(x="feature",y="total",data=feature_data).set_title('Categorical Representation of Most Popular Features among all Playlists')
    plt.show()

def main():
    visualize_keywords()
    visualize_lengths()
    visualize_features()

if __name__ == '__main__':
    main()