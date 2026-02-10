#!/usr/bin/env python3
import os
import sys
import click
from colorama import init, Fore, Style

from bot import BinanceTestnetClient, OrderManager, ValidationError, setup_logging

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Setup logging
logger = setup_logging()


def get_api_credentials():
    """
    Get API credentials from environment variables.
    
    Returns:
        Tuple of (api_key, api_secret)
        
    Raises:
        SystemExit: If credentials are not found
    """
    api_key = os.environ.get('BINANCE_TESTNET_API_KEY')
    api_secret = os.environ.get('BINANCE_TESTNET_API_SECRET')
    
    if not api_key or not api_secret:
        print(f"{Fore.RED}Error: API credentials not found in environment variables.")
        print(f"{Fore.YELLOW}Please set the following environment variables:")
        print("  - BINANCE_TESTNET_API_KEY")
        print("  - BINANCE_TESTNET_API_SECRET")
        print(f"\nExample:{Style.RESET_ALL}")
        print("  export BINANCE_TESTNET_API_KEY='your_api_key'")
        print("  export BINANCE_TESTNET_API_SECRET='your_api_secret'")
        sys.exit(1)
    
    return api_key, api_secret


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    Binance Futures Testnet Trading Bot
    
    A command-line tool for placing orders on Binance Futures Testnet (USDT-M).
    """
    pass


@cli.command()
@click.option('--symbol', '-s', required=True, help='Trading pair symbol (e.g., BTCUSDT)')
@click.option('--side', '-d', required=True, type=click.Choice(['BUY', 'SELL'], case_sensitive=False), 
              help='Order side: BUY or SELL')
@click.option('--type', '-t', 'order_type', required=True, 
              type=click.Choice(['MARKET', 'LIMIT'], case_sensitive=False),
              help='Order type: MARKET or LIMIT')
@click.option('--quantity', '-q', required=True, help='Order quantity')
@click.option('--price', '-p', default=None, help='Order price (required for LIMIT orders)')
def order(symbol, side, order_type, quantity, price):
    """
    Place an order on Binance Futures Testnet.
    
    Examples:
    
      Place a market buy order:
        python cli.py order -s BTCUSDT -d BUY -t MARKET -q 0.001
    
      Place a limit sell order:
        python cli.py order -s ETHUSDT -d SELL -t LIMIT -q 0.01 -p 2500.50
    """
    try:
        # Get API credentials
        api_key, api_secret = get_api_credentials()
        
        # Initialize client
        print(f"{Fore.CYAN}Initializing Binance Testnet client...{Style.RESET_ALL}")
        client = BinanceTestnetClient(api_key, api_secret)
        
        # Test connection
        if not client.test_connection():
            print(f"{Fore.RED}Failed to connect to Binance Testnet API.")
            print("Please check your API credentials and network connection.")
            sys.exit(1)
        
        print(f"{Fore.GREEN}✓ Connected to Binance Futures Testnet{Style.RESET_ALL}\n")
        
        # Initialize order manager
        order_manager = OrderManager(client)
        
        # Print order request summary
        print(f"{Fore.CYAN}Order Request Summary:{Style.RESET_ALL}")
        print(f"  Symbol:      {symbol.upper()}")
        print(f"  Side:        {side.upper()}")
        print(f"  Type:        {order_type.upper()}")
        print(f"  Quantity:    {quantity}")
        if price:
            print(f"  Price:       {price}")
        print()
        
        # Confirm order
        if not click.confirm(f"{Fore.YELLOW}Do you want to proceed with this order?{Style.RESET_ALL}"):
            print(f"{Fore.YELLOW}Order cancelled.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Placing order...{Style.RESET_ALL}\n")
        
        # Place order
        response = order_manager.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        
        # Print success message
        order_manager.print_order_summary(response)
        print(f"{Fore.GREEN}✓ Order placed successfully!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Check the logs directory for detailed information.{Style.RESET_ALL}\n")
        
    except ValidationError as e:
        print(f"\n{Fore.RED}Validation Error: {str(e)}{Style.RESET_ALL}")
        logger.error(f"Validation error: {str(e)}")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        logger.error(f"Error placing order: {str(e)}", exc_info=True)
        sys.exit(1)


@cli.command()
def test():
    """
    Test API connection and credentials.
    """
    try:
        # Get API credentials
        api_key, api_secret = get_api_credentials()
        
        # Initialize client
        print(f"{Fore.CYAN}Testing Binance Testnet connection...{Style.RESET_ALL}\n")
        client = BinanceTestnetClient(api_key, api_secret)
        
        # Test connection
        if client.test_connection():
            print(f"{Fore.GREEN}✓ API connection successful!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✓ Your API credentials are valid.{Style.RESET_ALL}\n")
            
            # Try to get current price as additional test
            print(f"{Fore.CYAN}Fetching current BTC price...{Style.RESET_ALL}")
            price = client.get_current_price('BTCUSDT')
            if price:
                print(f"{Fore.GREEN}✓ Current BTC price: ${price:,.2f}{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}✗ API connection failed.{Style.RESET_ALL}")
            print("Please check your API credentials and network connection.\n")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        logger.error(f"Error testing connection: {str(e)}", exc_info=True)
        sys.exit(1)


@cli.command()
@click.option('--symbol', '-s', default='BTCUSDT', help='Trading pair symbol (default: BTCUSDT)')
def price(symbol):
    """
    Get current market price for a symbol.
    """
    try:
        # Get API credentials
        api_key, api_secret = get_api_credentials()
        
        # Initialize client
        client = BinanceTestnetClient(api_key, api_secret)
        
        # Get price
        print(f"{Fore.CYAN}Fetching current price for {symbol.upper()}...{Style.RESET_ALL}\n")
        current_price = client.get_current_price(symbol.upper())
        
        if current_price:
            print(f"{Fore.GREEN}Current {symbol.upper()} Price: ${current_price:,.2f}{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}Failed to fetch price for {symbol.upper()}{Style.RESET_ALL}\n")
            
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        logger.error(f"Error fetching price: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
