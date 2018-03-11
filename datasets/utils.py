import os
import tarfile
import zipfile
import shutil
from urllib.request import urlretrieve

def extract_archive(file_path, path='.', archive_format='zip'):
    """Extract an archive if it maches tar, tar.gz, tar.bz, or zip formats.

    Arguments:
        file_path: path to the archive file
        path: path to extract the archive to
        archive_format: archive format to try for extracting the file.
            options: 'auto', 'tar', 'zip', and None

    Returns:
        True if a match was found and an archive extraction was completed,
        False otherwise.

    Raises:
        tarfile.TarError: Tar file cannot be extracted
        RuntimeError: There are problems with the extraction of zip format
        KeyboardInterrupt: File extraction is interrupted by user
    """
    if archive_format is None:
        return False
    elif archive_format is 'auto':
        archive_format = ['tar', 'zip']
    else:
        archive_format = [archive_format]

    for archive_type in archive_format:
        if archive_type is 'tar':
            open_fn = tarfile.open
            is_match_fn = tarfile.is_tarfile 
        elif archive_type is 'zip':
            open_fn = zipfile.ZipFile 
            is_match_fn = zipfile.is_zipfile
        if is_match_fn(file_path):
            with open_fn(file_path) as archive:
                try:
                    archive.extractall(path)
                except (tarfile.TarError, RuntimeError, KeyboardInterrupt):
                    if os.path.exists(path):
                        if os.path.isfile(path):
                            os.remove(path)
                        else:
                            shutil.rmtree(path)
                    raise
            return True
        return False

def get_file(fname, origin, extract=False, cache_dir=None, 
             cache_subdir='', archive_format='zip'):
    """Downloads a file from a URL if it not already in the cache.

    By default the file at url `origin` is downloaded to `cache_dir`.
    Files in tar, tar.gz, tar.bz, and zip formats can also be extracted.

    Arguments:
        fname: Name of the file
        origin: Download url of the file
        extract: Whether the downloaded file needs to be extracted
        cache_dir: Download root folder location
        cache_subdir: Download location
        archive_format: ['auto', 'tar', 'zip', None]
    """
    if cache_dir is None:
        cache_dir = os.path.join(os.getcwd(), '.cache')
    datadir_base = os.path.realpath(cache_dir)
    if not os.path.exists(datadir_base):
        try:
            os.makedirs(datadir_base)
        except:
            print("WARNING: Do not have permission to write to {}, writing to /tmp...".format(datadir_base))
            datadir_base = os.path.join('/tmp', '.cache')
    datadir = os.path.join(datadir_base, cache_subdir)
    if not os.path.exists(datadir):
        os.makedirs(datadir)

    if extract:
        untar_path = os.path.join(datadir, fname)
        fpath = untar_path + "." + archive_format
    else:
        fpath = os.path.join(datadir, fname)

    download = False
    if os.path.exists(fpath):
        print("File {} already exists in cache.".format(fname))
    else:
        download = True

    if download:
        print("Downloading data from {}...".format(origin))
        urlretrieve(origin, fpath)

    if extract:
        extract_archive(fpath, datadir, archive_format)

    return os.path.join(datadir, fname)

