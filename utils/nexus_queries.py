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

"""Module containing the tools for downloading mods from Nexus Mods."""

import typing
import requests


class NexusQuery:
    """Handles API queries to Nexus Mods.
    This class is responsible for handling API queries to Nexus
    Mods site.

    Attributes:
        url (optional): string of a url to request. Must be a complete address
        query_type (optional): a request function, like requests.get or requests.post
        params (optional): a dict of parameters:values passed to request
        headers (optional): a dict of headers:values passed to request
        _base_url (str): defines the base of the base URL of the API,
            defaults to "https://api.nexusmods.com/v1/".

    Returns:
        request.Response

    Examples:

    """

    def __init__(self,
                 url: str = None,
                 query_type: typing.Union[requests.get,
                                          requests.post] = None,
                 params: dict = None,
                 headers: dict = None):
        self.url = url
        self.query_type = query_type
        self.params = params
        self.headers = headers
        self._base_url = "https://api.nexusmods.com/v1/"

    def query(self,
              url: str = None,
              params: dict = None,
              headers: dict = None) -> requests.Response:
        """Sends requests to Nexus API.
        Args:
            url (str, optional): a full url sent to Nexus API via requests functions
            params(dict, optional): parameters to requests, default is declared during
                the initialization of the class
            headers(dict, optional): headers to requests, default is declared during
                the initialization of the class

        Returns:
            requests.Response object

        Examples:

        Raises:
            """
        if params is None:
            params = self.params
        if headers is None:
            headers = self.headers
        if url is None:
            url = self.url
        else:
            url = self._base_url + url

        # Make sure headers include the API key and accept json
        assert "apikey" in headers.keys(), "API key is not provided in headers {}." \
                                           "Make sure headers include 'apikey'.".format(headers)
        assert "accept" in headers.keys(), "accept not included in headers {}." \
                                           "Make sure headers include 'accept'.".format(headers)

        try:
            with self.query_type(url,
                                 params=params,
                                 headers=headers,
                                 timeout=5) as response:
                return response
        except requests.exceptions.ConnectionError as error:
            print("Connection error occurred: {}.".format(error))
            return requests.Response()
        except requests.exceptions.Timeout as error:
            print("Connection timed out: {}.".format(error))
            return requests.Response()
        except requests.exceptions.TooManyRedirects as error:
            print("Too many redirects: {}".format(error))
            return requests.Response()
        except requests.exceptions.HTTPError as error:
            print("An HTTP error occurred: {}.".format(error))
            return requests.Response()
        except requests.exceptions.URLRequired as error:
            print("Please specify the URL: {}.".format(error))
            return requests.Response()


class ModFileQuery(NexusQuery):
    """Generates requests about mod files to Nexus API.
    Inherits from ``NexusQuery``.

    Attributes:
        url (optional): string of a url to request. Must be a complete address
        game_domain (optional): specifies the game, which is modded by the requested mod
        mod_id (optional): specifies the mod id as set by Nexus Mods
        file_id (optional): specifies the file id
        query_type (optional): a request function, like requests.get or requests.post
        params (dict): a dict of parameters:values passed to request
        headers (dict) a dict of headers:values passed to request

    Methods:
        list_files: lists files for a specified mod
        generate_link: generates a download link using the Nexus API

    Returns:
        request.Response object

    Examples:

    """
    def __init__(self,
                 url: str = None,
                 game_domain: str = None,
                 mod_id: int = None,
                 file_id: int = None,
                 query_type=requests.get,
                 params: dict = None,
                 headers: dict = None):
        super(ModFileQuery, self).__init__(url, query_type, params, headers)
        self.game_domain = game_domain
        self.mod_id = mod_id
        self.file_id = file_id

    def list_files(self,
                   game_domain: str = None,
                   mod_id: typing.Union[int, typing.List[int]] = None,
                   params: dict = None,
                   headers: dict = None) -> requests.Response:
        """Requests list of files for a specified mod.
        Game has to be specified by ``game_domain`` and mod by ``mod_id``.

        Args:
            game_domain: a domain of the game the mod is modifying. Example: "skyrim"
            mod_id: Nexus Mods mod id
            params: dictionary of parameters:values to pass to requests
            headers: dictionary of headers:values to pass to requests

        Returns:
            requests.Response

        Examples:

        """
        # Assigning the values from __init__ if not specified in the call
        if game_domain is None:
            game_domain = self.game_domain
        if mod_id is None:
            mod_id = self.mod_id
        if params is None:
            params = self.params
        if headers is None:
            headers = self.headers

        # Creating a URL request
        self.url = ("games/{domain}/mods/{mod_id}/files.json".format(domain=game_domain,
                                                                     mod_id=mod_id))

        print(self.url, params, headers)
        # Executing the query
        response: requests.Response = super(ModFileQuery, self).query(self.url,
                                                                      params=params,
                                                                      headers=headers)

        return response

    def generate_link(self,
                      game_domain: str = None,
                      mod_id: int = None,
                      file_id: int = None,
                      params: dict = None,
                      headers: dict = None) -> requests.Response:
        """

        Args:
            game_domain: a domain of the game the mod is modifying. Example: "skyrim"
            mod_id: Nexus Mods mod id
            file_id: Nexus Mods file id
            params: dictionary of parameters:values to pass to requests
            headers: dictionary of headers:values to pass to requests

        Returns:
            requests.Response object
        """
        # Assigning the values from __init__ if not specified in the call
        if game_domain is None:
            game_domain = self.game_domain
        if mod_id is None:
            mod_id = self.mod_id
        if file_id is None:
            file_id = self.file_id
        if params is None:
            params = self.params
        if headers is None:
            headers = self.headers

        # Creating a URL request
        self.url = ("games/{domain}/mods/{mod_id}/files/{file_id}/"
                    "download_link.json".format(domain=game_domain,
                                                mod_id=mod_id,
                                                file_id=file_id))

        # Executing the query
        response: requests.Response = super(ModFileQuery, self).query(self.url,
                                                                      params=params,
                                                                      headers=headers)
        assert isinstance(response, requests.Response), "response is not a " \
                                                        "requests.Response object."

        return response

    def generate_mod_info(self,
                          mod_id: typing.Union[int, typing.List[int]],
                          game_domain: str = None,
                          params: dict = None,
                          headers: dict = None) -> typing.List[requests.Response]:
        """Attempts to get information about a specified mod.
        Attempts to download information about a mod specified by mod_id via
        a HTTP GET request.

        Args:
            game_domain: game domain specified by Nexus Mods site. Example: "skyrim"
            mod_id: mod id specified by Nexus Mods site
            params: parameters passed to GET request
            headers: headers passed to GET request

        Returns:
            requests.Response
        """
        if game_domain is None:
            game_domain = self.game_domain
        if params is None:
            params = self.params
        if headers is None:
            headers = self.headers

        response_list = []
        for single_id in mod_id:
            # Creating a URL request
            self.url = "games/{game_domain}/mods/{mod_id}.json".format(game_domain=game_domain,
                                                                       mod_id=single_id)

            # Executing the query
            response: requests.Response = super(ModFileQuery, self).query(self.url,
                                                                          params=params,
                                                                          headers=headers)
            assert isinstance(response, requests.Response), "response is not" \
                                                           "a requests.Response object."
            response_list.append(response)

        return response_list
