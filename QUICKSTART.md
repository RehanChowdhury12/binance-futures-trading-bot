# Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Step 1: Get Testnet Credentials

1. Go to https://testnet.binancefuture.com
2. Register or log in
3. Navigate to API Management
4. Create a new API key
5. Save your API Key and Secret Key

### Step 2: Install and Configure

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (replace with your actual keys)
export BINANCE_TESTNET_API_KEY='your_api_key_here'
export BINANCE_TESTNET_API_SECRET='your_secret_key_here'
```

### Step 3: Test Connection

```bash
python cli.py test
```

You should see:
```
✓ API connection successful!
✓ Your API credentials are valid.
✓ Current BTC price: $51,234.50
```

### Step 4: Place Your First Order

#### Market Order (executes immediately):
```bash
python cli.py order -s BTCUSDT -d BUY -t MARKET -q 0.001
```

#### Limit Order (waits for target price):
```bash
python cli.py order -s ETHUSDT -d SELL -t LIMIT -q 0.01 -p 3000.50
```

## 📝 Common Commands

```bash
# Check current price
python cli.py price -s BTCUSDT

# Buy BTC at market price
python cli.py order -s BTCUSDT -d BUY -t MARKET -q 0.001

# Sell ETH with limit order
python cli.py order -s ETHUSDT -d SELL -t LIMIT -q 0.01 -p 3000

# Get help
python cli.py --help
python cli.py order --help
```

## ⚠️ Important Notes

- **Use TESTNET credentials only** - Never use production API keys
- All symbols must end with "USDT" (e.g., BTCUSDT, ETHUSDT)
- LIMIT orders require a price parameter
- MARKET orders execute at current market price
- Check `logs/` directory for detailed execution logs

## 🐛 Troubleshooting

**"API credentials not found"**
- Make sure you've exported the environment variables
- Check for typos in variable names

**"Symbol not found"**
- Ensure symbol ends with 'USDT'
- Verify symbol exists on Binance Futures

**"Invalid API-key"**
- Verify you're using TESTNET credentials
- Check that API key has futures trading permissions enabled

## 📚 Learn More

Read the full [README.md](README.md) for:
- Detailed setup instructions
- Advanced usage examples
- Error handling guide
- Programmatic usage
- Security best practices
