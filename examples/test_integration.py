import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from csv_demo import energy_from_csv
from contextlib import closing
from advice_demo import make_report, good_stub, invalid_stub, timeout_stub, validate_response
from retrieval_demo import retrieve, read_approved_passage
from sqlite_demo import make_database, read_energy
from benchmark_demo import nearest_rank


class IntegrationTests(unittest.TestCase):
    def test_csv_and_rejection(self):
        sample = Path(__file__).with_name("telemetry.csv")
        self.assertEqual(energy_from_csv(sample), 90.0)
        with TemporaryDirectory() as folder:
            invalid = Path(folder) / "bad.csv"
            invalid.write_text(sample.read_text().replace(
                "00:30:00Z,120,30", "00:30:00Z,unknown,30"), encoding="utf-8")
            with self.assertRaises(ValueError):
                energy_from_csv(invalid)

    def test_sqlite_calculation(self):
        with closing(make_database()) as connection:
            self.assertEqual(read_energy(connection, "motor_1"), 90.0)
            with self.assertRaises(ValueError):
                read_energy(connection, "unknown")

    def test_query_value_is_not_sql(self):
        with closing(make_database()) as connection:
            with self.assertRaises(ValueError):
                read_energy(connection, "' OR 1=1 --")
            self.assertEqual(read_energy(connection, "motor_1"), 90.0)

    def test_retrieval_and_miss(self):
        self.assertEqual(retrieve("motor overheating")[0][1], "manual_motor_v1_p2")
        self.assertEqual(retrieve("thermal blockage"), [])

    def test_tool_authorisation(self):
        allowed = {"manual_motor_v1_p2"}
        self.assertIn("ventilation", read_approved_passage("manual_motor_v1_p2", allowed))
        with self.assertRaises(PermissionError):
            read_approved_passage("private_file", allowed)

    def test_valid_advice(self):
        result = make_report(good_stub)
        self.assertEqual(result["energy_Wh"], 90.0)
        self.assertEqual(result["advice"]["status"], "advice")

    def test_failure_preserves_energy(self):
        for provider, event in [(invalid_stub, "advice_invalid_response"),
                                (timeout_stub, "advice_timeout")]:
            with self.subTest(provider=provider.__name__):
                result = make_report(provider)
                self.assertEqual(result["energy_Wh"], 90.0)
                self.assertEqual(result["advice"]["status"], "unavailable")
                self.assertEqual(result["event"], event)

    def test_unknown_source_rejected(self):
        raw = json.dumps({"status": "advice", "summary": "A claim",
                          "source_ids": ["private_file"]})
        with self.assertRaises(ValueError):
            validate_response(raw, {"manual_motor_v1_p2"})

    def test_malformed_and_wrong_types(self):
        for raw in ("not json", "[]", '{"status": NaN}', "x" * 4001,
                    '{"status":"advice","summary":3,"source_ids":[]}'):
            with self.subTest(raw=raw[:40]):
                with self.assertRaises(ValueError):
                    validate_response(raw, set())

    def test_schema_does_not_establish_truth(self):
        raw = json.dumps({"status": "advice", "summary": "A false claim can fit a schema.",
                          "source_ids": ["manual_motor_v1_p2"]})
        # This passes structurally. Human grounding review is still required.
        self.assertEqual(validate_response(raw, {"manual_motor_v1_p2"})["status"], "advice")

    def test_quantile_convention(self):
        self.assertEqual(nearest_rank(list(range(1, 21)), 0.95), 19)
        with self.assertRaises(ValueError):
            nearest_rank([], 0.95)


if __name__ == "__main__":
    unittest.main(verbosity=2)
