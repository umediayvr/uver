import os
import sys

# querying root directory
root = os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))
)

# adding uver from src to the python's path
sourceFolder = os.path.join(root, "src")
sys.path.insert(
    1,
    os.path.join(root, "src")
)
