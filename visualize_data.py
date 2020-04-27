import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_keywords():
    # Occurance of Top Keywords in Recent News
    keyword_data = pd.read_csv("keywords.csv")
    sns.barplot(x="keyword",y="occurance",data=keyword_data).set_title('Occurance of Top Keywords in Recent News')
    plt.savefig('keywords.png')

def visualize_lengths():
    # Categorical Representation of Playlist Lengths of all Playlists
    playlist_length_data = pd.read_csv("playlist_lengths.csv")
    sns.barplot(x="playlist_range",y="total",data=playlist_length_data).set_title('Categorical Representation of Playlist Lengths of all Playlists')
    plt.savefig('playlist_ranges.png')

def visualize_features():
    # Categorical Representation of Most Popular Feature among songs in Each Playlist
    labels = []
    sizes = []
    with open("features.csv", "r") as feature_data:
        fd = feature_data.readlines()
        for i in range(len(fd)):
            if i == 0:
                continue
            labels.append(fd[i].split(',')[0])
            sizes.append(fd[i].split(',')[1])
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Categorical Representation of Most Popular Features among all Playlists')
    plt.savefig('features.png')

def main():
    visualize_keywords()
    visualize_lengths()
    visualize_features()

if __name__ == '__main__':
    main()