import app.patchers.spotdl_spotify_tools as spotify_tools_patcher
from app.utils.obfuscator import generate_filename, create_download_id


class SpotifyInformer(object):
    """
    Class for getting spotify meta data information about user, playlist, albums and artists.
    """

    @staticmethod
    def prepare_user_playlists(user_id):
        """
        Returning user playlists information for further downloading on spotify downloader class
        :param user_id: Spotify user id
        :return: Dictionary in the following format:
                 {
                   user_id: %username of the user%,
                   playlists: [{
                     name: %playlist name%,
                     count: %playlist number of tracks%,
                     link: %playlist link%,
                     download_id: %download id for downloading the playlist%,
                   }],
                   download_id: %download id for downloading all user playlists%
                 }
        """
        # Creating the returning object first
        user_playlists_info = {'user_id': user_id, 'playlists': [], 'download_id': ''}

        # Getting the whole user's playlists metadata
        playlists_metadata = spotify_tools_patcher.get_user_playlists_metadata(user_id)

        # List of all file names for the playlists of the user
        playlists_filenames = []

        # For each playlist, fetch it to file and create download id
        for playlist in playlists_metadata:
            current_filename = generate_filename(playlist['name'], user_id)
            current_download_id = create_download_id(current_filename)
            playlists_filenames.append(current_filename)
            spotify_tools_patcher.fetch_playlist_to_file_by_metadata(playlist, current_filename)
            user_playlists_info['playlists'].append({
                **spotify_tools_patcher.get_small_metadata(playlist),
                'download_id': current_download_id
            })

        # Creating download id for whole playlists
        user_playlists_info['download_id'] = create_download_id(playlists_filenames)

        return user_playlists_info

    @staticmethod
    def prepare_playlist(playlist_link):
        """
        Returning information for further downloading playlist given
        :param playlist_link: Spotify playlist link
        :return: Dictionary in the following format:
                 {
                   name: %playlist name%,
                   count: %playlist number of tracks%,
                   link: %playlist link%,
                   download_id: %download id for downloading the playlist%,
                 }
        """
        # Getting playlist metadata
        playlist_metadata = spotify_tools_patcher.get_playlist_metadata(playlist_link)

        # Generating filename and fetching playlist tracks to file
        playlist_filename = generate_filename(playlist_metadata['name'])
        spotify_tools_patcher.fetch_playlist_to_file_by_metadata(playlist_metadata, playlist_filename)

        return {
            **spotify_tools_patcher.get_small_metadata(playlist_metadata),
            'download_id': create_download_id(playlist_filename)
        }

    @staticmethod
    def prepare_artists_albums(artist_link):
        """
        Returning information for further downloading artist's albums
        :param artist_link: Spotify link for the artist
        :return: Dictionary in the following format:
                 {
                   artist_link: %artist link given%,
                   albums: [{
                     name: %album name%,
                     count: %album number of tracks%,
                     link: %album link%,
                     download_id: %download id for downloading the album%,
                   }],
                   download_id: %download id for downloading all artist's albums%
                 }
        """
        # Creating the returning object first
        artist_albums_info = {'artist_link': artist_link, 'albums': [], 'download_id': ''}

        # Get whole albums metadata for the artists
        albums_metadata = spotify_tools_patcher.get_artist_albums_metadata(artist_link)

        # List of all the albums filenames for the artists
        albums_filenames = []

        # For each album, fetch tracks to file and create download id
        for album_metadata in albums_metadata:
            current_filename = generate_filename(album_metadata['name'], album_metadata['artists'][0]['id'])
            current_download_id = create_download_id(current_filename)
            albums_filenames.append(current_filename)
            spotify_tools_patcher.fetch_album_to_file_by_metadata(album_metadata, current_filename)
            artist_albums_info['albums'].append({
                **spotify_tools_patcher.get_small_metadata(album_metadata),
                'download_id': current_download_id
            })

        # Creating download id for whole albums
        artist_albums_info['download_id'] = create_download_id(albums_filenames)

        return artist_albums_info

    @staticmethod
    def prepare_album(album_link):
        """
        Returning information for further downloading album
        :param album_link: Spotify album link
        :return: Dictionary in the following format:
                 {
                   name: %album name%,
                   count: %album number of tracks%,
                   link: %album link%,
                   download_id: %download id for downloading the album%,
                 }
        """
        # Getting album metadata
        album_metadata = spotify_tools_patcher.get_album_metadata(album_link)

        # Generating filename and fetch albums tracks to file
        album_filename = generate_filename(album_metadata['name'], album_metadata['artists'][0]['id'])
        spotify_tools_patcher.fetch_album_to_file_by_metadata(album_metadata, album_filename)

        return {
            **spotify_tools_patcher.get_small_metadata(album_metadata),
            'download_id': create_download_id(album_filename)
        }
