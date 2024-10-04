from dataclasses import dataclass
from backend.protocol_rpc.endpoint_generator import _serialize


def test_serialize():
    assert _serialize(1) == 1
    assert _serialize(1.1) == 1.1
    assert _serialize("1") == "1"
    assert _serialize(True) == True
    assert _serialize(None) == None
    assert _serialize(()) == []
    assert _serialize({}) == {}
    assert _serialize(dataclass()) == {}
    assert _serialize("test") == "test"
    assert _serialize((1, 2, ["test", False, ()])) == [1, 2, ["test", False, []]]
    assert _serialize({"test": 1, "test2": {"test3": "test4"}}) == {
        "test": 1,
        "test2": {"test3": "test4"},
    }
