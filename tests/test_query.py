import unittest
from src.lib.Versioned import Software, Addon
from src.lib import Query, SoftwareNotFoundError, AddonNotFoundError

class TestQuery(unittest.TestCase):
    """Test query object."""

    def test_constructor(self):
        """Should test the constructor."""
        softwares = self.__getSoftwares()
        query = Query(softwares)

        self.assertEqual(len(softwares), len(query.softwares()))

    def test_softwareNames(self):
        """Should return a list of expected software names."""
        softwares = self.__getSoftwares()
        query = Query(softwares)

        softwareNames = query.softwareNames()

        self.assertEqual(len(softwareNames), len(softwares))
        self.assertListEqual(
            filter(lambda x: x.name() not in softwareNames, softwares),
            []
        )

    def test_softwareUverNames(self):
        """Should return a list of expected uver names."""
        softwares = self.__getSoftwares()
        query = Query(softwares)

        softwareUverNames = query.softwareUverNames()

        self.assertEqual(len(softwareUverNames), len(softwares))
        self.assertListEqual(
            filter(lambda x: x.uverName() not in softwareUverNames, softwares),
            []
        )

    def test_addonNames(self):
        """Should return a list of expected addon names."""
        softwares = self.__getSoftwares()
        query = Query(softwares)
        addonNames = query.addonNames()

        self.assertEqual(len(addonNames), 1)
        self.assertListEqual(['A'], addonNames)

    def test_addonUverNames(self):
        """Should return a list of expected uver addon names."""
        softwares = self.__getSoftwares()
        query = Query(softwares)
        addonNames = query.addonUverNames()

        self.assertEqual(len(addonNames), 1)
        self.assertListEqual(['UVER_A_VERSION'], addonNames)

    def test_softwareByName(self):
        """Should return a software instance by name."""
        softwares = self.__getSoftwares()
        query = Query(softwares)

        for index, software in enumerate(softwares):
            self.assertEqual(
                query.softwareByName(software.name()),
                softwares[index]
            )

    def test_softwareByNameError(self):
        """Should raise an exception when software was not found."""
        softwares = self.__getSoftwares()
        query = Query(softwares)

        success = False
        try:
            query.softwareByName('E')
        except SoftwareNotFoundError:
            success = True

        self.assertTrue(success)

    def test_softwareByUverName(self):
        """Should return a software instance by uver name."""
        softwares = self.__getSoftwares()
        query = Query(softwares)

        for index, software in enumerate(softwares):
            self.assertEqual(
                query.softwareByUverName(software.uverName()),
                softwares[index]
            )

    def test_softwareByUverNameError(self):
        """Should raise an exception when software was not found (uver)."""
        softwares = self.__getSoftwares()
        query = Query(softwares)

        success = False
        try:
            query.softwareByUverName('UVER_E_VERSION')
        except SoftwareNotFoundError:
            success = True

        self.assertTrue(success)

    def test_softwaresByAddonName(self):
        """Should return a list of softwares based on the addon name."""
        softwares = self.__getSoftwares()
        query = Query(softwares)

        softwareList = query.softwaresByAddonName('A')

        self.assertEqual(len(softwareList), 2)

        for software in softwareList:
            self.assertIn(software.name(), ['B', 'C'])

    def test_softwaresByAddonNameError(self):
        """Should raise an exception when addon name was not found."""
        softwares = self.__getSoftwares()
        query = Query(softwares)

        success = False
        try:
            query.softwaresByAddonName('B')
        except AddonNotFoundError:
            success = True

        self.assertTrue(success)

    def test_softwaresByAddonUverName(self):
        """Should return a list of softwares based on the addon uver name."""
        softwares = self.__getSoftwares()
        query = Query(softwares)

        softwareList = query.softwaresByAddonUverName('UVER_A_VERSION')

        self.assertEqual(len(softwareList), 2)

        for software in softwareList:
            self.assertIn(software.name(), ['B', 'C'])

    def test_softwaresByAddonUverNameError(self):
        """Should raise an exception when addon name was not found (uver)."""
        softwares = self.__getSoftwares()
        query = Query(softwares)

        success = False
        try:
            query.softwaresByAddonUverName('B')
        except AddonNotFoundError:
            success = True

        self.assertTrue(success)

    def __getSoftwares(self):
        """Return an expected list of software with addons."""
        result = []

        softwareA = Software('A', '1.1.0')
        result.append(softwareA)

        softwareB = Software('B', '1.0.0')
        softwareB.addAddon(Addon(softwareA.name(), softwareA.version()))
        result.append(softwareB)

        softwareC = Software('C', '0.1.0')
        softwareC.addAddon(Addon(softwareA.name(), softwareA.version()))
        result.append(softwareC)

        softwareD = Software('D', '0.0.1')
        result.append(softwareD)

        return result
