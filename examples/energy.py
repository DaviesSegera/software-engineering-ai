"""Reference interval-energy implementation for Modules 1 and 2.

Each reading is a non-negative interval-average power in watts.
All intervals have the same strictly positive duration in minutes.
The function accepts a nonempty list of built-in int/float values,
rejects booleans and non-finite values, and never mutates the input.
"""

import math


def finite_number(value, label):
    if type(value) not in (int, float):
        raise ValueError(f"{label} must be an int or float, not a boolean")
    try:
        number = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"{label} must fit the finite numeric range") from exc
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    return number


def interval_energy_Wh(powers_W, interval_min):
    """Return finite energy in Wh; raise ValueError for invalid input.

    This readable implementation creates a validated copy: O(n) time
    and O(n) additional memory. It does not model instantaneous samples,
    signed export power, variable intervals or measurement uncertainty.
    """
    if not isinstance(powers_W, list) or not powers_W:
        raise ValueError("powers_W must be a nonempty list")
    duration = finite_number(interval_min, "interval_min")
    if duration <= 0:
        raise ValueError("interval_min must be positive")
    validated = []
    for index, raw in enumerate(powers_W):
        value = finite_number(raw, f"power at index {index}")
        if value < 0:
            raise ValueError("negative power is outside this model")
        validated.append(value)
    try:
        result = math.fsum(validated) * (duration / 60.0)
    except OverflowError as exc:
        raise ValueError("calculation exceeds the finite numeric range") from exc
    if not math.isfinite(result):
        raise ValueError("calculation exceeds the finite numeric range")
    return result


def format_kWh(energy_Wh):
    """Format a finite non-negative Wh value in kWh to three decimals."""
    value = finite_number(energy_Wh, "energy_Wh")
    if value < 0:
        raise ValueError("energy_Wh must be non-negative")
    return f"Energy: {value / 1000.0:.3f} kWh"


if __name__ == "__main__":
    energy = interval_energy_Wh([60.0, 120.0, 0.0], 30.0)
    print(f"Energy: {energy:.2f} Wh")
    print(format_kWh(energy))
