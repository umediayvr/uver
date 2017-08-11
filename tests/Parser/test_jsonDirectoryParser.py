import json
import os
from src.lib.Parser import JsonDirectoryParser, InvalidDirectoryError
from CommonParser import CommonParser

class TestJsonDirectoryParser(CommonParser):
    """Test json directory parser object."""

    __rootPath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    __jsonDirectory = os.path.join(__rootPath, 'data', 'json')

    def test_constructor(self):
        """Should test the constructor."""
        JsonDirectoryParser()

    def test_emptySoftwares(self):
        """Should test the result when the parser is empty."""
        parser = JsonDirectoryParser()

        self.assertEqual(parser.softwares(), [])

    def test_addingJsonDirectory(self):
        """Should test adding a directory with json files to the parser."""
        parser = JsonDirectoryParser()

        softwareInfos = {}

        simpleFilePath = os.path.join(self.__jsonDirectory, 'simple.json')
        complexFilePath = os.path.join(self.__jsonDirectory, 'complex.json')
        externalAddons = os.path.join(self.__jsonDirectory, 'externalAddons.json')
        for filePath in [simpleFilePath, complexFilePath, externalAddons]:
            with open(filePath, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    softwareInfos[key] = value

        # adding sotwares to the parser
        parser.addFromJsonDirectory(self.__jsonDirectory)

        # checking if the softwares were parsed properly
        softwares = parser.softwares()
        self.checkSoftwareInfo(softwareInfos, softwares)
        self.checkAddonsInfo(softwareInfos, softwares)

    def test_invalidDirectory(self):
        """
        Should fail when passing an invalid directory.
        """
        parser = JsonDirectoryParser()

        success = False
        try:
            parser.addFromJsonDirectory('/dev/null/invalid')
        except InvalidDirectoryError:
            success = True

        self.assertTrue(success)
