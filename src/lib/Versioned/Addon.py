from Versioned import Versioned

class Addon(Versioned):
    """
    Implements the addon support to the versioned.
    """

    def __init__(self, *args, **kwargs):
        """
        Create an addon object.
        """
        super(Addon, self).__init__(*args, **kwargs)

        # setting default options
        self.setOption('enabled', True)
