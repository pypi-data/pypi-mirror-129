from enum import IntEnum


class LLDRuleType(IntEnum):
    ZABBIX_AGENT = 0
    ZABBIX_TRAPPER = 2
    SIMPLE_CHECK = 3
    ZABBIX_INTERNAL = 5
    ZABBIX_AGENT_ACTIVE = 7
    EXTERNAL_CHECK = 10
    DATABASE_MONITOR = 11
    IPMI_AGENT = 12
    SSH_AGENT = 13
    TELNET_AGENT = 14
    CALCULATED = 15
    JMX_AGENT = 16
    DEPENDENT_ITEM = 18
    HTTP_AGENT = 19
    SNMP_AGENT = 20


class LLDRuleFilterOperator(IntEnum):
    MATCHES = 8
    DOES_NOT_MATCH = 9


class LLDRulePreprocessing(IntEnum):
    REGULAR_EXPRESSION = 5
    XML_XPATH = 11
    JSONPATH = 12
    DOES_NOT_MATCH_REGULAR_EXPRESSION = 15
    CHECK_FOR_ERROR_IN_JSON = 16
    CHECK_FOR_ERROR_IN_XML = 17
    DISCARD_UNCHANGED_WITH_HEARTBEAT = 20
    PROMETHEUS_PATTERN = 22
    PROMETHEUS_TO_JSON = 23
    CSV_TO_JSON = 24
    REPLACE = 25


LLDRuleOverrideFilterOperator = LLDRuleFilterOperator
