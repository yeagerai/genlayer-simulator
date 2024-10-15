from enum import IntEnum


class Methods(IntEnum):
    APPEND_CALLDATA = 0
    GET_CODE = 1
    STORAGE_READ = 2
    STORAGE_WRITE = 3
    CONSUME_RESULT = 4
    GET_LEADER_NONDET_RESULT = 5
    POST_NONDET_RESULT = 6
    POST_MESSAGE = 7


class ResultCode(IntEnum):
    RETURN = 0
    ROLLBACK = 1
    NONE = 2
    ERROR = 3
