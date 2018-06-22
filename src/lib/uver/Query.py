class SoftwareNotFoundError(Exception):
    """Software not found error."""

class AddonNotFoundError(Exception):
    """Addon not found error."""

class Query(object):
    """
    Queries softwares and addons.
    """

    def __init__(self, softwares):
        """Create a query object."""
        self.__setSoftwares(softwares)

    def softwares(self):
        """Return a list of softwares used for queries."""
        return self.__softwares

    def softwareNames(self):
        """
        Return a list of software names.
        """
        return list(map(lambda x: x.name(), self.softwares()))

    def softwareUverNames(self):
        """
        Return a list of software uver names.
        """
        return list(map(lambda x: x.uverName(), self.softwares()))

    def addonNames(self):
        """
        Return a list of all addon names among the softwares.
        """
        result = set()

        for software in self.softwares():
            for addonName in software.addonNames():
                result.add(addonName)

        return list(result)

    def addonUverNames(self):
        """
        Return a list of all addon uver names among the softwares.
        """
        result = set()

        for software in self.softwares():
            for addon in map(lambda x: software.addon(x), software.addonNames()):
                result.add(addon.uverName())

        return list(result)

    def softwareByName(self, name):
        """
        Return a software instance based on software's name.
        """
        for software in self.softwares():
            if name == software.name():
                return software

        raise SoftwareNotFoundError(
            'Could not find software "{0}"'.format(name)
        )

    def softwareByUverName(self, uverName):
        """
        Return a software instance based on software's uver name.
        """
        for software in self.softwares():
            if uverName == software.uverName():
                return software

        raise SoftwareNotFoundError(
            'Could not find software "{0}"'.format(uverName)
        )

    def softwaresByAddonName(self, name):
        """
        Return a list of software instances based on addon's name.
        """
        result = []
        for software in self.softwares():
            if name in software.addonNames():
                result.append(software)

        if not result:
            raise AddonNotFoundError(
                'Could not find any software with addon "{0}"'.format(name)
            )

        return result

    def softwaresByAddonUverName(self, uverName):
        """
        Return a list of software instances based on addon's uver name.
        """
        result = []
        for software in self.softwares():
            for addon in map(lambda x: software.addon(x), software.addonNames()):
                if addon.uverName() == uverName:
                    result.append(software)

        if not result:
            raise AddonNotFoundError(
                'Could not find any software with addon "{0}"'.format(uverName)
            )

        return result

    def __setSoftwares(self, softwares):
        """Set a list of softwares that should be used by the query."""
        assert isinstance(softwares, list), "Unexcepted type!"

        self.__softwares = softwares
