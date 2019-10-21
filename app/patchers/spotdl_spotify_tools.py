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


def get_user_playlists_metadata(user_id, small=False):
    """
    Get all user's playlist metadata
    :param user_id: User id on spotify
    :param small: Indicating if the metadata should be small or whole
    :return: Array of dictionaries of playlist metadata in following format (When small is True):
            [ { name: % playlist name %, count: % number of tracks %, link: % playlist link % } ]
            Otherwise, it contains the full playlist object as Spotify API show here:
            https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlist/
    """
    links = spotify_tools.get_playlists(user_id)
    playlists_metadata = []

    for playlist_link in links:
        playlist_metadata = get_playlist_metadata(playlist_link)
        playlists_metadata.append(get_small_metadata(playlist_metadata) if small else playlist_metadata)

    return playlists_metadata


def get_artist_albums_metadata(artist_link, small=False):
    """
    Get all artist's albums metadata
    :param artist_link: Artist link on Spotify
    :param small: Indicating if the metadata should be small or whole
    :return: Array of dictionaries of albums metadata in following format (If small is True):
            [ { name: % album name %, count: % number of tracks %, link: % album link % } ]
            Otherwise, it contains the full album object as Spotify API show here:
            https://developer.spotify.com/documentation/web-api/reference/albums/get-album/
    """
    album_base_url = 'https://open.spotify.com/album/'
    fetched_albums = spotify_tools.fetch_albums_from_artist(artist_link)
    albums = []

    for album in fetched_albums:
        albums.append(get_small_metadata(album) if small else get_album_metadata(album_base_url + album['id']))

    return albums


def get_playlist_metadata(playlist_link):
    """
    Get playlist metadata
    :param playlist_link: Playlist link on Spotify
    :return: Playlist metadata as followed in Spotify API in
             https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlist/
    """
    return spotify_tools.fetch_playlist(playlist_link)


def get_album_metadata(album_link):
    """
    Get album metadata
    :param album_link: Album link on Spotify
    :return: Album metadata as followed in Spotify API in:
            https://developer.spotify.com/documentation/web-api/reference/albums/get-album/
            in dictionary of the following format:
             { name: % album name %, count: % number of tracks %, link: % album link % }
    """
    return spotify_tools.fetch_album(album_link)


def fetch_playlist_to_file(playlist_link, file_name):
    """
    Fetching playlist tracks links to file
    :param playlist_link: Playlist link
    :param file_name: The file name to write the tracks links to
    """
    playlist_metadata = get_playlist_metadata(playlist_link)
    fetch_playlist_to_file_by_metadata(playlist_metadata)


def fetch_playlist_to_file_by_metadata(playlist_metadata, file_name):
    """
    Fetching playlist tracks links to file by given playlist metadata
    :param playlist_metadata: Playlist metadata
    :param file_name: The file name to write the tracks links to
    """
    write_tracks_to_file(playlist_metadata['tracks'], file_name)


def fetch_album_to_file(album_link, file_name):
    """
    Fetching album tracks links to file
    :param album_link: Album link
    :param file_name: The file name to write the tracks links to
    """
    album_metadata = get_album_metadata(album_link)
    fetch_album_to_file_by_metadata(album_metadata, file_name)


def fetch_album_to_file_by_metadata(album_metadata, file_name):
    """
    Fetching album tracks links to file by given album metadata
    :param album_metadata: Album metadata
    :param file_name: The file name to write the tracks links to
    """
    tracks = spotify_tools.spotify.album_tracks(album_metadata['id'])
    write_tracks_to_file(tracks, file_name)


def write_tracks_to_file(tracks, file_name):
    """
    Writing tracks links to file
    :param tracks: Tracks list of playlist/album/artist etc.
    :param file_name: the file name to write the tracks links
    """
    spotify_tools.write_tracks(tracks, file_name)


def get_small_metadata(playlist_or_album):
    """
    Getting smaller metadata for playlist or album
    :param playlist_or_album: full metadata for playlist or album
    :return: Returning only the below dictionary as metadata:
            { name: % playlist/album name %, count: % number of tracks %, link: % playlist/album link % }
    """
    return {
        'name': spotify_tools.slugify(playlist_or_album['name'], ok='-_()[]{}'),
        'count': playlist_or_album['tracks']['total'],
        'link':  'https://open.spotify.com/album/' + playlist_or_album['id']
                 if playlist_or_album['type'] == 'album'
                 else playlist_or_album['href']
    }
