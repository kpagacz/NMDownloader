import unittest
import utils.mod_import as mod_import

import codecov


class ModListImporterTestCase(unittest.TestCase):
    def setUp(self):
        self.importer = mod_import.ModListImporter()
        self.csv_header = "modids,names\n"
        self.csv_values = ["1,abc\n"
                           "2,def\n"]

    def testModListDefaultValue(self):
        self.assertEqual(self.importer.mod_list,
                         [],
                         msg="Default value of mod_list is not []")

    def testModListSetter(self):
        self.importer.mod_list = [1, 2, 3]
        self.assertEqual(self.importer._mod_list,
                         [1, 2, 3],
                         msg="Setter method did not assign [1, 2, 3] to mod_list")

    def testModListGetter(self):
        self.importer.mod_list = [1, 2]
        self.assertEqual([1, 2],
                         self.importer.mod_list,
                         msg="mod_list getter failed to output correctly")


    def testImportFromCSVWithHeader(self):
        cls = self.importer.from_csv("test_utils/testModImporterFromCSV.csv")
        self.assertIsInstance(cls, mod_import.ModListImporter)
        self.assertEqual([1, 2],
                         cls.mod_list,
                         msg="ModImporter succesfully created, but mod_list is incorrect.")

    def testImportFromExcel(self):
        cls = self.importer.from_excel("test_utils/testModImporterFromExcel.xlsx")
        self.assertIsInstance(cls, mod_import.ModListImporter)
        self.assertEqual([1, 2],
                         cls.mod_list,
                         msg="ModImporter succesfully created, but mod_list is incorrect.")
