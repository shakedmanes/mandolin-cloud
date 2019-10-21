"""
Used for obfuscating file names for creating download_id's
"""
from zlib import compress, decompress
from ast import literal_eval
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from time import time_ns


def obscure(data: bytes) -> bytes:
    """
    Obscure data bytes to unreadable bytes
    :param data: Data bytes to obscure
    :return: Obscured data bytes
    """
    return b64e(compress(data, 9))


def unobscure(obscured: bytes) -> bytes:
    """
    Unobscure obscured data bytes to readable bytes
    :param obscured: Obscured data bytes
    :return: Readable data bytes
    """
    return decompress(b64d(obscured))


def create_download_id(*files):
    """
    Create obscured download id for app requests for downloading files
    :param files: Arguments indicating file names for the files to download
    :return: Obscured download id string
    """
    return str(obscure(bytes(str({'filenames': files}), 'utf-8')), 'utf-8')


def parse_download_id(download_id):
    """
    Parse obscured download id for extract information from download id
    :param download_id: Obscured download id
    :return: Plain download id dictionary object
    """
    return literal_eval(str(unobscure(bytes(download_id, 'utf-8')), 'utf-8'))


def generate_filename(playlist_or_album_name, user_id_or_artist_id=None):
    """
    Generates filename for given user id and playlist name
    :param playlist_or_album_name: Playlist/Album name
    :param user_id_or_artist_id: User id or artists id if given
    :return: filename for given properties
    """
    filename = ''
    if user_id_or_artist_id:
        filename += user_id_or_artist_id + '_'
    filename += playlist_or_album_name + '_' + str(time_ns())
    return filename
