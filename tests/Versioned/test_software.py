import unittest
from uver.Versioned import Software, Addon, InvalidAddonError

class TestSoftware(unittest.TestCase):
    """Test software object."""

    def test_constructor(self):
        """Should test the values passed to the constructor."""
        name = "foo"
        version = "1.1.0"
        software = Software(name, version)

        self.assertEqual(software.name(), name)
        self.assertEqual(software.version(), version)

    def test_defaultOptions(self):
        """Should test the default options of the software."""
        software = Software("foo", "1.1")

        self.assertEqual(len(software.optionNames()), 0)

    def test_addons(self):
        """Should add addons to the software."""
        software = Software("foo", "1.1")

        addons = {
            "a": None,
            "b": None,
            "c": None
        }

        for addonName in addons:
            addon = Addon(addonName, "1.0")
            addons[addonName] = addon
            software.addAddon(addon)

        self.assertEqual(len(addons), len(software.addonNames()))

        # should be the same instance
        for addonName in addons.keys():
            self.assertIs(software.addon(addonName), addons[addonName])

    def test_invalidAddons(self):
        """Should fail to get an invalid addon."""
        software = Software("foo", "1.1")

        success = False
        try:
            software.addon('invalid')
        except InvalidAddonError:
            success = True

        self.assertTrue(success)
