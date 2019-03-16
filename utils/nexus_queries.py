﻿# -*- coding = utf-8 *-*

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

import requests
import utils.authorization as authorization


class NexusInterface:
    """Interacts with NexusMods.
    This class is responsible for interactions with Nexus Mods site.

    Args:
        authenticator: an instance of Authenticator class with a loaded API key
    """

    def __init__(self,
                 authenticator: authorization.Authenticator = None):
        self.authenticator = authenticator

    def authenticate(self) -> requests.Response:
        """Function, which sends a validation request to the API.

        Returns:
            requests.Response with the response from the API
        """
        headers = {
            "key": self.authenticator.api_key,
            "accept": "application/json"
        }

        query = NexusQuery(query_type=requests.get,
                           headers=headers)
        response = query.query("users/validate.json")


        return response


class NexusQuery:
    """Handles API queries to Nexus Mods.
    This class is responsible for handling API queries to Nexus
    Mods site.

    Args:
        url (str): string of a url to request. Must be a complete address
        query_type (request): a request function, like requests.get or requests.post
        params (dict): a dict of parameters:values passed to request
        headers (dict) a dict of headers:values passed to request

    Returns:
        request.Response

    Examples:

    """

    def __init__(self,
                 url=None
                 query_type=None,
                 params: dict = None,
                 headers: dict = None):
        self._url = url
        self._query_type = query_type
        self._params = params
        self._headers = headers
        self._base_url = "https://api.nexusmods.com/v1/"

    def query(self,
              url: str = self._url,
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
            params = self._params
        if headers is None:
            headers = self._headers
        if url is None:
            url = self._base_url + url

        try:
            with self._query_type(url,
                                  params=params,
                                  headers=headers,
                                  timeout=0.5) as r:
                return r
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred: {}.".format(e))
            return requests.Response()
        except requests.exceptions.Timeout as e:
            print("Connection timed out: {}.".format(e))
            return requests.Response()
        except requests.exceptions.TooManyRedirects as e:
            print("Too many redirects: {}".format(e))
            return requests.Response()
        except requests.exceptions.HTTPError as e:
            print("An HTTP error occurred: {}.".format(e))
            return requests.Response()
        except requests.exceptions.URLRequired as e:
            print("Please specify the URL: {}.".format(e))
            return requests.Response()