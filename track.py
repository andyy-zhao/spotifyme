class Track:
    # A track is a song

    def __init__(self, name, id, artist):
        """
        :param name (str): Track name
        :param id (int): Song ID
        :param artist (str): Song Artist
        """
        self.name = name
        self.id = id
        self.artist = artist

    def get_spotify_uri(self):
        return f"spotify:track:{self.id}"
    
    def __str__(self): 
        return self.name + " by " + self.artist