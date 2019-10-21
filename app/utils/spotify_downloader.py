import app.patchers.spotdl_downloader as downloader_patcher
from app.utils.obfuscator import parse_download_id


class SpotifyDownloader(object):
    """
    Class for managing downloads of tracks (playlist/albums/user/artists etc.)
    """

    @staticmethod
    def download_by_download_id(download_id):
        """
        Download tracks by download id
        :param download_id: Download id
        """
        # Parse download id
        parsed_download_id = parse_download_id(download_id)

        for filename in parsed_download_id['filenames']:
            # TODO: Optimize instead downloading same file over times
            downloader_patcher.Downloader.download_list(filename)

    @staticmethod
    def download_single_song(raw_song):
        """
        Download single song by name or song link (Spotify link or Youtube)
        :param raw_song: Song name or song link (Spotify link or Youtube)
        """
        downloader_patcher.Downloader.download_song(raw_song)
