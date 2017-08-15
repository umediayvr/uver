from src.lib.Parser import Parser, AddonNotFoundError
from CommonParser import CommonParser

class TestParser(CommonParser):
    """Test parser object."""

    def test_constructor(self):
        """Should test the constructor."""
        Parser()

    def test_emptySoftwares(self):
        """Should test the result when the parser is empty."""
        parser = Parser()

        self.assertEqual(parser.softwares(), [])

    def test_softwareInfo(self):
        """Should test adding parsed software info to the parser."""
        parser = Parser()

        softwareInfos = {
            'a': {
                'version': '10.1',
                'options': {
                    'a': 1
                }
            },
            'b': {
                'version': '12.1',
                'options': {
                }
            }
        }

        # adding sotwares to the parser
        for softwareName, softwareData in softwareInfos.items():
            parser.addSoftwareInfo(
                softwareName,
                softwareData['version'],
                softwareData['options'],
            )

        # checking if the softwares were parsed properly
        softwares = parser.softwares()
        self.checkSoftwareInfo(softwareInfos, softwares)

    def test_addonInfo(self):
        """Should test adding parsed addon info to the parser."""
        parser = Parser()

        softwareInfos = {
            'a': {
                'version': '10.1',
                'addons': {
                    'c': {
                        'options': {
                            'enabled': False
                        }
                    }
                },
                'options': {
                    'foo': 1
                }
            },
            'b': {
                'version': '12.1',
                'addons': {
                    'c': {},
                    'd': {},
                },
                'options': {
                    'foo': 1
                }
            },
            'c': {
                'version': '12.1',
                'options': {
                }
            },
            'd': {
                'version': '14.1',
                'options': {
                }
            }
        }

        # adding sotwares & addons to the parser
        for softwareName, softwareData in softwareInfos.items():
            parser.addSoftwareInfo(
                softwareName,
                softwareData['version'],
                softwareData['options'],
            )

            # addons
            if 'addons' in softwareData:
                for addonName, addonData in softwareData['addons'].items():
                    if 'options' in addonData:
                        parser.addAddonInfo(
                            softwareName,
                            addonName,
                            addonData['options']
                        )
                    else:
                        parser.addAddonInfo(
                            softwareName,
                            addonName
                        )

        # checking if the softwares were properly parsed
        softwares = parser.softwares()

        # checking addons
        self.checkAddonsInfo(softwareInfos, softwares)

    def test_addonNotFound(self):
        """Should fail when addon is not declared as software."""
        parser = Parser()

        softwareInfos = {
            'a': {
                'version': '10.1',
                'addons': {
                    'missing': {}
                }
            },
            'b': {
                'version': '10.1',
            }
        }

        # adding sotwares & addons to the parser
        for softwareName, softwareData in softwareInfos.items():
            parser.addSoftwareInfo(
                softwareName,
                softwareData['version']
            )

            # addons
            if 'addons' in softwareData:
                for addonName, addonData in softwareData['addons'].items():
                    parser.addAddonInfo(
                        softwareName,
                        addonName
                    )

        success = False
        try:
            parser.softwares()
        except AddonNotFoundError:
            success = True

        self.assertTrue(success)
