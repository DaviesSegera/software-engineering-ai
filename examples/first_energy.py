"""Module 1 fixed-input demonstration, not a general validator."""
powers_W = [60.0, 120.0, 0.0]
interval_min = 30.0
energy_Wh = sum(powers_W) * interval_min / 60.0
print("Energy (Wh):", energy_Wh)
