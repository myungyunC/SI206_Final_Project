import requests
import spotipy
import spotipy.oauth2 as oauth2


class Spotify:
    """Main class to handle all Spotify API calls."""

    URLs = {'PLAYLIST': 'https://api.spotify.com/v1/playlists/{}',
            'PLAYLIST_TRACKS': 'https://api.spotify.com/v1/playlists/{}/tracks',
            'SEARCH': 'https://api.spotify.com/v1/search',
            'TRACKS': 'https://api.spotify.com/v1/tracks/'}

    def __init__(self, id, secret):
        """Initializer for Spotify class."""
        self.client_id = id
        self.client_secret = secret

        # Get Authorization Token
        self.credentials = oauth2.SpotifyClientCredentials(client_id=id,
                                                           client_secret=secret)
        # self.token = self.credentials.get_access_token()
        # print(self.token)
        self.token = "BQDsANVnfNXFHSIfmK8KtXJ7TPovXzhPSgL_DmWaQTBChX6C-f_foj4Spz_OyT4vwWW8RxAdEutv0cFPXFI"
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
