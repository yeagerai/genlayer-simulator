from typing import Dict, List
from pydantic import BaseModel

class LeaderData(BaseModel):
    state: Dict
    non_det_calls: Dict[str,str] # input, output

class ConsensusData(BaseModel):
    final: bool
    votes: Dict[str,str]
    leader_data: Dict #LeaderData TODO: finish the data enforcing

class ContractData(BaseModel):
    code: str
    state: Dict

class CallContractInputData(BaseModel):
    contract_address: str
    function_name: str
    args: List
