from typing import Optional, Dict, Any
from dataclasses import dataclass, replace
from unit_registry import UnitRegistry, UnitDefinition

@dataclass
class ConversionResult:
    value: float
    from_unit: str
    to_unit: str
    quantity: str
    chain: list
    formatted_value: str

class ConverterEngine:
    def __init__(self, registry: UnitRegistry):
        self.registry = registry

    def resolve_unit(self, unit_name: str, country: Optional[str] = None, state: Optional[str] = None) -> UnitDefinition:
        unit_def = self.registry.get_unit(unit_name)
        if not unit_def:
            raise ValueError(f"Unknown unit: {unit_name}")

        # Handle variants
        if unit_def.factor is None and unit_def.country_variants:
            key = country.upper() if country else None
            if state and country:
                state_key = f"{country.upper()}-{state.upper()}"
                if state_key in unit_def.country_variants:
                    key = state_key
            
            if key in unit_def.country_variants:
                return replace(unit_def, factor=unit_def.country_variants[key])
            else:
                variants = ", ".join(unit_def.country_variants.keys())
                raise ValueError(f"Ambiguous unit '{unit_name}'. Specify one of: {variants}")
        
        return unit_def

    def convert(self, value: float, from_unit: str, to_unit: str, 
                country: Optional[str] = None, state: Optional[str] = None,
                precision: int = 4) -> ConversionResult:
        
        from_def = self.resolve_unit(from_unit, country, state)
        to_def = self.resolve_unit(to_unit, country, state)

        if from_def.quantity != to_def.quantity:
            raise ValueError(f"Dimension mismatch: {from_def.quantity} vs {to_def.quantity}")

        # 1. To Base
        base_value = value * from_def.factor + from_def.offset

        # Absolute Zero Protection
        if from_def.quantity == "temperature" and base_value < 0:
            raise ValueError("Temperature cannot be below absolute zero (0K).")

        # 2. From Base
        result_value = (base_value - to_def.offset) / to_def.factor

        # 3. Chain
        base_unit_name = self.registry.get_base_unit(from_def.quantity)
        chain = [
            f"{value} {from_unit}",
            f"→ {round(base_value, precision)} {base_unit_name}",
            f"→ {round(result_value, precision)} {to_unit}"
        ]

        formatted = f"{result_value:,.{precision}f}"
        
        return ConversionResult(
            value=result_value,
            from_unit=from_unit,
            to_unit=to_unit,
            quantity=from_def.quantity,
            chain=chain,
            formatted_value=formatted
        )
