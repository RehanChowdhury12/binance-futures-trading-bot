# Binance Futures Testnet Trading Bot

A Python trading bot for placing orders on Binance Futures Testnet (USDT-M). This application provides a clean, well-structured CLI interface with comprehensive logging and error handling.

## Features

✅ **Order Types**: Support for MARKET and LIMIT orders  
✅ **Both Sides**: BUY and SELL operations  
✅ **Input Validation**: Comprehensive validation of all parameters  
✅ **Error Handling**: Robust exception handling for API and network errors  
✅ **Logging**: Detailed logging to files with timestamps  
✅ **Clean Architecture**: Separated concerns (client, orders, validators, CLI)  
✅ **User-Friendly CLI**: Interactive command-line interface with colored output  
✅ **API Testing**: Built-in connection testing functionality  

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py          # Package initialization
│   ├── client.py            # Binance API client wrapper
│   ├── orders.py            # Order placement logic
│   ├── validators.py        # Input validation utilities
│   └── logging_config.py    # Logging configuration
├── cli.py                   # CLI entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Prerequisites

- Python 3.7 or higher
- Binance Futures Testnet account ([Register here](https://testnet.binancefuture.com/))
- API Key and Secret from Binance Futures Testnet

## Setup Instructions

### 1. Clone or Download the Repository

```bash
git clone <your-repo-url>
cd trading_bot
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Credentials

#### Option A: Using Environment Variables (Recommended)

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```
BINANCE_TESTNET_API_KEY=your_actual_api_key
BINANCE_TESTNET_API_SECRET=your_actual_api_secret
```

Load environment variables:

```bash
# Linux/Mac
export $(cat .env | xargs)

# Or add to your shell profile (~/.bashrc, ~/.zshrc):
export BINANCE_TESTNET_API_KEY='your_api_key'
export BINANCE_TESTNET_API_SECRET='your_api_secret'
```

#### Option B: Direct Environment Variables

```bash
export BINANCE_TESTNET_API_KEY='your_api_key'
export BINANCE_TESTNET_API_SECRET='your_api_secret'
```

### 5. Test Your Connection

```bash
python cli.py test
```

You should see:
```
✓ API connection successful!
✓ Your API credentials are valid.
```

## Usage Examples

### Basic Commands

The CLI provides several commands. Use `--help` to see all options:

```bash
python cli.py --help
```

### 1. Test API Connection

```bash
python cli.py test
```

### 2. Get Current Price

```bash
# Default symbol (BTCUSDT)
python cli.py price

# Specific symbol
python cli.py price -s ETHUSDT
```

### 3. Place a Market Order

**Buy Order:**
```bash
python cli.py order -s BTCUSDT -d BUY -t MARKET -q 0.001
```

**Sell Order:**
```bash
python cli.py order -s ETHUSDT -d SELL -t MARKET -q 0.01
```

### 4. Place a Limit Order

**Buy Limit:**
```bash
python cli.py order -s BTCUSDT -d BUY -t LIMIT -q 0.001 -p 50000.00
```

**Sell Limit:**
```bash
python cli.py order -s ETHUSDT -d SELL -t LIMIT -q 0.01 -p 3000.50
```

### Command-Line Options

```
Options:
  -s, --symbol TEXT       Trading pair symbol (e.g., BTCUSDT) [required]
  -d, --side [BUY|SELL]  Order side: BUY or SELL [required]
  -t, --type [MARKET|LIMIT]  Order type: MARKET or LIMIT [required]
  -q, --quantity TEXT     Order quantity [required]
  -p, --price TEXT        Order price (required for LIMIT orders)
  --help                  Show this message and exit
```

## Example Output

### Market Order Success

```
Order Request Summary:
  Symbol:      BTCUSDT
  Side:        BUY
  Type:        MARKET
  Quantity:    0.001

Do you want to proceed with this order? [y/N]: y

Placing order...

======================================================================
ORDER PLACED SUCCESSFULLY
======================================================================
Order ID:        12345678
Symbol:          BTCUSDT
Side:            BUY
Type:            MARKET
Status:          FILLED
Quantity:        0.001
Executed Qty:    0.001
======================================================================

✓ Order placed successfully!
Check the logs directory for detailed information.
```

### Limit Order Success

```
Order Request Summary:
  Symbol:      ETHUSDT
  Side:        SELL
  Type:        LIMIT
  Quantity:    0.01
  Price:       3000.50

Do you want to proceed with this order? [y/N]: y

Placing order...

======================================================================
ORDER PLACED SUCCESSFULLY
======================================================================
Order ID:        87654321
Symbol:          ETHUSDT
Side:            SELL
Type:            LIMIT
Status:          NEW
Quantity:        0.01
Price:           3000.50
Executed Qty:    0
======================================================================

✓ Order placed successfully!
Check the logs directory for detailed information.
```

## Logging

All operations are logged to files in the `logs/` directory:

- Filename format: `trading_bot_YYYYMMDD_HHMMSS.log`
- Includes: API requests, responses, errors, validation details
- Log levels: DEBUG (file) and INFO (console)

Example log location:
```
logs/trading_bot_20240215_143022.log
```

## Error Handling

The bot handles various error scenarios:

### Validation Errors
- Invalid symbol format
- Missing price for LIMIT orders
- Negative or zero quantities
- Invalid order types or sides

### API Errors
- Invalid API credentials
- Insufficient balance
- Symbol not found
- Network connectivity issues

### Example Error Messages

```
Validation Error: Price is required for LIMIT orders
```

```
Error: Symbol INVALID not found or not tradable
```

```
Binance API error: -2015 - Invalid API-key, IP, or permissions for action
```

## Assumptions

1. **Testnet Environment**: This bot is designed exclusively for Binance Futures Testnet (https://testnet.binancefuture.com)
2. **USDT-M Futures**: All symbols must be USDT-margined futures (end with 'USDT')
3. **Python Version**: Requires Python 3.7+
4. **Dependencies**: Uses `python-binance` library for API interactions
5. **Time in Force**: LIMIT orders default to GTC (Good-Till-Cancelled)
6. **Decimal Precision**: Uses Binance's default precision for each symbol

## Troubleshooting

### "API credentials not found"
Make sure you've exported the environment variables:
```bash
export BINANCE_TESTNET_API_KEY='your_key'
export BINANCE_TESTNET_API_SECRET='your_secret'
```

### "API connection failed"
1. Verify your API credentials are correct
2. Check that API key has futures trading permissions enabled
3. Ensure you're using Testnet credentials (not production)
4. Check your internet connection

### "Symbol not found"
- Ensure the symbol ends with 'USDT' (e.g., BTCUSDT, ETHUSDT)
- Verify the symbol exists on Binance Futures Testnet
- Check spelling and capitalization

### Import Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Security Notes

⚠️ **Never commit your `.env` file or API credentials to version control**

- The `.gitignore` file is configured to exclude `.env` and `logs/`
- Use environment variables for credentials
- This is a TESTNET bot - use testnet credentials only
- Do not use production API keys with this application

## Advanced Usage

### Programmatic Usage

You can also use the bot modules programmatically:

```python
from bot import BinanceTestnetClient, OrderManager, setup_logging

# Setup
logger = setup_logging()
client = BinanceTestnetClient(api_key='your_key', api_secret='your_secret')
order_manager = OrderManager(client)

# Place order
response = order_manager.place_order(
    symbol='BTCUSDT',
    side='BUY',
    order_type='MARKET',
    quantity='0.001'
)
```

## Testing Checklist

- [ ] API connection test passes
- [ ] Market BUY order executes successfully
- [ ] Market SELL order executes successfully
- [ ] Limit BUY order places successfully
- [ ] Limit SELL order places successfully
- [ ] Validation catches invalid inputs
- [ ] Logs are created with correct information
- [ ] Error messages are clear and helpful

## License

MIT License - Free to use for educational and personal purposes.

## Contributing

This is an application task project. For actual contributions to improve the codebase, please follow standard GitHub workflow:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues or questions:
- Check the logs in `logs/` directory for detailed error information
- Review the Binance Futures Testnet documentation
- Ensure you're using valid testnet credentials

**Happy Trading! 🚀**

*Note: This bot is for educational purposes and testnet use only. Never use with real funds without proper testing and risk management.*
