# OmniConvert Pro

A unit and currency converter built in Python — a modular converter engine, a structured unit registry, and a currency provider for exchange-rate conversions.

## What it does

- Converts everyday units across categories (length, mass, temperature, and more)
- Converts currencies using exchange rates from a dedicated provider module
- Keeps unit definitions in a registry, so adding a new unit or category doesn't touch the conversion logic

## Project layout

The application lives in the [`omniconvert-pro/`](omniconvert-pro/) folder:

| File | Role |
|---|---|
| `app.py` | Application entry point |
| `converter_engine.py` | Core conversion logic |
| `unit_registry.py` | Unit and category definitions |
| `currency_provider.py` | Currency / exchange-rate handling |
| `data/` | Supporting data files |

See the README inside `omniconvert-pro/` for setup details.

## Tech

Python · modular engine design (engine / registry / provider separation)

## Status

Working project — part of my build-in-public portfolio as a Class 9 developer from Mithi, Pakistan, working toward Computer Science at MIT.

— **Ronak Kumar** · [GitHub](https://github.com/Ronakkumar343) · [AI WALA on YouTube](https://www.youtube.com/@AIWalaHQ)
