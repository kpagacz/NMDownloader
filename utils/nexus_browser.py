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


import webbrowser
from typing import Union, List, Optional


class NexusBrowser:
    """Covers the use of the user's default browser to interact with Nexus Mods.

    Attributes:
        file_ids:
        domain_name:
        links:
        _games_dict:

    Examples:

    """
    def __init__(self,
                 file_ids: Union[int, List[int]] = None,
                 domain_name: str = None,
                 links: Union[str, List[str]] = None):
        if file_ids is not None:
            self.file_ids = list(file_ids)
        else:
            self.file_ids = file_ids
        self.domain_name = domain_name
        if links is not None and isinstance(links, str):
            links = [links]
        else:
            self.links = links
        self._games_dict = {
            "morrowind": 100,
            "skyrim": 110,
            "oblivion": 101,
        }

    def _generate_downloadpage_links_from_file_ids(
            self,
            file_ids: Union[int, List[int]],
            domain_name: str
        ) -> List[str]:
        """

        Args:
            file_ids: list of file ids from Nexus Mods
            domain_name: domain name of the game in Nexus Mods

        Returns:
            List of links

        Examples:

        """
        try:
            game_id = self._games_dict[self.domain_name]
        except KeyError as error:
            print("{} is not a valid game name."
                  "Error message: {}".format(domain_name, error))

        links = [("https://www.nexusmods.com/Core/Libs/Common/"
                  "Widgets/DownloadPopUp?id={file_id}&game_id={game_id}"
                  "&source=FileExpander").format(file_id=file_id,
                                                 game_id=game_id)
                 for file_id
                 in file_ids]

        return links

    def open_download_links(self, links: Optional[Union[str, List[str]]] = None):
        """Attempts to open download links in user's default browser.

        Args:
            links: list of str links to open

        Returns:

        """
        # Create links, if there are non supplied
        if links is None:
            links = self.links
            assert isinstance(self.file_ids, List[int]),\
                "{} are not valid file ids.".format(self.file_ids)
            assert isinstance(self.domain_name, str),\
                "{} is not a valid domain name. " \
                "Available are: {}".format(self.domain_name, self._games_dict.keys())
            links = self._generate_downloadpage_links_from_file_ids(self.file_ids,
                                                                    self.domain_name)

        # Attempts to open the default user's browser with submitted links
        for link in links:
            webbrowser.get().open(link)

    def browser_download(self):
        """Streamlines the process of downloading files from the Nexus Mods.
        Reminds user to login before the downloading process. Basically
        a wrapper for open_download_links.

        Returns:
            None
        """
        # User needs to login first, before he can use this function
        print("Remember to log in to Nexus Mods in your default browser"
              "before using this function.")
        self.open_download_links()


