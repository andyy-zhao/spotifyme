import os
from spotifyclient import SpotifyClient

def main():
    spotify_client = SpotifyClient(os.getenv("SPOTIFY_AUTHORIZATION_TOKEN"),
                                   os.getenv("SPOTIFY_USER_ID"))

    # get last played tracks
    num_last_played = int(input("How many tracks would you like to use as samples? "))
    last_played = spotify_client.get_last_played_tracks(num_last_played) # array of songs

    print("Here are the most recent songs you listened to: ")
    for index, track in enumerate(last_played):
        print(f"{index+1} - {track}")

    # select the seed tracks
    print("\nEnter a list of up to 5 tracks that you would like to use as seeds. Use indexes separated by a space: (e.g. 1 2) ")
    idxs = input()
    idxs = idxs.split()
    seed_tracks = []
    for index in idxs:
        seed_tracks.append(last_played[int(index) - 1])

    # get recommended tracks based off seed tracks
    recommended_tracks = spotify_client.get_track_recommendations(seed_tracks)

    print("\nHere are the recommended tracks which will be included in your new playlist:")
    for index, track in enumerate(recommended_tracks):
        print(f"{index+1} - {track}")

    # get playlist name from user and create playlist
    playlist_name = input("Enter Playlist Name: ")
    playlist = spotify_client.generate_playlist(playlist_name)
    print(f"\nPlaylist '{playlist.name}' was created successfully.")

    # populate playlist with recommended tracks
    spotify_client.add_songs(playlist, recommended_tracks)
    print(f"\nRecommended tracks successfully uploaded to playlist '{playlist.name}'.")

if __name__ == "__main__":
    main()