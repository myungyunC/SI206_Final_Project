# SI 206 - Final Project

Final project using data from the Google News API and the Spotify API to make calculations and visual representations of the analyzed data.

## Getting Started

These instructions will ensure the code runs correctly to retrieve the data.

### Clear Tables and Existing Data

Run the following in your terminal or command line:

```
python3 delete_table.py
```
This will delete all tables and clear the JSON file.

### Retrieve the Data

Google News API - repeat until output states it's finished.

```
python3 keywords.py
```

Spotify Playlists and Tracks data - repeat until finished.

```
python3 spotify_getter.py
```

### Process the Data

This will process the data by:
  - The top 10 most common keywords and their count
  - The most frequently occuring songs among the playlists
  - The most popular track features among the playlists


## Authors
* **Myungyun Chung**
* **Ian Herdegen**
