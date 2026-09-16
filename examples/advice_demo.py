"""Modules 4 to 6: response-contract validation with injected local stubs.

No live model, SDK, network timeout or semantic grounding is tested here.
The application keeps the independently calculated energy on failure.
"""
import json
from energy import interval_energy_Wh

ALLOWED_SOURCE_IDS = {"manual_motor_v1_p2"}
FALLBACK = {"status": "unavailable", "summary": "Advice unavailable.",
            "source_ids": []}


def validate_response(raw, allowed_ids):
    if not isinstance(raw, str) or len(raw.encode("utf-8")) > 4000:
        raise ValueError("response must be text within the 4000-byte limit")
    def reject_constant(value):
        raise ValueError(f"nonstandard JSON constant: {value}")
    try:
        data = json.loads(raw, parse_constant=reject_constant)
    except (json.JSONDecodeError, RecursionError) as exc:
        raise ValueError("response is not valid supported JSON") from exc
    if not isinstance(data, dict) or set(data) != {"status", "summary", "source_ids"}:
        raise ValueError("response fields do not match the schema")
    if data["status"] not in ("advice", "unavailable"):
        raise ValueError("unknown status")
    if not isinstance(data["summary"], str) or not (1 <= len(data["summary"]) <= 500):
        raise ValueError("summary must contain 1 to 500 characters")
    ids = data["source_ids"]
    if not isinstance(ids, list) or not all(isinstance(x, str) for x in ids):
        raise ValueError("source_ids must be a list of strings")
    if len(ids) != len(set(ids)) or not set(ids).issubset(allowed_ids):
        raise ValueError("source IDs must be unique and authorised")
    if data["status"] == "advice" and not ids:
        raise ValueError("advice must identify supporting sources")
    if data["status"] == "unavailable" and ids:
        raise ValueError("unavailable responses must have no source IDs")
    return data


def make_report(provider):
    energy = interval_energy_Wh([60.0, 120.0, 0.0], 30.0)
    try:
        advice = validate_response(provider(), ALLOWED_SOURCE_IDS)
        event = "advice_validated" if advice["status"] == "advice" else "advice_unavailable"
    except TimeoutError:
        advice = dict(FALLBACK)
        event = "advice_timeout"
    except ValueError:
        advice = dict(FALLBACK)
        event = "advice_invalid_response"
    return {"energy_Wh": energy, "advice": advice, "event": event,
            "release": "classroom-v1", "provider": "local-stub"}


def good_stub():
    return json.dumps({"status": "advice",
                       "summary": "Inspect the simulated ventilation path.",
                       "source_ids": ["manual_motor_v1_p2"]})


def invalid_stub():
    return '{"status": "advice", "summary": "Missing source field"}'


def timeout_stub():
    raise TimeoutError("simulated provider timeout")


if __name__ == "__main__":
    for provider in (good_stub, invalid_stub, timeout_stub):
        print(json.dumps(make_report(provider), indent=2))
