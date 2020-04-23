import requests
import spotipy
import spotipy.oauth2 as oauth2


class Spotify:
    """Main class to handle all Spotify API calls."""

    URLs = {'SEARCH': 'https://api.spotify.com/v1/search',
            'TRACKS': 'https://api.spotify.com/v1/tracks/',
            'FEATURES': 'https://api.spotify.com/v1/audio-features/',
            'PLAYLIST': 'https://api.spotify.com/v1/playlists/'}

    def __init__(self, id, secret):
        """Initializer for Spotify class."""
        self.client_id = id
        self.client_secret = secret

        # Get Authorization Token
        self.credentials = oauth2.SpotifyClientCredentials(client_id=id,
                                                           client_secret=secret)
        self.token = self.credentials.get_access_token()
        # print(self.token)
        # self.token = "BQDsANVnfNXFHSIfmK8KtXJ7TPovXzhPSgL_DmWaQTBChX6C-f_foj4Spz_OyT4vwWW8RxAdEutv0cFPXFI"
        self.spotify = spotipy.Spotify(auth=self.token)

    def _get_headers(self):
        """Format header for spotify Api request."""
        return {'Authorization': "Bearer {}".format(self.token)}

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
        return r.json()

    def get_tracks_from_playlist(self, playlist_href):
        """
        Get the list of track IDs from a particular playlist.
        Parameters: href link to API for getting tracks from playlist
        Returns: list of IDs
        """
        ids = []

        response = requests.get(playlist_href, headers=self._get_headers())
        response = response.json()

        for track in response["tracks"]["items"]:
            # Get max 20 tracks
            if len(ids) == 10:
                break
            track_id = track['track']['id']
            if track_id is not None:
                ids.append(track_id)

        return ids

    def get_data(self, s_type, id):
        """Returns Spotify API search result for given type and ID. """
        payload = {}

        # Get track data
        url = self.URLs['TRACKS'] + id

        # Get track features data if passed in
        if s_type == "features":
            url = self.URLs['FEATURES'] + id

        # Get playlist feature if passed in
        if s_type == "playlist":
            url = self.URLs['PLAYLIST'] + id

        r = requests.get(url, headers=self._get_headers(),
                         params=payload)
        return r.json()


