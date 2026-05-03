import json
import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

@dataclass
class UnitDefinition:
    name: str
    quantity: str
    factor: Optional[float]
    offset: float = 0.0
    aliases: List[str] = field(default_factory=list)
    systems: List[str] = field(default_factory=list)
    countries: List[str] = field(default_factory=list)
    country_variants: Dict[str, float] = field(default_factory=dict)
    note: str = ""

class UnitRegistry:
    def __init__(self, data_path: str = "data/units.json"):
        self.units_by_name: Dict[str, UnitDefinition] = {}
        self.units_by_quantity: Dict[str, List[str]] = {}
        self.base_units: Dict[str, str] = {}
        self.load_data(data_path)

    def load_data(self, path: str):
        if not os.path.exists(path):
            return

        with open(path, "r") as f:
            data = json.load(f)

        for quantity_name, quantity_data in data.items():
            self.base_units[quantity_name] = quantity_data["base_unit"]
            self.units_by_quantity[quantity_name] = []
            
            for unit_name, unit_data in quantity_data["units"].items():
                unit_def = UnitDefinition(
                    name=unit_name,
                    quantity=quantity_name,
                    factor=unit_data.get("factor"),
                    offset=unit_data.get("offset", 0.0),
                    aliases=unit_data.get("aliases", []),
                    systems=unit_data.get("systems", []),
                    countries=unit_data.get("countries", []),
                    country_variants=unit_data.get("country_variants", {}),
                    note=unit_data.get("note", "")
                )
                
                # Index by name and aliases
                self.units_by_name[unit_name.lower()] = unit_def
                for alias in unit_def.aliases:
                    self.units_by_name[alias.lower()] = unit_def
                
                self.units_by_quantity[quantity_name].append(unit_name)

    def get_unit(self, name: str) -> Optional[UnitDefinition]:
        return self.units_by_name.get(name.lower())

    def get_quantities(self) -> List[str]:
        return list(self.units_by_quantity.keys())

    def get_units_for_quantity(self, quantity: str) -> List[str]:
        return self.units_by_quantity.get(quantity, [])

    def get_base_unit(self, quantity: str) -> str:
        return self.base_units.get(quantity, "unknown")
