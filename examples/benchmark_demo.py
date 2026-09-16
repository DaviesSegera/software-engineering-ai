"""Module 6: actual local timings; synthetic data; no external provider."""
import math
import statistics
from time import perf_counter
from energy import interval_energy_Wh


def nearest_rank(values, fraction):
    if not values or not 0 < fraction <= 1:
        raise ValueError("nonempty values and fraction in (0, 1] required")
    return sorted(values)[math.ceil(fraction * len(values)) - 1]


def measure(repeats=40):
    if type(repeats) is not int or repeats < 20:
        raise ValueError("use at least 20 repeats in this demonstration")
    powers = [60.0, 120.0, 0.0] * 1000
    expected = 90000.0
    # Warm up outside the measured runs; report this choice.
    if not math.isclose(interval_energy_Wh(powers, 30), expected):
        raise RuntimeError("baseline correctness check failed")
    observations = []
    for _ in range(repeats):
        start = perf_counter()
        result = interval_energy_Wh(powers, 30)
        observations.append((perf_counter() - start) * 1000)
        if not math.isclose(result, expected):
            raise RuntimeError("measured result failed correctness check")
    return observations


if __name__ == "__main__":
    values = measure()
    print("Local deterministic calculation, 3000 readings, one warm-up run")
    print("All observed durations in ms:", ", ".join(f"{x:.4f}" for x in values))
    print(f"Median: {statistics.median(values):.4f} ms")
    print(f"Nearest-rank p95: {nearest_rank(values, 0.95):.4f} ms")
    print("These observations describe this machine and run only.")
