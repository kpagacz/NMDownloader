import unittest
from unittest import mock
import sys
import os
import utils.authorization as authorization
sys.path.insert(0, os.path.abspath(".."))


class AuthenticatorTestCase(unittest.TestCase):
    def setUp(self):
        self.auth = authorization.Authenticator()

    def testSettingAnAPIKey(self):
        self.auth.api_key = "apikey"
        self.assertEqual(first=self.auth.api_key,
                         second="apikey", msg="authenticator.api_key(self, value)")

    def testDefaultValueOfApiKey(self):
        self.assertEqual(first=self.auth.api_key, second=None,
                         msg="Default value of api_key is not correct")
    @mock.patch("os.path.isfile")
    def testCreatingAuthenticatorFromFile(self, mock_isfile):
        # Testing reading a key from file and creating an instance of Authenticator

        mock_isfile.return_value = True

        mock_open = mock.mock_open(read_data="apikey")
        with mock.patch("utils.authorization.open", mock_open):
            cls = authorization.Authenticator.from_file("mockname")
        self.assertIsInstance(cls, authorization.Authenticator,
                              msg=("Return of Authenticator.from_file is not an"
                                   "authenticator class"))

    @mock.patch("os.path.isfile")
    def testApikeyCreatedByFromFileConstructor(self, mock_isfile):
        # Testing reading a key from file and creating an instance of Authenticator

        mock_isfile.return_value = True

        mock_open = mock.mock_open(read_data="apikey")
        with mock.patch("utils.authorization.open", mock_open):
            cls = authorization.Authenticator.from_file("mockname")
        self.assertEqual(cls.api_key, "apikey",
                         msg="Apikey created from from_file is not correct")
