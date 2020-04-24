import numpy as numpy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Occurance of Top Keywords in Recent News
keyword_data = pd.read_csv("keywords.csv")
sns.barplot(x="keyword",y="occurance",data=keyword_data).set_title('Occurance of Top Keywords in Recent News')
plt.show()

# Categorical Representation of Playlist Lengths of all Playlists
playlist_length_data = pd.read_csv("playlist_lengths.csv")
sns.barplot(x="playlist_range",y="total",data=playlist_length_data).set_title('Categorical Representation of Playlist Lengths of all Playlists')
plt.show()