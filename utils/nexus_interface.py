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


import json
import os

import requests

import utils.authorization as authorization
import utils.nexus_queries as nexus_queries
import utils.mod_import as mod_import


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
            "apikey": self.authenticator.api_key,
            "accept": "application/json"
        }

        # Getting the response from Nexus
        query = nexus_queries.NexusQuery(query_type=requests.get,
                                         headers=headers)
        response = query.query("users/validate.json", headers=headers)

        # Checking whether HTTP error occurred
        # Checking whether the response is a response containing the information
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            print("Http error occurred: {}. Connection issues"
                  " or wrong api key.".format(error))
            return requests.Response()

        if response.status_code != 200:
            print("Error occurred during authentication.")
            return requests.Response()

        # Saving the body of the response to a profile file
        # Body should contain the information about the user
        decoded = response.json()
        file_name = os.path.normpath("profile/user_profile.json")
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, mode="wt", encoding="utf-8") as write_file:
            json.dump(obj=decoded, fp=write_file)

        return response

    def import_mod_info(self,
                        importer: mod_import.ModListImporter(),
                        game_domain: str) -> dict:
        """Attempts to download info about mods listed in mod_id.
        Attempts to get the info about mods via HTTP GET request to
        Nexus API. Also outputs the info about mods to a file
        in profile/mod_info.json.

        Args:
            importer:
            game_domain:
            mod_id:

        Returns:
            dict

        Exampmles:
        """
        # Creating a list from mod_id
        mod_id = importer.mod_list

        # Setting the required headers
        headers = {
            "apikey": self.authenticator.api_key,
            "accept": "application/json"
        }

        # Asserting things are what they should be
        assert isinstance(game_domain, str), "{} is not an instance of str.".format(game_domain)
        assert isinstance(mod_id, (int, list)), "{} is not a list.".format(mod_id)

        # Importing mod info
        import_query = nexus_queries.ModFileQuery(game_domain=game_domain,
                                                  headers=headers)
        response_list = import_query.generate_mod_info(headers=headers,
                                                       mod_id=mod_id)

        # Decoding json and creating a dict of mod infos
        mod_info_dict = {}
        for response in response_list:
            decoded = response.json()
            mod_info_dict[decoded["mod_id"]] = decoded

        # Saving infos of all the mods as a .json file
        # Inside profile/mod_infos.json
        path = os.path.normpath("profile/mod_infos.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wt", encoding="utf-8") as output_file:
            json.dump(obj=mod_info_dict, fp=output_file)

        return mod_info_dict

    def import_file_list(self,
                         importer: mod_import.ModListImporter,
                         domain_name: str) -> dict:
        """Attempts to import file lists for a list of mods.
        Attempts to import file lists for a list of mods specified
        by their mod ids via HTTP GET requests to Nexus API.

        Args:
            importer: contains the mod ids
            domain_name: name of the game as described by Nexus Mods

        Returns:
            dict

        Examples:

        """
        mod_ids = importer.mod_list

        # Create the header
        header = {
            "apikey": self.authenticator.api_key,
            "accept": "application/json"
        }

        # Download the file lists via HTTP GET
        file_list_dict = {}
        assert isinstance(domain_name, str), "{} is not a str object.".format(domain_name)
        mod_file_query = nexus_queries.ModFileQuery(game_domain=domain_name,
                                                    headers=header)
        for single_id in mod_ids:
            # Make the request
            response = mod_file_query.list_files(mod_id=single_id).json()

            file_list_dict[single_id] = response

        # Output to a file
        # profile/file_lists.json
        path = os.path.normpath("profile/file_lists.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wt", encoding="utf-8") as output_file:
            json.dump(obj=file_list_dict, fp=output_file)

        return file_list_dict
