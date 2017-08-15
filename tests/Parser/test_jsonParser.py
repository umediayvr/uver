import json
from src.lib.Parser import \
    JsonParser, \
    UnexpectedRootContentError, \
    UnexpectedAddonsDataError, \
    UnexpectedAddonContentError, \
    UnexpectedVersionFormatError
from CommonParser import CommonParser

class TestJsonParser(CommonParser):
    """Test json parser object."""

    def test_constructor(self):
        """Should test the constructor."""
        JsonParser()

    def test_emptySoftwares(self):
        """Should test the result when the parser is empty."""
        parser = JsonParser()

        self.assertEqual(parser.softwares(), [])

    def test_addingJson(self):
        """Should test adding json to the parser."""
        parser = JsonParser()

        softwareInfos = {
            'a': {
                'version': '10.1',
                'options': {
                    'a': 1
                }
            },
            'b': {
                'version': '12.1',
                'addons': {
                    'a': {
                        'options': {
                            'enabled': True
                        }
                    }
                }
            },
            'c': '10.0.1'
        }

        # adding sotwares to the parser
        jsonString = json.dumps(softwareInfos)
        parser.addFromJson(jsonString)

        # checking if the softwares were parsed properly
        softwares = parser.softwares()
        self.checkSoftwareInfo(softwareInfos, softwares)
        self.checkAddonsInfo(softwareInfos, softwares)

    def test_unexpectedRootContent(self):
        """
        Should fail when json does not have the proper format for the root.
        """
        parser = JsonParser()

        softwareInfos = [{
            'a': '10.1'
        }]
        jsonString = json.dumps(softwareInfos)

        success = False
        try:
            parser.addFromJson(jsonString)
        except UnexpectedRootContentError:
            success = True

        self.assertTrue(success)

    def test_unexpectedVersionFormat(self):
        """
        Should fail when json does not have the proper format for the version.
        """
        parser = JsonParser()

        softwareInfos = {
            'a': ['10.0']
        }
        jsonString = json.dumps(softwareInfos)

        success = False
        try:
            parser.addFromJson(jsonString)
        except UnexpectedVersionFormatError:
            success = True

        self.assertTrue(success)

    def test_unexpectedAddonsData(self):
        """
        Should fail when json does not have the proper format for the addons.
        """
        parser = JsonParser()

        softwareInfos = {
            'a': {
                'version': '10.1',
                'addons': [
                ]
            },
            'b': '10.10'
        }
        jsonString = json.dumps(softwareInfos)

        success = False
        try:
            parser.addFromJson(jsonString)
        except UnexpectedAddonsDataError:
            success = True

        self.assertTrue(success)

    def test_unexpectedAddonContent(self):
        """
        Should fail when json does not have the proper format for the addon itself.
        """
        parser = JsonParser()

        softwareInfos = {
            'a': {
                'version': '10.1',
                'addons': {
                    'a': None
                }
            },
            'b': '10.10'
        }
        jsonString = json.dumps(softwareInfos)

        success = False
        try:
            parser.addFromJson(jsonString)
        except UnexpectedAddonContentError:
            success = True

        self.assertTrue(success)
