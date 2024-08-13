from dataclasses import dataclass


@dataclass
class DecodedTransaction:
    from_address: str
    to_address: str
    data: str
    type: str


@dataclass
class DecodedMethodCallData:
    function_name: str
    function_args: str


@dataclass
class DecodedDeploymentData:
    contract_code: str
    constructor_args: str
