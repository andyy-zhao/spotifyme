import requests
import json
from track import Track
from playlist import Playlist

class SpotifyClient:
    def __init__(self, authorization_token, user_id):
        """
        :param authorization_token (str): Spotify API token
        :param user_id (str): Spotify user id
        """
        self.authorization_token = authorization_token
        self.user_id = user_id
    
    def get_api_request(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.authorization_token}"
            }
        )
        return response

    def post_api_request(self, url, data):
        response = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.authorization_token}"
            }
        )
        return response
    
    def get_last_played_tracks(self, limit = 10):
        """ Get the last 10 tracks played by user

        :param limit (int): Number of tracks to get. Should be <= 50
        :return tracks (list of Track): List of last played tracks
        """
        # GET url
        url = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}"
        response = self.get_api_request(url)
        response_json = response.json()
        # return response_json

        # name, id, artist
        tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]) for track in response_json["items"]]
        return tracks

    def get_track_recommendations(self, seed_tracks, limit=50):
        """Get a list of recommended tracks starting from a number of seed tracks.

        :param seed_tracks (list of Track): Reference tracks to get recommendations. Should be 5 or less.
        :param limit (int): Number of recommended tracks to be returned
        :return tracks (list of Track): List of recommended tracks
        """

        seed_tracks_url = ""
        for seed_track in seed_tracks:
            seed_tracks_url += seed_track.id + ","
            # removing comma at the end
        seed_tracks_url = seed_tracks_url[:-1]
        url = f"https://api.spotify.com/v1/recommendations?seed_tracks={seed_tracks_url}&limit={limit}"
        response = self.get_api_request(url)
        response_json = response.json()
        tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) for track in response_json["tracks"]]
        return tracks
    
    def generate_playlist(self, name):
        """
        :param name (str): New playlist name
        :return playlist (Playlist): Newly created playlist
        """
        # Request body
        data = json.dumps({
            "name": name,
            "description": "Recommended songs",
            "public": True
        })

        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response = self.post_api_request(url, data)
        response_json = response.json()

        playlist_id = response_json["id"]
        playlist = Playlist(name, playlist_id)
        return playlist

    def add_songs(self, playlist, tracks):
        """Add tracks to a playlist.
        :param playlist (Playlist): Playlist to which to add tracks
        :param tracks (list of Track): Tracks to be added to playlist
        :return response: API response
        """
        track_uris = [track.get_spotify_uri() for track in tracks]
        data = json.dumps(track_uris)
        url = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
        response = self.post_api_request(url, data)
        response_json = response.json()
        return response_json

# lastplayedtracks = SpotifyClient('BQDZmjahIpYuU6ztj2rQ6Y5nVUW5TUiuC6-JW9pVXsZicxg_w5qQLTjv-E3KaIpTYOKSy_JY4yRSDx4GLC6oEJ6NXpj0--19aGD0FaDo4yGTjlzBco380y9qg5PEB_9yRziKKkYFGsJykIe4E4abt5QU2haD2UGldLpp6sGoAMtsUgKz13wlJoBvMJ5CDaqBLfJ6lIh6U3dOTDhE3uyySJnESQg2jD5Q-lwb7mRZu1c4kxzUr1JJmuP02HqChNk', 'gsyduhgozpv87cedz8ap5wmh4')
# lastplayedtrackslst = lastplayedtracks.get_last_played_tracks(3)
# print(lastplayedtrackslst)

# print(f"\nHere are the last 3 tracks you listened to on Spotify:")
# for index, track in enumerate(lastplayedtrackslst):
#     print(f"{index+1} - {track}")

