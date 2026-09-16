# Runnable classroom examples

Use an approved Python 3 installation with the standard library, including sqlite3. No API key, paid account or third-party package is needed for these examples. Open a terminal in this examples folder and use the interpreter command configured for your installation.

## Commands

```text
python first_energy.py
python energy.py
python run_checks.py
python csv_demo.py
python sqlite_demo.py
python retrieval_demo.py
python advice_demo.py
python benchmark_demo.py
```

The first examples return 90 Wh, and the formatter returns Energy: 0.090 kWh. The database is in memory and returns 90 Wh for motor_1. The lexical retrieval example deliberately misses the synonym query thermal blockage. The advice example demonstrates valid output, invalid output and a simulated timeout; every report retains 90 Wh. Benchmark durations are measured locally and will vary.

## What the checks establish

The suite checks independently calculated values, invalid and non-finite inputs, no mutation, useful algebraic relationships, parameter-bound SQL, authorised document lookup, response structure, fallback behaviour and the p95 convention. It explicitly demonstrates that schema acceptance does not establish semantic truth.

The suite does not test an actual language model, enforce a real network timeout, evaluate field sensor accuracy or certify an equipment controller. Provider stubs are labelled as stubs. Use Module 4's live integration preparation steps for a separately configured provider experiment.

## Suggested learning sequence

Modules 1 and 2 use energy.py and test_energy.py. Module 3 reviews changes to format_kWh and the tests. Module 4 uses the database, retrieval and advice examples. Module 5 runs the quality gate and observes fallback events. Module 6 uses authorisation checks and the benchmark. Module 7 reproduces and explains the complete local package.

These files are reference solutions. Preserve a clean copy, work in a separate student folder and attempt practice questions before consulting the answers. All data and manual passages are invented classroom examples.
