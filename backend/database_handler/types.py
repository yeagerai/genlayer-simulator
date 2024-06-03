from typing import Dict, List
from pydantic import BaseModel, validator
from typing import Optional


class LeaderData(BaseModel):
    state: Dict
    non_det_calls: Dict[str, str]  # input, output


class ConsensusData(BaseModel):
    final: bool
    votes: Dict[str, str]
    leader: Dict  # LeaderData TODO: finish the data enforcing
    validators: Optional[List] = None

    @validator("validators")
    def prevent_none(cls, v):
        assert v is not None, "validators may not be None"
        return v


class ContractData(BaseModel):
    code: str
    state: str


class CallContractInputData(BaseModel):
    contract_address: str
    function_name: str
    args: List
