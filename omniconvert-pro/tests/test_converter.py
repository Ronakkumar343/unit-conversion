"""Unit tests for the OmniConvert Pro conversion engine.

Run from the omniconvert-pro folder:

    python -m unittest discover -s tests -v

The tests resolve the unit data file relative to this file, so they
also pass when run from any other working directory.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from unit_registry import UnitRegistry
from converter_engine import ConverterEngine
from currency_provider import CurrencyProvider

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "units.json")


class EngineTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = ConverterEngine(UnitRegistry(DATA_PATH))

    def convert(self, *args, **kwargs):
        return self.engine.convert(*args, **kwargs).value


class LengthTests(EngineTestCase):
    def test_kilometer_to_meter(self):
        self.assertEqual(self.convert(1, "kilometer", "meter"), 1000.0)

    def test_mile_to_kilometer(self):
        self.assertAlmostEqual(self.convert(1, "mile", "kilometer"), 1.609344)

    def test_foot_to_inch(self):
        self.assertAlmostEqual(self.convert(1, "foot", "inch"), 12.0)

    def test_aliases_resolve(self):
        self.assertEqual(self.convert(1, "km", "m"), 1000.0)
        self.assertAlmostEqual(self.convert(1, "ft", "inch"), 12.0)


class MassTests(EngineTestCase):
    def test_kilogram_to_gram(self):
        self.assertEqual(self.convert(1, "kilogram", "gram"), 1000.0)

    def test_kilogram_to_pound(self):
        self.assertAlmostEqual(self.convert(1, "kilogram", "pound"), 2.2046226, places=6)


class TemperatureTests(EngineTestCase):
    def test_celsius_to_fahrenheit_boiling(self):
        self.assertAlmostEqual(self.convert(100, "celsius", "fahrenheit"), 212.0)

    def test_celsius_to_fahrenheit_crossover(self):
        self.assertAlmostEqual(self.convert(-40, "celsius", "fahrenheit"), -40.0)

    def test_fahrenheit_to_celsius_freezing(self):
        self.assertAlmostEqual(self.convert(32, "fahrenheit", "celsius"), 0.0)

    def test_celsius_to_kelvin(self):
        self.assertAlmostEqual(self.convert(0, "celsius", "kelvin"), 273.15)

    def test_below_absolute_zero_rejected(self):
        with self.assertRaises(ValueError):
            self.convert(-300, "celsius", "kelvin")


class VolumeTests(EngineTestCase):
    """Regression tests: gallon used to be registered under *length*,
    so gallon -> liter failed with a dimension mismatch and
    gallon -> meter silently returned the litre factor as metres."""

    def test_us_gallon_to_liter(self):
        self.assertAlmostEqual(
            self.convert(1, "gallon", "liter", country="US"), 3.785411784
        )

    def test_uk_gallon_to_liter(self):
        self.assertAlmostEqual(
            self.convert(1, "gallon", "liter", country="UK"), 4.54609
        )

    def test_gallon_is_not_a_length(self):
        with self.assertRaises(ValueError):
            self.convert(1, "gallon", "meter", country="US")

    def test_gallon_without_country_is_ambiguous(self):
        with self.assertRaises(ValueError):
            self.convert(1, "gallon", "liter")

    def test_liter_to_milliliter(self):
        self.assertEqual(self.convert(1, "liter", "milliliter"), 1000.0)

    def test_cubic_meter_to_liter(self):
        self.assertEqual(self.convert(1, "cubic_meter", "liter"), 1000.0)


class AreaTests(EngineTestCase):
    def test_bigha_uttar_pradesh(self):
        self.assertAlmostEqual(
            self.convert(1, "bigha", "square_meter", country="IN", state="UP"),
            2529.3,
        )

    def test_bigha_rajasthan(self):
        self.assertAlmostEqual(
            self.convert(1, "bigha", "square_meter", country="IN", state="RJ"),
            1618.7,
        )

    def test_acre_to_square_meter(self):
        self.assertAlmostEqual(self.convert(1, "acre", "square_meter"), 4046.856)


class SpeedTests(EngineTestCase):
    def test_mph_to_kmh(self):
        self.assertAlmostEqual(
            self.convert(60, "mile_per_hour", "kilometer_per_hour"), 96.56064
        )


class ErrorTests(EngineTestCase):
    def test_unknown_unit(self):
        with self.assertRaises(ValueError):
            self.convert(1, "furlong", "meter")

    def test_dimension_mismatch(self):
        with self.assertRaises(ValueError):
            self.convert(1, "kilogram", "meter")


class CurrencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.currency = CurrencyProvider()

    def test_usd_to_eur(self):
        self.assertAlmostEqual(self.currency.convert(100, "USD", "EUR").result, 92.0)

    def test_round_trip(self):
        eur = self.currency.convert(100, "USD", "EUR").result
        self.assertAlmostEqual(self.currency.convert(eur, "EUR", "USD").result, 100.0)

    def test_unknown_currency(self):
        with self.assertRaises(ValueError):
            self.currency.convert(1, "USD", "XXX")

    def test_supported_currencies(self):
        self.assertIn("USD", self.currency.get_supported())


if __name__ == "__main__":
    unittest.main()
