from enum import IntEnum


class _NoYes(IntEnum):
    NO = 0
    YES = 1


class _YesNo(IntEnum):
    YES = 0
    NO = 1


class _DiscoveryFlag(IntEnum):
    PLAIN = 0
    DISCOVERED = 4


class _EntityStatus(IntEnum):
    ENABLED = 0
    DISABLED = 1


class _Permission(IntEnum):
    READ_ONLY = 2
    READ_WRITE = 3


class _Priority(IntEnum):
    NOT_CLASSIFIED = 0
    INFORMATION = 1
    WARNING = 2
    AVERAGE = 3
    HIGH = 4
    DISASTER = 5


class _Suppressed(IntEnum):
    NO = 0
    YES = 1


class _ObjectTrigger(IntEnum):
    TRIGGER = 0


class _ObjectInternal(IntEnum):
    TRIGGER = 0
    ITEM = 4
    LLD = 5


class _PrototypeDiscover(IntEnum):
    DISCOVER = 0
    DONT_DISCOVER = 1


class _ObjectSource(IntEnum):
    TRIGGER = 0
    DISCOVERY = 1
    AUTOREGISTRATION = 2
    INTERNAL = 3


from .alert import *
from .audit_log import *
from .dashboard import *
from .discovered_host import *
from .discovered_service import *
from .discovery_check import *
from .discovery_rule import *
from .event import *
from .graph import *
from .graph_item import *
from .graph_prototype import *
from .host import *
from .host_group import *
from .host_interface import *
from .host_prototype import *
from .image import *
from .item import *
from .item_http import *
from .item_preprocessing import *
from .item_prototype import *
from .lld import *
from .map import *
from .media_type import *
from .problem import *
from .proxy import *
from .script import *
from .snmp import *
from .task import *
from .trigger_prototype import *
from .trigger import *
from .user_group import *