import os
import glob
from JsonParser import JsonParser

class InvalidDirectoryError(Exception):
    """Invalid Directory Error."""

class JsonDirectoryParser(JsonParser):
    """
    Parse a list of softwares from a directory containing json files.
    """

    def addFromJsonDirectory(self, directory):
        """
        Add json files from inside of a directory.

        The json file need to follow the format expected
        by {@link addFromJson}.
        """
        # making sure it's a valid directory
        if not (os.path.exists(directory) and os.path.isdir(directory)):
            raise InvalidDirectoryError(
                'Invalid directory "{0}"!'.format(directory)
            )

        # collecting the json files and loading them to the parser.
        for fileName in glob.glob(os.path.join(directory, '*.json')):
            with open(fileName, 'r') as f:
                contents = '\n'.join(f.readlines())
                self.addFromJson(contents)
