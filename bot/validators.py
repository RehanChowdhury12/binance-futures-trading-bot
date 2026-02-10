from typing import Optional
from decimal import Decimal, InvalidOperation


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_symbol(symbol: str) -> str:
    """
    Validate trading symbol format.
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        
    Returns:
        Uppercase symbol
        
    Raises:
        ValidationError: If symbol is invalid
    """
    if not symbol:
        raise ValidationError("Symbol cannot be empty")
    
    symbol = symbol.upper().strip()
    
    if not symbol.endswith('USDT'):
        raise ValidationError("Symbol must end with 'USDT' for USDT-M futures")
    
    if len(symbol) < 5:
        raise ValidationError("Symbol is too short")
    
    return symbol


def validate_side(side: str) -> str:
    """
    Validate order side.
    
    Args:
        side: Order side (BUY or SELL)
        
    Returns:
        Uppercase side
        
    Raises:
        ValidationError: If side is invalid
    """
    side = side.upper().strip()
    
    if side not in ['BUY', 'SELL']:
        raise ValidationError("Side must be 'BUY' or 'SELL'")
    
    return side


def validate_order_type(order_type: str) -> str:
    """
    Validate order type.
    
    Args:
        order_type: Type of order (MARKET or LIMIT)
        
    Returns:
        Uppercase order type
        
    Raises:
        ValidationError: If order type is invalid
    """
    order_type = order_type.upper().strip()
    
    if order_type not in ['MARKET', 'LIMIT']:
        raise ValidationError("Order type must be 'MARKET' or 'LIMIT'")
    
    return order_type


def validate_quantity(quantity: str) -> float:
    """
    Validate order quantity.
    
    Args:
        quantity: Order quantity
        
    Returns:
        Validated quantity as float
        
    Raises:
        ValidationError: If quantity is invalid
    """
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError("Quantity must be a valid number")
    
    if qty <= 0:
        raise ValidationError("Quantity must be greater than 0")
    
    return qty


def validate_price(price: Optional[str]) -> Optional[float]:
    """
    Validate order price.
    
    Args:
        price: Order price (required for LIMIT orders)
        
    Returns:
        Validated price as float or None
        
    Raises:
        ValidationError: If price is invalid
    """
    if price is None or price == "":
        return None
    
    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValidationError("Price must be a valid number")
    
    if p <= 0:
        raise ValidationError("Price must be greater than 0")
    
    return p


def validate_order_params(symbol: str, side: str, order_type: str, 
                         quantity: str, price: Optional[str] = None) -> dict:
    """
    Validate all order parameters.
    
    Args:
        symbol: Trading pair symbol
        side: Order side (BUY/SELL)
        order_type: Order type (MARKET/LIMIT)
        quantity: Order quantity
        price: Order price (required for LIMIT)
        
    Returns:
        Dictionary of validated parameters
        
    Raises:
        ValidationError: If any parameter is invalid
    """
    validated = {
        'symbol': validate_symbol(symbol),
        'side': validate_side(side),
        'type': validate_order_type(order_type),
        'quantity': validate_quantity(quantity)
    }
    
    if validated['type'] == 'LIMIT':
        if price is None or price == "":
            raise ValidationError("Price is required for LIMIT orders")
        validated['price'] = validate_price(price)
    elif price is not None and price != "":
        raise ValidationError("Price should not be specified for MARKET orders")
    
    return validated
