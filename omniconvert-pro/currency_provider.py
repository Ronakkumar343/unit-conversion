from typing import Dict, List, Optional
from dataclasses import dataclass
import datetime

@dataclass
class CurrencyRate:
    code: str
    rate: float  # Base USD
    name: str
    symbol: str

@dataclass
class CurrencyResult:
    from_code: str
    to_code: str
    amount: float
    result: float
    rate: float
    timestamp: str

class CurrencyProvider:
    def __init__(self):
        self.rates: Dict[str, CurrencyRate] = {
            "USD": CurrencyRate("USD", 1.0, "US Dollar", "$"),
            "EUR": CurrencyRate("EUR", 0.92, "Euro", "€"),
            "GBP": CurrencyRate("GBP", 0.79, "British Pound", "£"),
            "JPY": CurrencyRate("JPY", 151.4, "Japanese Yen", "¥"),
            "INR": CurrencyRate("INR", 83.3, "Indian Rupee", "₹"),
            "CAD": CurrencyRate("CAD", 1.35, "Canadian Dollar", "C$")
        }

    def convert(self, amount: float, from_code: str, to_code: str) -> CurrencyResult:
        f = self.rates.get(from_code.upper())
        t = self.rates.get(to_code.upper())
        
        if not f or not t:
            raise ValueError(f"Unsupported currency: {from_code if not f else to_code}")

        # amount / from_rate * to_rate
        in_base = amount / f.rate
        res = in_base * t.rate
        effective_rate = t.rate / f.rate

        return CurrencyResult(
            from_code=from_code.upper(),
            to_code=to_code.upper(),
            amount=amount,
            result=res,
            rate=effective_rate,
            timestamp=datetime.datetime.now().isoformat()
        )

    def get_supported(self) -> List[str]:
        return list(self.rates.keys())
