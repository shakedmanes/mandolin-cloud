"""
Patching for `downloader` module in spotdl
"""
from spotdl import downloader as spotdl_downloader


class Downloader(object):

    @staticmethod
    def download_song(raw_song):
        """
        Download single song
        :param raw_song: Song name or youtube/spotify link
        """
        song_downloader = spotdl_downloader.Downloader(raw_song=raw_song)
        song_downloader.download_single()

    @staticmethod
    def download_list(list_file, skip_file=None, write_successful_file=None):
        """
        Download list of songs
        :param list_file: file list contains all the songs to download
        :param skip_file: file contains songs to skip when downloading
        :param write_successful_file: file to write successful downloads of songs
        """
        list_downloader = spotdl_downloader.ListDownloader(
            tracks_file=list_file,
            skip_file=skip_file,
            write_successful_file=write_successful_file
        )

        list_downloader.download_list()
