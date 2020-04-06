import requests
import spotipy
import spotipy.oauth2 as oauth2


class Spotify:
    """Main class to handle all Spotify API calls."""

    URLs = {'AUDIO_FEATURES': 'https://api.spotify.com/v1/audio-features/',
            'ARTIST_TOP_SONG': 'https://api.spotify.com/v1/artists/{}/top-tracks',
            'CREATE_PLAYLIST': 'https://api.spotify.com/v1/users/{}/playlists',
            'PAUSE': 'https://api.spotify.com/v1/me/player/pause',
            'PLAY': 'https://api.spotify.com/v1/me/player/play',
            'PLAYLIST': 'https://api.spotify.com/v1/playlists/{}',
            'PLAYLIST_TRACKS': 'https://api.spotify.com/v1/playlists/{}/tracks',
            'SEARCH': 'https://api.spotify.com/v1/search',
            'SKIP': 'https://api.spotify.com/v1/me/player/next',
            'TRACKS': 'https://api.spotify.com/v1/tracks/',
            'USER_PROFILE': 'https://api.spotify.com/v1/me'}

    def __init__(self, id, secret):
        """Initializer for Spotify class."""
        self.client_id = id
        self.client_secret = secret

        # Get Authorization Token
        self.credentials = oauth2.SpotifyClientCredentials(client_id=id,
                                                           client_secret=secret)
        # self.token = self.credentials.get_access_token()
        self.token = "BQD-80EFP2O9LfrwAY8kksEumjBryZMrz56piEURh4Ms0Q7MsTzquiUqIfjOdB_jU4jmfSfSVKw_MNXTKTQ"
        self.spotify = spotipy.Spotify(auth=self.token)

    def _get_headers(self):
        """Format header for spotify Api request."""
        return {'Authorization': "Bearer {}".format(self.token)}

    def _check_for_response_errors(self, response):
        """Check response for any error codes."""
        if response.status_code >= 400:
            caller_name = inspect.stack()[1].function
            print("ERROR on {}".format(caller_name))
            print(response.text)

    def search(self, query, s_type):
        """
        Returns Spotify API search result.
        See https://developer.spotify.com/documentation/web-api/reference/search/search/
        `type` is one of: ['album', 'artist', 'playlist', 'track']
        """
        assert s_type in ['album', 'artist', 'playlist', 'track']
        payload = {
            'q': query,
            'type': s_type,
        }

        r = requests.get(self.URLs['SEARCH'], headers=self._get_headers(),
                         params=payload)
        self._check_for_response_errors(r)
        return r.json()

    def get_tracks_from_playlist(self, playlist_href):
        """
        Get the list of track IDs from a particular playlist.
        Parameters: href link to API for getting tracks from playlist
        Returns: list of IDs
        """
        ids = []
        uris = []

        response = requests.get(playlist_href, headers=self._get_headers())
        self._check_for_response_errors(response)
        response = response.json()

        for track in response["tracks"]["items"]:
            # Get max 100 tracks
            if len(ids) == 100:
                break
            track_id = track['track']['id']
            track_uri = track['track']['uri']
            if track_id is not None and track_uri is not None: # sometimes track id is None apparently, but we don't want that
                ids.append(track_id)
                uris.append(track_uri)

        return ids, uris

    def search_for_playlists(self, keyword):
        """Search for playlists in Spotify given list of keywords."""
        results = self.search(keyword, 'playlist')
        url = results['playlists']['items'][0]['href']

        ids, uris = self.get_tracks_from_playlist(url)

        return ids, uris