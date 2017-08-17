import json
import os
from src.lib.Loader import JsonDirectoryLoader, InvalidDirectoryError
from CommonLoader import CommonLoader

class TestJsonDirectoryLoader(CommonLoader):
    """Test json directory loader object."""

    __rootPath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    __jsonDirectory = os.path.join(__rootPath, 'data', 'json')

    def test_constructor(self):
        """Should test the constructor."""
        JsonDirectoryLoader()

    def test_emptySoftwares(self):
        """Should test the result when the loader is empty."""
        loader = JsonDirectoryLoader()

        self.assertEqual(loader.softwares(), [])

    def test_addingJsonDirectory(self):
        """Should test adding a directory with json files to the loader."""
        loader = JsonDirectoryLoader()

        softwareInfos = {}

        simpleFilePath = os.path.join(self.__jsonDirectory, 'simple.json')
        complexFilePath = os.path.join(self.__jsonDirectory, 'complex.json')
        externalAddons = os.path.join(self.__jsonDirectory, 'externalAddons.json')
        for filePath in [simpleFilePath, complexFilePath, externalAddons]:
            with open(filePath, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    softwareInfos[key] = value

        # adding sotwares to the loader
        loader.addFromJsonDirectory(self.__jsonDirectory)

        # checking if the softwares were parsed properly
        softwares = loader.softwares()
        self.checkSoftwareInfo(softwareInfos, softwares)
        self.checkAddonsInfo(softwareInfos, softwares)

    def test_invalidDirectory(self):
        """
        Should fail when passing an invalid directory.
        """
        loader = JsonDirectoryLoader()

        success = False
        try:
            loader.addFromJsonDirectory('/dev/null/invalid')
        except InvalidDirectoryError:
            success = True

        self.assertTrue(success)
