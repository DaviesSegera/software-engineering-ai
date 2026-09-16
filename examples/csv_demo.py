"""Module 2 optional input-boundary example for the supplied CSV.

This narrow loader requires one device, equal intervals and the exact
four-column schema. It does not validate timestamp syntax or completeness.
Those are explicit extensions, not silently assumed capabilities.
"""
import csv
from pathlib import Path
from energy import interval_energy_Wh


def energy_from_csv(path):
    expected = ["device_id", "timestamp_utc", "power_W", "interval_min"]
    with open(path, newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != expected:
            raise ValueError("CSV fields do not match the required schema")
        powers, intervals, devices, timestamps = [], [], set(), set()
        for row_number, row in enumerate(reader, start=2):
            if None in row or any(row.get(key) in (None, "") for key in expected):
                raise ValueError(f"malformed record at row {row_number}")
            identity = (row["device_id"], row["timestamp_utc"])
            if identity in timestamps:
                raise ValueError(f"duplicate timestamp at row {row_number}")
            timestamps.add(identity)
            devices.add(row["device_id"])
            try:
                powers.append(float(row["power_W"]))
                intervals.append(float(row["interval_min"]))
            except ValueError as exc:
                raise ValueError(f"non-numeric value at row {row_number}") from exc
    if not powers or len(devices) != 1 or len(set(intervals)) != 1:
        raise ValueError("require nonempty data for one device and equal intervals")
    return interval_energy_Wh(powers, intervals[0])


if __name__ == "__main__":
    print("Energy from CSV (Wh):", energy_from_csv(Path(__file__).with_name("telemetry.csv")))
