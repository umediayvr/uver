from ..Versioned import Versioned
from ..Versioned import Software
from ..Versioned import Addon

class AddonNotFoundError(Exception):
    """Addon not found in the softwares error."""

class Parser(object):
    """
    Abstract parser.

    Returns a list of software instances based on the addon and software
    information (@see softwares)
    """

    def __init__(self):
        """
        Create a software.
        """
        self.__softwares = {}
        self.__addons = {}

    def addSoftwareInfo(self, softwareName, version, options={}):
        """
        Add an addon to a specific software.
        """
        assert isinstance(options, dict), \
            'options need to be a dictionary'

        self.__softwares[softwareName] = {
            'version': version,
            'options': dict(options)
        }

    def addAddonInfo(self, softwareName, addonName, options={}):
        """
        Add an addon to a specific software.
        """
        assert isinstance(options, dict), \
            'options need to be a dictionary'

        if softwareName not in self.__addons:
            self.__addons[softwareName] = {}

        self.__addons[softwareName][addonName] = {
            'options': dict(options)
        }

    def softwares(self):
        """
        Return a list of softwares based on the added software/addon info.
        """
        # now creating softwares
        result = []
        for softwareName in self.__softwares.keys():
            softwareVersion = self.__softwares[softwareName]['version']
            softwareOptions = self.__softwares[softwareName]['options']

            # creating a software instance
            software = Software(
                softwareName,
                softwareVersion
            )

            # setting software options
            self.__setVersionedOptions(software, softwareOptions)

            # adding addons to the software
            self.__addAddonsToSoftware(software)

            # adding software to result
            result.append(software)

        return result

    def __addAddonsToSoftware(self, software):
        """
        Add addons to a software.

        @private
        """
        assert isinstance(software, Software), \
            "Invalid software type!"

        softwareName = software.name()

        # creating addons for the software
        if softwareName in self.__addons:
            for addonName, addonContent in self.__addons[softwareName].items():

                if addonName not in self.__softwares:
                    raise AddonNotFoundError(
                        'Could not find a version for the addon "{0}"'.format(
                            addonName
                        )
                    )

                addonVersion = self.__softwares[addonName]['version']
                addonOptions = addonContent['options']

                # creating addon
                addon = Addon(
                    addonName,
                    addonVersion
                )

                # setting addon options
                self.__setVersionedOptions(addon, addonOptions)

                # adding addon to software
                software.addAddon(addon)

    def __setVersionedOptions(self, versioned, options):
        """
        Set options to a versioned instance.

        @private
        """
        assert isinstance(versioned, Versioned), \
            "Invalid versioned type"

        for optionName, optionValue in options.items():
            versioned.setOption(optionName, optionValue)
