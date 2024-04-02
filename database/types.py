from typing import Dict, List
from dataclasses import dataclass

@dataclass
class LeaderData:
    state: Dict
    non_det_calls: Dict[str,str] # input, output

@dataclass
class ConsensusData:
    final: str
    votes: Dict[str,bool]
    leader_data: LeaderData

@dataclass
class ContractData:
    code: str
    state: Dict

@dataclass
class CallContractInputData:
    contract_address: str
    function_name: str
    args: List
