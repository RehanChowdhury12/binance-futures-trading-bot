import logging
from typing import Dict, Optional

from bot.client import BinanceTestnetClient
from bot.validators import validate_order_params, ValidationError


logger = logging.getLogger("trading_bot")


class OrderManager:
    """
    Manages order placement and execution.
    """
    
    def __init__(self, client: BinanceTestnetClient):
        """
        Initialize OrderManager.
        
        Args:
            client: BinanceTestnetClient instance
        """
        self.client = client
        logger.info("OrderManager initialized")
    
    def place_order(self, symbol: str, side: str, order_type: str, 
                   quantity: str, price: Optional[str] = None) -> Dict:
        """
        Validate inputs and place an order.
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY/SELL)
            order_type: Order type (MARKET/LIMIT)
            quantity: Order quantity
            price: Order price (required for LIMIT)
            
        Returns:
            Order response dictionary
            
        Raises:
            ValidationError: If validation fails
            Exception: If order placement fails
        """
        # Validate all parameters
        logger.info(f"Validating order parameters...")
        params = validate_order_params(symbol, side, order_type, quantity, price)
        
        logger.info(f"Order validated: {params['type']} {params['side']} "
                   f"{params['quantity']} {params['symbol']}")
        
        # Check if symbol exists and is tradable
        symbol_info = self.client.get_symbol_info(params['symbol'])
        if not symbol_info:
            raise ValidationError(f"Symbol {params['symbol']} not found or not tradable")
        
        if symbol_info.get('status') != 'TRADING':
            raise ValidationError(f"Symbol {params['symbol']} is not currently trading")
        
        # Place the order based on type
        if params['type'] == 'MARKET':
            return self._place_market_order(params)
        else:  # LIMIT
            return self._place_limit_order(params)
    
    def _place_market_order(self, params: Dict) -> Dict:
        """
        Place a market order.
        
        Args:
            params: Validated order parameters
            
        Returns:
            Order response
        """
        logger.info("=" * 60)
        logger.info("MARKET ORDER REQUEST")
        logger.info("=" * 60)
        logger.info(f"Symbol:   {params['symbol']}")
        logger.info(f"Side:     {params['side']}")
        logger.info(f"Quantity: {params['quantity']}")
        logger.info("=" * 60)
        
        response = self.client.place_market_order(
            symbol=params['symbol'],
            side=params['side'],
            quantity=params['quantity']
        )
        
        self._log_order_response(response)
        
        return response
    
    def _place_limit_order(self, params: Dict) -> Dict:
        """
        Place a limit order.
        
        Args:
            params: Validated order parameters
            
        Returns:
            Order response
        """
        logger.info("=" * 60)
        logger.info("LIMIT ORDER REQUEST")
        logger.info("=" * 60)
        logger.info(f"Symbol:   {params['symbol']}")
        logger.info(f"Side:     {params['side']}")
        logger.info(f"Quantity: {params['quantity']}")
        logger.info(f"Price:    {params['price']}")
        logger.info("=" * 60)
        
        response = self.client.place_limit_order(
            symbol=params['symbol'],
            side=params['side'],
            quantity=params['quantity'],
            price=params['price']
        )
        
        self._log_order_response(response)
        
        return response
    
    def _log_order_response(self, response: Dict) -> None:
        """
        Log order response details.
        
        Args:
            response: Order response from API
        """
        logger.info("=" * 60)
        logger.info("ORDER RESPONSE")
        logger.info("=" * 60)
        logger.info(f"Order ID:       {response.get('orderId', 'N/A')}")
        logger.info(f"Client Order ID: {response.get('clientOrderId', 'N/A')}")
        logger.info(f"Symbol:         {response.get('symbol', 'N/A')}")
        logger.info(f"Status:         {response.get('status', 'N/A')}")
        logger.info(f"Type:           {response.get('type', 'N/A')}")
        logger.info(f"Side:           {response.get('side', 'N/A')}")
        logger.info(f"Price:          {response.get('price', 'N/A')}")
        logger.info(f"Original Qty:   {response.get('origQty', 'N/A')}")
        logger.info(f"Executed Qty:   {response.get('executedQty', 'N/A')}")
        
        # Average price might not be available immediately
        if 'avgPrice' in response and response['avgPrice'] not in ['0', 0, '', None]:
            logger.info(f"Average Price:  {response['avgPrice']}")
        
        logger.info(f"Time in Force:  {response.get('timeInForce', 'N/A')}")
        logger.info(f"Update Time:    {response.get('updateTime', 'N/A')}")
        logger.info("=" * 60)
    
    def print_order_summary(self, response: Dict) -> None:
        """
        Print a user-friendly order summary to console.
        
        Args:
            response: Order response from API
        """
        print("\n" + "=" * 70)
        print("ORDER PLACED SUCCESSFULLY")
        print("=" * 70)
        print(f"Order ID:        {response.get('orderId')}")
        print(f"Symbol:          {response.get('symbol')}")
        print(f"Side:            {response.get('side')}")
        print(f"Type:            {response.get('type')}")
        print(f"Status:          {response.get('status')}")
        print(f"Quantity:        {response.get('origQty')}")
        
        if response.get('type') == 'LIMIT':
            print(f"Price:           {response.get('price')}")
        
        print(f"Executed Qty:    {response.get('executedQty', '0')}")
        
        # Show average price if available
        if 'avgPrice' in response and response['avgPrice'] not in ['0', 0, '', None]:
            print(f"Average Price:   {response['avgPrice']}")
        
        print("=" * 70)
        print()
