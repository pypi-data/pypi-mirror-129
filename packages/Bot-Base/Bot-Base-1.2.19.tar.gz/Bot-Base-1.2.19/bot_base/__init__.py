from .bot import BotBase
import logging
from collections import namedtuple

__version__ = "1.2.19"


logging.getLogger(__name__).addHandler(logging.NullHandler())
VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(
    major=1, minor=2, micro=19, releaselevel="production", serial=0
)
