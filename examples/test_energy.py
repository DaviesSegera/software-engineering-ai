"""Independent examples and contract checks; run with unittest."""
import unittest
from energy import interval_energy_Wh, format_kWh


class EnergyTests(unittest.TestCase):
    def test_hand_calculated_cases(self):
        cases = [([60, 120, 0], 30, 90), ([100, 200], 15, 75),
                 ([30, 90], 20, 40), ([0], 10, 0)]
        for powers, duration, expected in cases:
            with self.subTest(powers=powers, duration=duration):
                self.assertAlmostEqual(interval_energy_Wh(powers, duration), expected)

    def test_invalid_readings(self):
        for values in ([], [-1], [True], [None], ["60"],
                       [float("nan")], [float("inf")], [10**400]):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    interval_energy_Wh(values, 30)

    def test_invalid_container(self):
        for values in (None, "60", 60, (60,)):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    interval_energy_Wh(values, 30)

    def test_invalid_duration(self):
        for value in (0, -1, True, None, "30", float("inf"), float("nan")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    interval_energy_Wh([60], value)

    def test_no_mutation(self):
        original = [120, 0, 60]
        interval_energy_Wh(original, 30)
        self.assertEqual(original, [120, 0, 60])

    def test_scaling_and_concatenation(self):
        a, b = [10, 20], [30, 40]
        base = interval_energy_Wh(a, 15)
        self.assertAlmostEqual(interval_energy_Wh([2*x for x in a], 15), 2*base)
        self.assertAlmostEqual(interval_energy_Wh(a+b, 15),
                               base + interval_energy_Wh(b, 15))

    def test_overflow_rejected(self):
        with self.assertRaises(ValueError):
            interval_energy_Wh([1e308, 1e308], 60)

    def test_format(self):
        self.assertEqual(format_kWh(90), "Energy: 0.090 kWh")
        self.assertEqual(format_kWh(0), "Energy: 0.000 kWh")
        for value in (-1, True, float("nan")):
            with self.assertRaises(ValueError):
                format_kWh(value)


if __name__ == "__main__":
    unittest.main(verbosity=2)
