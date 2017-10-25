import os
import glob
import json
from .Loader import Loader

# compatibility with python 2/3
try:
    basestring
except NameError:
    basestring = str

class UnexpectedRootContentError(Exception):
    """Unexpected root content error."""

class UnexpectedAddonsDataError(Exception):
    """Unexpected addons data error."""

class UnexpectedAddonContentError(Exception):
    """Unexpected addon content error."""

class UnexpectedVersionFormatError(Exception):
    """Unexpected version format error."""

class InvalidDirectoryError(Exception):
    """Invalid directory Error."""

class InvalidFileError(Exception):
    """Invalid file Error."""

class JsonLoader(Loader):
    """
    Loads a list of softwares from a json.
    """

    def addFromJson(self, jsonContents):
        """
        Add softwares and addons from json contents.

        Expected format:
        {
            "a": "1.0.0",
            "b": "1.1.0",
            "c": {
                "version": "1.2.5",
                "addons": {
                    "a": {
                        "options": { // options as addon
                            "enabled": true
                        }
                    },
                    "b": {
                        "options": {
                            "enabled": false
                        }
                    }
                },
                "options": { // options as standalone
                    "foo": 10
                }
            }
        }
        """
        contents = json.loads(jsonContents)

        # root checking
        if not isinstance(contents, dict):
            raise UnexpectedRootContentError('Expecting object as root!')

        for softwareName, softwareContents in contents.items():
            self.__addParsedSoftware(softwareName, softwareContents)

    def addFromJsonFile(self, fileName):
        """
        Add json from a file.

        The json file need to follow the format expected
        by {@link addFromJson}.
        """
        # making sure it's a valid file
        if not (os.path.exists(fileName) and os.path.isfile(fileName)):
            raise InvalidFileError(
                'Invalid file "{0}"!'.format(fileName)
            )

        with open(fileName, 'r') as f:
            contents = '\n'.join(f.readlines())
            self.addFromJson(contents)

    def addFromJsonDirectory(self, directory):
        """
        Add json from inside of a directory with json files.

        The json file need to follow the format expected
        by {@link addFromJson}.
        """
        # making sure it's a valid directory
        if not (os.path.exists(directory) and os.path.isdir(directory)):
            raise InvalidDirectoryError(
                'Invalid directory "{0}"!'.format(directory)
            )

        # collecting the json files and loading them to the loader.
        for fileName in glob.glob(os.path.join(directory, '*.json')):
            self.addFromJsonFile(fileName)

    def __addParsedSoftware(self, softwareName, softwareContents):
        """
        Add a software based on the parsed software contents.

        @private
        """
        options = {}
        addons = {}
        version = None

        # detecting if it's a compound format (with addons, options)
        if isinstance(softwareContents, dict):
            if 'version' in softwareContents:
                version = softwareContents['version']

            if 'options' in softwareContents:
                options = softwareContents['options']

            if 'addons' in softwareContents:
                addons = softwareContents['addons']

        # when the value is a string (version)
        elif isinstance(softwareContents, basestring):
            version = softwareContents

        # ortherwise there's a problem
        if not version:
            raise UnexpectedVersionFormatError(
                'Could not decode version for "{0}"'.format(softwareName)
            )

        # adding software
        self.addSoftwareInfo(softwareName, version, options)

        # adding addons
        self.__addParsedAddons(softwareName, addons)

    def __addParsedAddons(self, softwareName, addons):
        """
        Add an addon based on the parsed addon contents.

        @private
        """
        # addon checking
        if not isinstance(addons, dict):
            raise UnexpectedAddonsDataError('Expecting object for addons!')

        for addonName, addonData in addons.items():
            addonOptions = {}

            if not isinstance(addonData, dict):
                raise UnexpectedAddonContentError('Expecting object as content for addon!')

            if 'options' in addonData:
                addonOptions = addonData['options']

            self.addAddonInfo(softwareName, addonName, addonOptions)
