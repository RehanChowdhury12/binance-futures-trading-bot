import logging
import time
import hmac
import hashlib
from typing import Dict, Optional
from urllib.parse import urlencode

import requests
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException


logger = logging.getLogger("trading_bot")


class BinanceTestnetClient:
    """
    Wrapper for Binance Futures Testnet API interactions.
    """
    
    TESTNET_BASE_URL = "https://testnet.binancefuture.com"
    
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize Binance Futures Testnet client.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
        """
        self.api_key = api_key
        self.api_secret = api_secret
        
        # Initialize python-binance client with testnet URL
        self.client = Client(api_key, api_secret, testnet=True)
        self.client.API_URL = self.TESTNET_BASE_URL
        
        logger.info("Binance Testnet client initialized")
        
    def _generate_signature(self, params: Dict) -> str:
        """
        Generate HMAC SHA256 signature for API request.
        
        Args:
            params: Request parameters
            
        Returns:
            Signature string
        """
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def test_connection(self) -> bool:
        """
        Test API connection and credentials.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            logger.info("Testing API connection...")
            # Test connection by fetching account info
            url = f"{self.TESTNET_BASE_URL}/fapi/v2/account"
            
            timestamp = int(time.time() * 1000)
            params = {'timestamp': timestamp}
            params['signature'] = self._generate_signature(params)
            
            headers = {'X-MBX-APIKEY': self.api_key}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                logger.info("API connection successful")
                return True
            else:
                logger.error(f"API connection failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False
    
    def get_symbol_info(self, symbol: str) -> Optional[Dict]:
        """
        Get trading rules and symbol information.
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Symbol info dictionary or None if not found
        """
        try:
            logger.debug(f"Fetching symbol info for {symbol}")
            
            url = f"{self.TESTNET_BASE_URL}/fapi/v1/exchangeInfo"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for s in data.get('symbols', []):
                    if s['symbol'] == symbol:
                        logger.debug(f"Symbol info retrieved: {s}")
                        return s
                
                logger.warning(f"Symbol {symbol} not found in exchange info")
                return None
            else:
                logger.error(f"Failed to get exchange info: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching symbol info: {str(e)}")
            return None
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict:
        """
        Place a market order on Binance Futures Testnet.
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY or SELL)
            quantity: Order quantity
            
        Returns:
            Order response dictionary
            
        Raises:
            BinanceAPIException: If API returns an error
            Exception: For other errors
        """
        try:
            logger.info(f"Placing MARKET order: {side} {quantity} {symbol}")
            
            order_params = {
                'symbol': symbol,
                'side': side,
                'type': 'MARKET',
                'quantity': quantity,
                'timestamp': int(time.time() * 1000)
            }
            
            logger.debug(f"Order parameters: {order_params}")
            
            # Use python-binance library
            response = self.client.futures_create_order(**order_params)
            
            logger.info(f"Market order placed successfully. Order ID: {response.get('orderId')}")
            logger.debug(f"Full order response: {response}")
            
            return response
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.status_code} - {e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Binance request error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing market order: {str(e)}")
            raise
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, 
                         price: float, time_in_force: str = 'GTC') -> Dict:
        """
        Place a limit order on Binance Futures Testnet.
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY or SELL)
            quantity: Order quantity
            price: Order price
            time_in_force: Time in force (GTC, IOC, FOK)
            
        Returns:
            Order response dictionary
            
        Raises:
            BinanceAPIException: If API returns an error
            Exception: For other errors
        """
        try:
            logger.info(f"Placing LIMIT order: {side} {quantity} {symbol} @ {price}")
            
            order_params = {
                'symbol': symbol,
                'side': side,
                'type': 'LIMIT',
                'quantity': quantity,
                'price': price,
                'timeInForce': time_in_force,
                'timestamp': int(time.time() * 1000)
            }
            
            logger.debug(f"Order parameters: {order_params}")
            
            # Use python-binance library
            response = self.client.futures_create_order(**order_params)
            
            logger.info(f"Limit order placed successfully. Order ID: {response.get('orderId')}")
            logger.debug(f"Full order response: {response}")
            
            return response
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.status_code} - {e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Binance request error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing limit order: {str(e)}")
            raise
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """
        Get current market price for a symbol.
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Current price or None if error
        """
        try:
            url = f"{self.TESTNET_BASE_URL}/fapi/v1/ticker/price"
            params = {'symbol': symbol}
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                price = float(data['price'])
                logger.debug(f"Current price for {symbol}: {price}")
                return price
            else:
                logger.error(f"Failed to get price: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching current price: {str(e)}")
            return None
