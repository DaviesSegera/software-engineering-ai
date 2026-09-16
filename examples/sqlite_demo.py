"""Module 4 local in-memory database; no persistent files are changed."""
import sqlite3
from contextlib import closing
from energy import interval_energy_Wh


def make_database():
    connection = sqlite3.connect(":memory:")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript("""
        CREATE TABLE devices (
            device_id TEXT PRIMARY KEY,
            description TEXT NOT NULL
        );
        CREATE TABLE readings (
            device_id TEXT NOT NULL REFERENCES devices(device_id),
            timestamp_utc TEXT NOT NULL,
            power_W REAL NOT NULL CHECK(power_W >= 0),
            interval_min REAL NOT NULL CHECK(interval_min > 0),
            PRIMARY KEY(device_id, timestamp_utc)
        );
    """)
    connection.execute("INSERT INTO devices VALUES (?, ?)",
                       ("motor_1", "Invented classroom motor"))
    connection.executemany("INSERT INTO readings VALUES (?, ?, ?, ?)", [
        ("motor_1", "2026-09-01T00:00:00Z", 60.0, 30.0),
        ("motor_1", "2026-09-01T00:30:00Z", 120.0, 30.0),
        ("motor_1", "2026-09-01T01:00:00Z", 0.0, 30.0),
    ])
    connection.commit()
    return connection


def read_energy(connection, device_id):
    rows = connection.execute(
        "SELECT power_W, interval_min FROM readings "
        "WHERE device_id = ? ORDER BY timestamp_utc", (device_id,)
    ).fetchall()
    if not rows:
        raise ValueError("no readings for that device")
    durations = {row[1] for row in rows}
    if len(durations) != 1:
        raise ValueError("this example requires equal intervals")
    return interval_energy_Wh([row[0] for row in rows], rows[0][1])


if __name__ == "__main__":
    with closing(make_database()) as connection:
        print("Energy (Wh):", read_energy(connection, "motor_1"))
        try:
            read_energy(connection, "unknown")
        except ValueError as exc:
            print("Expected rejection:", exc)
