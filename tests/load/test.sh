#!/bin/bash

# Base URL of the application
BASE_URL="http://localhost:4000"

# Number of requests and concurrency level
REQUESTS=1000
CONCURRENCY=50

echo "Starting load test for create_db endpoint"
oha -n $REQUESTS -c $CONCURRENCY -m POST -d '{"action": "create_db"}' -H "Content-Type: application/json" --no-tui  $BASE_URL

echo "Starting load test for create_tables endpoint"
oha -n $REQUESTS -c $CONCURRENCY -m POST -d '{"action": "create_tables"}' -H "Content-Type: application/json" --no-tui  $BASE_URL

echo "Starting load test for create_random_validators endpoint"
oha -n $REQUESTS -c $CONCURRENCY -m POST -d '{"action": "create_random_validators", "min_stake": 8.0, "max_stake": 12.0, "number_of_validators": 10}' -H "Content-Type: application/json" --no-tui  $BASE_URL

# Assume from_address is obtained from a previous step or hardcoded for the test
FROM_ADDRESS="test_address"

echo "Starting load test for fund_account endpoint"
oha -n $REQUESTS -c $CONCURRENCY -m POST -d "{\"action\": \"fund_account\", \"address\": \"$FROM_ADDRESS\", \"amount\": 10.0}" -H "Content-Type: application/json" --no-tui  $BASE_URL

# Contract deployment test requires reading the contract file and constructing a valid payload
CONTRACT_CODE=$(<examples/contracts/wizard_of_coin.py)
DATA=$(jq -n --arg from_address "$FROM_ADDRESS" --arg class_name "WizardOfCoin" --arg contract_code "$CONTRACT_CODE" --arg initial_state '{"have_coin": "True"}' '{from_account: $from_address, class_name: $class_name, contract_code: $contract_code, initial_state: $initial_state}')

echo "Starting load test for deploy_intelligent_contract endpoint"
oha -n $REQUESTS -c $CONCURRENCY -m POST -d "{\"action\": \"deploy_intelligent_contract\", \"data\": $DATA}" -H "Content-Type: application/json" --no-tui  $BASE_URL

# Contract execution test
FUNCTION="WizardOfCoin.ask_for_coin"
ARGS='["Can you please give me my coin?"]'

echo "Starting load test for call_contract_function endpoint"
oha -n $REQUESTS -c $CONCURRENCY -m POST -d "{\"action\": \"call_contract_function\", \"from_address\": \"$FROM_ADDRESS\", \"contract_address\": \"$CONTRACT_ADDRESS\", \"function\": \"$FUNCTION\", \"args\": $ARGS}" -H "Content-Type: application/json" --no-tui  $BASE_URL
