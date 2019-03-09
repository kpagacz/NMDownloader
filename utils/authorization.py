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


class Authenticator:
    """Handles authentication with Nexus Mods site
    """
    def __init__(self, key=None):
        self._api_key = key

    @classmethod
    def from_file(cls, file_name: str = 'api_key.txt'):
        """Imports the authentication key from a text file.

        :type file_name: str
        :param file_name: a str object with name of the .txt file containing the API key
        """
        assert os.path.isfile(file_name), "{file_name} is not a valid path to a file"

        with open(file_name, 'r') as file:
            key = file.read()
        return cls(key)

    @property
    def api_key(self):
        return self._get_api_key()

    @api_key.setter
    def api_key(self, key):
        # Check whether the key is an str object, then call the indirect setter
        assert isinstance(key, str), "api_key needs to be a str object"
        return self._set_api_key(key)

    def _get_api_key(self):
        """Indirect accessor to the api_key property"""
        return self._api_key

    def _set_api_key(self, key):
        """Indirect setter of the api_key property"""
        self._api_key = key
