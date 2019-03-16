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

import json
import os
import typing
import requests
import utils.authorization as authorization


class NexusInterface:
    """Interacts with NexusMods.
    This class is responsible for interactions with Nexus Mods site.

    Attributes:
        authenticator: an instance of Authenticator class with a loaded API key

    Examples:

    """

    def __init__(self,
                 authenticator: authorization.Authenticator = None):
        self.authenticator = authenticator

    def authenticate(self) -> requests.Response:
        """Function, which sends a validation request to the API.
        It check whether the key is valid and also update the information
        about the user (premium or not, saves api_key, etc.

        Returns:
            requests.Response with the response from the API
        """
        # Setting the required headers
        headers = {
            "key": self.authenticator.api_key,
            "accept": "application/json"
        }

        # Getting the response from Nexus
        query = NexusQuery(query_type=requests.get,
                           headers=headers)
        response = query.query("users/validate.json")

        # Checking whether HTTP error occurred
        # Checking whether the response is a response containing the information
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            print("Http error occurred: {}. Connection issues/"
                  " or wrond api key.".format(error))
            return requests.Response

        if response.status_code != 200:
            print("Error occurred during authentication.")
            return requests.Response

        # Saving the body of the response to a profile file
        # Body should contain the information about the user
        decoded = response.json()
        file_name = "profile/user_profile.json"
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, mode="w") as write_file:
            json.dump(obj=decoded)

        return response


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
            headers = self._headers
        if url is None:
            url = self.url
        else:
            url = self._base_url + url

        try:
            with self._query_type(url,
                                  params=params,
                                  headers=headers,
                                  timeout=0.5) as response:
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
        super.__init__(url, query_type, params, headers)
        self.game_domain = game_domain
        self.mod_id = mod_id
        self.file_id = file_id

    def list_files(self,
                   game_domain: str = None,
                   mod_id: int = None,
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
        self.url = ("games/{domain}/mods/{mod_id}/files.json".format(game_domain, mod_id))

        # Executing the query
        response: requests.Response = super.query(self.url, params, headers)

        return response

    def generateLink(self,
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
        self.url = ("games/{domain}/mods/{mod_id}/files/{file_id}/download_link.json".format(game_domain,
                                                                                             mod_id,
                                                                                             file_id))

        # Executing the query
        response: requests.Response = super.query(self.url, params, headers)
        assert isinstance(response, requests.Response), "response is not a requests.Response object"

        return respone
