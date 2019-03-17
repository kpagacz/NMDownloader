# -*- coding: utf-8 -*-
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
"""Module containing all the tools associated with importing mod lists.
It contains all the classes, which are responsible for importing
mod ids and mod names.
"""
import csv
import openpyxl


class ModListImporter:
    """A class responsible for importing mod lists.
    This class imports mod lists from files and from other sources.

    Methods:
        from_csv
        from_excel

    Attributes:
        mod_list: list of Nexus Mods mod ids
    """

    def __init__(self, mod_list: list = None):
        """Constructor method of ModListImporter.
        """
        if mod_list is None:
            self.mod_list = []
        else:
            self._mod_list = mod_list

    @classmethod
    def from_csv(cls, file_name: str, modid_column: int = 0):
        """Imports a list of mod ids from a .csv file.
        Mod ids defined by Nexus Mods site.

        Args:
            file_name (str): path to .csv file containing the mod ids
            modid_column (:obj:'int', optional): defines the number of the column with mod ids.
                Defaults to the 1st column in the file = 0.

        Returns:
            mod_import.ModListImporter
        """
        modid_array = []

        with open(file_name, newline="") as csvfile:
            # Recognizes the dialect of the file and whether it has headers
            dialect = csv.Sniffer().sniff(csvfile.readline())
            csvfile.seek(0)
            has_headers = csv.Sniffer().has_header(csvfile.read(1024))
            csvfile.seek(0)

            # Check for column names
            if has_headers:
                fieldnames = csvfile.readline()

            # Reads the modids and adds to modid_array
            csv_reader = csv.reader(csvfile, dialect=dialect)
            for row in csv_reader:
                modid_array.append(int(row[modid_column]))

        modid_array = list(modid_array)
        assert isinstance(modid_array, list), "modid_array is not a list. Expected a list."
        return cls(modid_array)

    @classmethod
    def from_excel(cls, file_name: str, modid_column: int = 0):
        """Imports a list of mod ids from an .xlsx file
        Mod ids defined by Nexus Mods site.

        Args:
            file_name (str): name of the .xlsx file
            modid_column (int): column number of the mod ids

        Returns:
            mod_import.ModListImporter: an instance of ModListImporter with mod ids already imported
        """
        modid_array = []

        book = openpyxl.load_workbook(filename=file_name,
                                      read_only=True)
        sheet = book.active

        # Read in a header
        fieldnames = []
        fieldnames_row = next(sheet.rows)
        for cell in fieldnames_row:
            fieldnames.append(cell.value)

        # Read in modids
        for row in sheet.rows:
            modid_array.append(row[modid_column].value)

        modid_array = list(modid_array)
        assert isinstance(modid_array, list)
        return cls(modid_array)

    @property
    def mod_list(self):
        """list(int): A python list object with mod ids.

        Examples::
            >>> c = ModListImporter([1, 2, 3])
            >>> print(c.mod_list)
            >>> [1, 2, 3]
            >>> c.mod_list = [1, 2]
            >>> print(c.mod_list)
            >>> [1, 2]
        """
        return self._get_mod_list()

    @mod_list.setter
    def mod_list(self, value: list):
        assert isinstance(value, list), "value must be a python list."
        return self._set_mod_list(value)

    def _get_mod_list(self):
        return self._mod_list

    def _set_mod_list(self, value: list):
        self._mod_list = value
