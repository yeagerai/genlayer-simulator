import json
from backend.node.genvm.icontract import IContract
from backend.node.genvm.equivalence_principle import EquivalencePrinciple

class AdaptiveAMM(IContract):
    """
    AdaptiveAMM is an intelligent market-making contract that takes in real-time market data and
    outputs a JSON response with the recommended actions (order placements and cancellations) to
    be executed externally.   
    """
    def __init__(self, exchange:str):
        """
        Initializes the AdaptiveAMM intelligent contract with default parameters.
        """
        self.exchange = exchange
        self.symbol = "SUI/USDT"
        self.balance_percentage_to_use = 0.5
        self.max_order_balance_percentage = 0.1
        self.randomness_factor = 0.01  
        self.volatility_threshold = 0.01
        self.max_order_size = 10000  
        self.min_order_size = 1000  

        # Retrieve market data through simulation functions. It should create a conexion with
        # ccxt and get this data.
        self.order_book = self.get_order_book()
        self.current_price = self.get_current_price()
        self.volume = self.get_volume()
        self.open_orders = self.get_open_orders()
        self.balance = self.get_balance()

        self.resolve_response = {}

    # Simulated data retrieval functions
    def get_order_book(self):
        """
        Simulates retrieving the order book data.
        """
        return {
            "bids": [
                [3.2, 10000],
                [3.198, 38000],
                [3.195, 45000]
            ],
            "asks": [
                [3.221, 6700],
                [3.224, 49000],
                [3.225, 70000]
            ]
        }

    def get_current_price(self):
        """
        Simulates retrieving the current price of the asset.
        """
        return 3.22

    def get_volume(self):
        """
        Simulates retrieving the 24-hour trading volume for the asset symbol.
        """
        return 1000000

    def get_open_orders(self):
        """
        Simulates retrieving the user's current open orders.
        """
        return [
            {"id": 1, "side": "buy", "price": 3.198, "amount": 20000},
            {"id": 2, "side": "buy", "price": 3.195, "amount": 37000},
            {"id": 3, "side": "sell", "price": 3.224, "amount": 25000},
            {"id": 4, "side": "sell", "price": 3.225, "amount": 55000}
        ]

    def get_balance(self):
        """
        Simulates retrieving the balance available for the asset symbol.
        """
        return {"SUI": 300000, "USDT": 12999}

    async def _resolve(self, symbol: str) -> dict:
        """
        Processes the input market data and returns a JSON with recommended actions (order placements and cancellations).
        """
        self.symbol = symbol
        final_result = {}
        
        async with EquivalencePrinciple(
            result=final_result,
            principle="Analyze order book, current price, volume, and balance to suggest adaptive order placements",
            comparative=True,
        ) as eq:
            task = f"""You are an adaptive market maker in '{self.exchange}' for the trading symbol '{self.symbol}' on a centralized exchange. 
            Your goal is to optimize liquidity and minimize risk by strategically placing and canceling buy and sell orders. 
            Analyze the following market data and create a response in JSON format that contains recommended actions for 
            order placements and cancellations, considering multiple dynamic factors and potential market conditions.

            Market Data:
            - exchange: {self.exchange}
            - symbol: {self.symbol}
            - Order Book (bid and ask prices with volumes): {json.dumps(self.order_book)}
            - Current Price: {self.current_price}
            - 24-hour Volume: {self.volume}
            - Open Orders: {json.dumps(self.open_orders)}
            - Balance: {json.dumps(self.balance)}
            - Balance Percentage to Use: {self.balance_percentage_to_use}  # % of total balance to allocate to market making
            - Max Order Balance Percentage: {self.max_order_balance_percentage}  # % of balance to allocate per individual order
            - Volatility Threshold: {self.volatility_threshold}
            - Max Order Size: {self.max_order_size}
            - Min Order Size: {self.min_order_size}
            - Randomness Factor: {self.randomness_factor}

            Consider the following criteria for adjusting the market-making strategy:

            1. **Price Volatility**: Adjust order sizes and spread between buy and sell orders to minimize slippage during high volatility. 
              If the volatility exceeds the defined threshold, reduce the order size closer to the min_order_size to mitigate risks. 

            2. **Trade Volume**: Increase liquidity by placing more orders in periods of high volume, while scaling down during low activity 
              to avoid potential manipulation or abnormal price shifts.

            3. **Market Trends**: Determine if the symbol is in an uptrend, downtrend, or neutral market condition. If an uptrend is detected, 
              favor buy orders closer to the current price to capture price appreciation; in a downtrend, place more sell orders to capitalize 
              on selling pressure. Neutral trends can focus on balanced buy-sell order placement.

            4. **Order Book Depth and Balance**: Observe bid and ask levels to identify areas of significant support and resistance. 
              Place buy orders slightly below major support levels and sell orders slightly above resistance points to align with supply 
              and demand patterns. Avoid placing large orders that may disrupt market equilibrium.

            5. **Randomness Factor**: Introduce controlled randomness to adjust the order prices slightly away from standard levels to reduce 
              predictability and protect against arbitrage bots.

            6. **Balance Constraints**: Ensure that the total allocation of orders does not exceed {self.balance_percentage_to_use * 100}% of 
              the available balance for each asset in {self.balance}. Additionally, each individual order should not exceed 
              {self.max_order_balance_percentage * 100}% of the total balance to manage risk.

            7. **Market Sentiment and News**: If there is relevant news or events impacting {self.symbol}, adjust the aggressiveness of order 
              placements accordingly. For example, increase the spread in cases of high uncertainty or significant news to protect against 
              sudden adverse movements.

            Respond with the following JSON structure:
            {{
                "cancel_orders": [int],  // List of order IDs to cancel
                "new_orders": [
                    {{
                        "side": str,  // 'buy' or 'sell'
                        "price": float,  // Optimal price based on market conditions
                        "amount": float  // Order size determined by volatility, balance constraints, and volume
                    }}
                ],
                "reason_decision": str // An explanation of the decision that includes factors influencing order placement, balance utilization, and other key criteria
            }}
            It is mandatory that you respond only using the JSON format above,
            nothing else. Don't include any other words or characters,
            your output must be only JSON without any formatting prefix or suffix.
            AVOID USING '```json' in the beggining of your response Just return something like the JSON structure.
            This result should be perfectly parseable by a JSON parser without errors.
            Make sure that your JSON response is limited to recommended actions only. Adjust order sizes dynamically based on the 
            volatility threshold, balance constraints, and current market conditions. Provide an efficient strategy for the next set of 
            market making activities, optimizing liquidity provision and minimizing risks.
            """
            result = await eq.call_llm(task)
            eq.set(result)

        return json.loads(final_result["output"])
    
    async def resolve(self, symbol: str) -> None:
        """
        Public method to process market data and update `resolve_response`.
        Calls `_resolve` to perform the async task and update `resolve_response`.
        """
        self.resolve_response = await self._resolve(symbol)
    
    def get_resolve_response(self) -> dict:
        """
        Returns the most recent `resolve_response`, which includes:
            - `cancel_orders`: List of order IDs to cancel.
            - `new_orders`: List of recommended new orders with side, price, and amount.
            - `reason_decision`: Explanation of the decision-making process.
        """
        return self.resolve_response