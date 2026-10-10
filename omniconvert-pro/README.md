# OmniConvert Pro

A unit and currency converter written in Python with a Streamlit UI.
Unit definitions live in a JSON registry, conversion logic in a small
engine module, and currency conversion in its own provider module —
adding a unit means editing data, not code.

## Run locally

**Prerequisites:** Python 3

1. Install Streamlit:
   `pip install streamlit`
2. Run the app from this folder:
   `streamlit run app.py`

## Use the engine without the UI

```python
from unit_registry import UnitRegistry
from converter_engine import ConverterEngine

engine = ConverterEngine(UnitRegistry("data/units.json"))
print(engine.convert(1, "mile", "kilometer").value)        # 1.609344
print(engine.convert(1, "gallon", "liter", country="US").value)  # 3.785411784
```

Units whose size depends on the country (gallon: US vs UK; bigha:
Indian state / Pakistan) need a `country` (and where relevant a
`state`) argument — without one the engine raises an error instead of
guessing.

## Tests

```bash
python -m unittest discover -s tests -v
```

The suite covers length, mass, temperature (including the
below-absolute-zero guard), volume, area variants, speed, error
cases, and currency conversion.

## Notes

- Currency rates in `currency_provider.py` are a small built-in
  snapshot (USD, EUR, GBP, JPY, INR, CAD) — they are **not** live
  market rates.
- Temperature conversions are checked against absolute zero (0 K).
