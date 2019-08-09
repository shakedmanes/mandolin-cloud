"""
Patching for functions used in `spotify_tools` for using it more definitive for our cause
"""

from spotdl import spotify_tools, const
from app.patchers import spotdl_config

# Setting the client credentials configuration values
const.args.spotify_client_id = spotdl_config.config.client_id
const.args.spotify_client_secret = spotdl_config.config.client_secret


def get_song_metadata(raw_song):
    """
    Get song metadata on Spotify
    :param raw_song: Raw song name string / Spotify link for song
    :return: Song's metadata on Spotify
    """
    return spotify_tools.generate_metadata(raw_song)


def get_user_playlists_metadata(user_id):
    """
    Get all user's playlist metadata
    :param user_id: User id on spotify
    :return: Array of dictionaries of playlist metadata in following format:
            [ { name: % playlist name %, count: % number of tracks %, link: % playlist link % } ]
    """
    links = spotify_tools.get_playlists(user_id)
    playlists_metadata = []

    for playlist_link in links:
        playlists_metadata.append(get_playlist_metadata(playlist_link))

    return playlists_metadata


def get_artist_albums_metadata(artist_link):
    """
    Get all artist's albums metadata
    :param artist_link: Artist link on Spotify
    :return: Array of dictionaries of albums metadata in following format:
            [ { name: % album name %, count: % number of tracks %, link: % album link % } ]
    """
    album_base_url = 'https://open.spotify.com/album/'
    fetched_albums = spotify_tools.fetch_albums_from_artist(artist_link)
    albums = []

    for album in fetched_albums:
        albums.append({
            'name': spotify_tools.slugify(album['name'], ok='-_()[]{}'),
            'count': album['tracks']['total'],
            'link': album_base_url + album['id']
        })

    return albums


def get_playlist_metadata(playlist_link):
    """
    Get playlist metadata
    :param playlist_link: Playlist link on Spotify
    :return: Playlist metadata in dictionary of the following format:
             { name: % playlist name %, count: % number of tracks %, link: % playlist link % }
    """
    playlist = spotify_tools.fetch_playlist(playlist_link)

    return {
        'name': spotify_tools.slugify(playlist['name'], ok='-_()[]{}'),
        'count': playlist['tracks']['total'],
        'link': playlist_link
    }


def get_album_metadata(album_link):
    """
    Get album metadata
    :param album_link: Album link on Spotify
    :return: Album metadata in dictionary of the following format:
             { name: % album name %, count: % number of tracks %, link: % album link % }
    """
    album = spotify_tools.fetch_album(album_link)

    return {
        'name': spotify_tools.slugify(album['name'], ok='-_()[]{}'),
        'count': album['tracks']['total'],
        'link': album_link
    }


def fetch_playlist_to_file(playlist_link, file_name):
    """
    Fetching playlist tracks links to file
    :param playlist_link: Playlist link
    :param file_name: The file name to write the tracks links to
    """
    playlist = spotify_tools.fetch_playlist(playlist_link)
    tracks = playlist['tracks']
    write_tracks_to_file(tracks, file_name)


def fetch_album_to_file(album_link, file_name):
    """
    Fetching album tracks links to file
    :param album_link: Album link
    :param file_name: The file name to write the tracks links to
    """
    album = spotify_tools.fetch_album(album_link)
    tracks = spotify_tools.spotify.album_tracks(album['id'])
    write_tracks_to_file(tracks, file_name)


def write_tracks_to_file(tracks, file_name):
    """
    Writing tracks links to file
    :param tracks: Tracks list of playlist/album/artist etc.
    :param file_name: the file name to write the tracks links
    """
    spotify_tools.write_tracks(tracks, file_name)
