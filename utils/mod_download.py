# -*- coding = utf-8 *-*

# MIT License
#
# Copyright (c) 2019 Konrad Pagacz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import requests
import tqdm

class FileDownloader():
    """Handles downloading files from a URL.

    Attributes:
          url: str of the URL of the file to download
          write_folder: path to a folder to download files

    Examples:
          >>> f = FileDownloader("link").download()
    """
    def __init__(self,
                 url: str = None,
                 write_folder: str = "mod_downloads/"):
        self.url = url
        self.write_folder = write_folder

    def download(self,
                 url: str = None,
                 write_folder: str = "mod_downloads/"):
        """Downloads the file from the URL.

        Args:
            url: url to the downloaded file
            write_folder: folder to write the file into

        Returns:

        """
        if url is None:
            url = self.url

        assert isinstance(url, str), "URL {} is not a str object".format(url)
        assert isinstance(write_folder, str), "Path {} is not a str object.".format(write_folder)
        return download_with_progress_bar(url, write_folder)

def download_with_progress_bar(url: str,
                               write_folder: str):
    """Downloads the file from the URL.
    It does it with a pretty progress bar curtosy of tqdm!

    Args:
        url: url to the downloaded file
        write_folder: folder to write the file into

    Returns:

    """
    # Checking whether the folders exist and creating the ones needed
    os.makedirs(os.path.dirname(write_folder), exist_ok=True)

    # Getting the file name from URL
    assert isinstance(url, str), "URL {} is not a str.".format(url)
    try:
        file_name = get_mod_name_from_url(url)
    except ValueError as error:
        print(("Encountered an error in extraction of the file name: {} "
               "Using the url as the file name.").format(error))
        file_name = url

    # File download
    with open(write_folder + file_name, "wb") as output_file:
        response = requests.get(url, stream=True)
        chunk_size = 1024*1024
        for data in tqdm.tqdm(response.iter_content(chunk_size=chunk_size),
                              unit="MB",
                              desc=file_name):
            output_file.write(data)

    # return True

def get_mod_name_from_url(url: str) -> str:
    """Extracts the file name from the url.

    Args:
        url: url of a downloaded file

    Returns:
        str: name of the file name

    Examples:
        >>> FileDownloader._get_mod_name_from_url(("https://files.nexus-cdn.com/110/3863/"
        >>> "SkyUI_5_1-3863-5-1.7z?md5=5yKmT54-6qBhgCjAYwUuxg&expires=1552787172&"
        >>> "user_id=522107&rip=31.183.199.94"))
        SkyUI_5_1-3863-5-1.7z
    """
    # Splitting the url into parts on '/' and getting the last part containing the file name
    last_part = url.split(sep="/")[-1]

    # Regex search for the file name
    pattern = r"^.+(?=\?)"
    regex = re.compile(pattern=pattern)
    match = re.match(regex, last_part)
    if match:
        file_name = match[0]
    else:
        raise ValueError(("Could not find the file name in"
                          " the last part of the url {}.").format(last_part))
    return file_name
